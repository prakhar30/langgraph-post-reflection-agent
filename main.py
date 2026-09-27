from typing import TypedDict, Annotated
from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from chains import generate_chain, reflect_chain

class MessageGraph(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

REFLECT = "reflect"
GENERATE = "generate"

def generation_node(state: MessageGraph):
    return {"messages": [generate_chain.invoke({"messages": state["messages"]})]}

def reflection_node(state: MessageGraph):
    res = reflect_chain.invoke({"messages": state["messages"]})
    # artificially tagging this generated message as a human message, as a prompting technique.
    return {"messages": [HumanMessage(content=res.content)]}

def should_continue(state: MessageGraph):
    if len(state["messages"]) > 6:
        return END
    return REFLECT

builder = StateGraph(state_schema=MessageGraph)
builder.add_node(GENERATE, generation_node)
builder.set_entry_point(GENERATE)
builder.add_node(REFLECT, reflection_node)

builder.add_conditional_edges(GENERATE, should_continue, path_map={END:END, REFLECT:REFLECT})
builder.add_edge(REFLECT, GENERATE)

graph = builder.compile()
graph.get_graph().draw_mermaid_png(output_file_path='mermain.png')

def main():
    print("Hello from langgraph-reflection-agent!")
    inputs = {
        "messages": [
            HumanMessage(content="""
                Make this LinkedIn post better to gain more interations and following:
                
                Bookmarky now summarizes your saved articles with one tap.
                Powered by Apple Intelligence, everything runs on-device — your reading data stays private. Save the link, skip the scroll, get the gist.

                Download free on the App Store: https://shorturl.at/8QiJL
                hashtag#AI hashtag#AppleIntelligence hashtag#iOS hashtag#IndieApp hashtag#BuildInPublic hashtag#Productivity
                """)
        ]
    }
    response = graph.invoke(inputs)
    print(response)

if __name__ == "__main__":
    main()
