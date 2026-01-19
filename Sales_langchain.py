
import os
import pandas as pd
from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import List
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    AnyMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.graph import StateGraph, START, END


# ----------------------------------------------------------------
# 🔧 Setup
# ----------------------------------------------------------------
load_dotenv()
df = pd.read_csv("C:/Users/sashi/OneDrive/Documents/Langchain/products.csv")



class MessagesState(TypedDict):
    messages: List[AnyMessage]
    cart: List[str]


SYSTEM_PROMPT = (
    "You are a helpful e-commerce assistant. "
    "Recommend electronics based on user input like brand, price, or product type. "
    "If details are missing, suggest top-rated options and summarize results clearly. "
    "Always present results in a readable list with product name, ID, price, rating, and brand."
)

# Global memory for persistent chat
conversation_memory: List[AnyMessage] = [
    SystemMessage(content=SYSTEM_PROMPT)
]

# ----------------------------------------------------------------
# 🤖 Initialize model
# ----------------------------------------------------------------
model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
    temperature=0.3,
)


# ----------------------------------------------------------------
# 🧰 Tools
# ----------------------------------------------------------------
@tool
def filter_products(product_type=None, min_rating=0, price_min=0, price_max=999999, brand=None):
    """Filter and show top 5 products by type, price, or rating."""
    filtered = df[
        (df["rating"] >= min_rating)
        & (df["price"] >= price_min)
        & (df["price"] <= price_max)
    ]

    if product_type:
        synonyms = {
            "earphones": ["earbuds", "headphones"],
            "smartphone": ["phone", "mobile"],
            "laptop": ["notebook", "pc"],
        }
        related = synonyms.get(product_type.lower(), [product_type])
        mask = df["product_type"].apply(lambda x: any(w in str(x).lower() for w in related))
        filtered = filtered[mask]

    if brand:
        filtered = filtered[filtered["brand_name"].str.contains(brand, case=False, na=False)]

    if filtered.empty:
        filtered = df.nlargest(5, "rating")

    top5 = filtered.nlargest(5, "rating")[["product_id", "product_name", "brand_name", "price", "rating"]]
    lines = ["Here are the best matches I found:"]
    for _, r in top5.iterrows():
        lines.append(
            f"• {r['product_name']} (ID: {r['product_id']}) — ${r['price']} | ⭐ {r['rating']} | {r['brand_name']}"
        )
    return "\n".join(lines)


@tool
def check_inventory(product_id: str):
    """Check if a product is in stock."""
    row = df[df["product_id"] == product_id]
    if row.empty:
        return f"❌ No product found with ID {product_id}."
    qty = int(row["quantity"].values[0])
    return f"✅ Product {product_id} is available ({qty} units)." if qty > 0 else f"❌ Product {product_id} is out of stock."


@tool
def checkout(product_id: str):
    """Checkout a product by reducing inventory."""
    global df
    row = df[df["product_id"] == product_id]
    if row.empty:
        return f"❌ No product found with ID {product_id}."
    if int(row["quantity"].values[0]) > 0:
        df.loc[df["product_id"] == product_id, "quantity"] -= 1
        return f"✅ Product {product_id} checked out successfully."
    return f"❌ Product {product_id} is out of stock."


tools = [filter_products, check_inventory, checkout]
model_with_tools = model.bind_tools(tools)


# ----------------------------------------------------------------
# 🧩 LangGraph logic
# ----------------------------------------------------------------
def build_agent():
    """Build the LangGraph agent."""
    def llm_call(state: MessagesState):
        result = model_with_tools.invoke(state["messages"])
        return {"messages": state["messages"] + [result]}

    def tool_node(state: MessagesState):
        """Handle tool calls and send ToolMessage with correct tool_call_id."""
        last_msg = state["messages"][-1]
        new_messages = []

        if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
            for call in last_msg.tool_calls:
                tool_name = call["name"]
                args = call["args"]
                tool_id = call["id"]

                tool = next((t for t in tools if t.name == tool_name), None)
                if not tool:
                    result = f"❌ Tool '{tool_name}' not found."
                else:
                    try:
                        result = tool.invoke(args)
                    except Exception as e:
                        result = f"❌ Error using {tool_name}: {e}"

                # ✅ Always respond with a ToolMessage (required by OpenAI)
                new_messages.append(ToolMessage(content=str(result), tool_call_id=tool_id))

        # Append all tool responses
        return {"messages": state["messages"] + new_messages}

    def should_continue(state: MessagesState):
        last = state["messages"][-1]
        return "tool_node" if hasattr(last, "tool_calls") and last.tool_calls else END

    builder = StateGraph(MessagesState)
    builder.add_node("llm_call", llm_call)
    builder.add_node("tool_node", tool_node)
    builder.add_edge(START, "llm_call")
    builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
    builder.add_edge("tool_node", "llm_call")

    return builder.compile()


# ----------------------------------------------------------------
# Entry function for Streamlit
# ----------------------------------------------------------------
def run_agent(user_query: str, reset_memory: bool = False):
    """Run the assistant with persistent memory (for API)."""
    global conversation_memory

    if reset_memory:
        conversation_memory = [SystemMessage(content=SYSTEM_PROMPT)]

    # Add user query to memory
    conversation_memory.append(HumanMessage(content=user_query))

    agent = build_agent()
    chat_state = {"messages": conversation_memory, "cart": []}
    result = agent.invoke(chat_state)

    # Add model reply to memory
    conversation_memory.append(result["messages"][-1])

    return result["messages"][-1].content