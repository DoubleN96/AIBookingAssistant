# import gradio as gr
import logging
import os
import openai

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

MODEL = 'gpt-3.5-turbo'
openai.api_key = os.environ.get('OPEN_API_KEY', "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")

BOOKING_AGENT_TEMPLATE = """
You are a room booking assistant. Be kind, detailed and nice, but also try to sell the booking of the apartment to me. 
Present the three given queried search result in a nice way as answer to the user input. dont ask questions back! 
just take the given context

{chat_history}
Human: {user_msg}
Chatbot:"""

BOOKING_PROMPT = PromptTemplate(
    input_variables=["chat_history", "user_msg"],
    template=BOOKING_AGENT_TEMPLATE
)


llm = OpenAI(
    model_name=MODEL,
    temperature=0.3,
    openai_api_key=openai.api_key
)

booking_prompt = PromptTemplate(
    input_variables=["product_description"],
    template="Create comma seperated product keywords to perform a query on a airbnb dataset for this user input: "
             "{product_description}",
)


def get_booking_chain():
    logging.info('Building the chatgpt booking assistant object.')
    return LLMChain(llm=llm, prompt=booking_prompt)


def booking_interact(results, userinput):
    full_result_string = ''
    for product in results.docs:
        full_result_string += ' '.join(
            [
                product.property_type, product.name, f", amenities are:", product.amenities, " Located in city:",
                product.city,
                'ID of this booking is:', product.id,
                "\n\n\n"
            ]
        )

    memory = ConversationBufferMemory(memory_key="chat_history")
    llm_chain = LLMChain(
        llm=OpenAI(model_name="gpt-3.5-turbo", temperature=0.8,
                   openai_api_key="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"),
        prompt=BOOKING_PROMPT,
        verbose=False,
        memory=memory,
    )

    answer = llm_chain.predict(user_msg=f"{full_result_string} ---\n\n {userinput}")
    return "Bot:", answer


chatter = openai.ChatCompletion(
    model_name=MODEL,
    verbose=False
)


def get_response(message_history: list[dict], user_input: str):
    if not message_history:
        message_history = [
            {"role": "system", "content": "You are the assistant answering users questions."},
            {"role": "user", "content": user_input}
        ]
    return chatter.create(
          model="gpt-3.5-turbo",
          messages=message_history
    )
# TODO: Add voice Input
# TODO: Add Redis and import CSV
