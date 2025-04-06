import os 
from dotenv import load_dotenv
from agents import Agent , OpenAIChatCompletionsModel , AsyncOpenAI , Runner
from agents.run import RunConfig
from typing import cast
import chainlit as cl
from pydantic import BaseModel

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key: 
    raise ValueError("Please set the GEMINI_API_KEY environment variable")


@cl.on_chat_start
async def on_start():

    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client,
        
    
    )
    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    
    )


    cl.user_session.set("chat_history" , [])

    cl.user_session.set("config" , config)


    agent : Agent = Agent(
        name="Chatbot" , 
        instructions="You are a helpful assistant and you have to assists user with their queries.",
        model=model
        )

    cl.user_session.set("agent", agent)

    await cl.Message(content="Hello! I am a chatbot. How can I help you?").send()

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent : Agent = cast(Agent, cl.user_session.get("agent"))

    config : RunConfig = cast(RunConfig, cl.user_session.get("config"))


    history = cl.user_session.get("chat_history") or []

    history.append({"role":"user", "content": message.content})



    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n" , history , "\n")
        result = Runner.run_sync(starting_agent=agent , 
                                     input=history,
                                     run_config=config
                                     )
        # async for event in result.stream_events():
        #     if event.type == "raw_response_event"  and hasattr(event.data , "delta") :
        #         token = event.data.delta
        #         await msg.stream_token(token)     
        # print("------------")  
        # print(result.json())
        ### for run_sync method
        response_content = result.final_output

        msg.content = response_content
        await msg.update()

        cl.user_session.set("chat_history", result.to_input_list())
        

        print(f"User: , {message.content}")
        print(f"Agent:, {response_content}")
        # print(f"Agent:, {msg.content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")