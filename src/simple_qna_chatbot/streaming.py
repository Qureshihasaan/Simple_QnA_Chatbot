import os 
from dotenv import load_dotenv
import chainlit as cl 
from agents import Agent , Runner , AsyncOpenAI , OpenAIChatCompletionsModel
from agents.run import RunConfig
from typing import cast
from openai.types.responses import ResponseTextDeltaEvent

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    default_headers={
        "Content-Type": "application/json",
    }
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

simple_agent = Agent(name="Q&A_agent" , 
                  instructions="You are a helpful assistant and you have to assists user with their queries. Answer user questions concisely and informatively.",
                  model=model
                  )

@cl.on_chat_start
async def start():
    cl.user_session.set("chat_history" , [])
    cl.user_session.set("agent" , simple_agent)
    await cl.Message(content="Hello! How can I help you?").send()

@cl.on_message
async def main(message : cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent : Agent = cast(Agent , cl.user_session.get("agent"))
    config : RunConfig = cast(RunConfig , cl.user_session.get("config"))

    history = cl.user_session.get("chat_history") or []

    history.append({"role": "user" , "content":message.content})

    try: 
        result = Runner.run_streamed(agent , history)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data , ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)

        response_content = result.final_output
        msg.content = response_content
        await msg.update()

        history.append({"role":"assistant" , "content": response_content})

        cl.user_session.set("chat_history" , history)

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")