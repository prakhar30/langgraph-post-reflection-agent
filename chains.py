from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

llm = ChatOpenAI(model="gpt-6-sol")

# These are the same things as 
# def generate_chain(inputs: dict):
#     return llm.invoke(generation_prompt.invoke(inputs))

# def reflect_chain(inputs: dict):
#     return llm.invoke(reflection_prompt.invoke(inputs))
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm