import os
import openai

from llama_index.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.callbacks.base import CallbackManager
from llama_index import (
    LLMPredictor,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from langchain.chat_models import ChatOpenAI
import chainlit as cl
from transcribe_video import VideoTranscriber
openai.api_key = os.environ.get("OPENAI_API_KEY")

# try:
#     # rebuild storage context
#     storage_context = StorageContext.from_defaults(persist_dir="./storage")
#     # load index
#     index = load_index_from_storage(storage_context)
# except:
#     from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

#     documents = SimpleDirectoryReader("./outputs").load_data()
#     index = GPTVectorStoreIndex.from_documents(documents)
#     index.storage_context.persist()

def create_index():
    try:
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
    except:
        from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
        documents = SimpleDirectoryReader("./outputs").load_data()
        index = GPTVectorStoreIndex.from_documents(documents)
        index.storage_context.persist()
    return index
@cl.on_chat_start
async def factory():
    files = None

    # Wait for the user to upload a file
    while files == None:
        files = await cl.AskFileMessage(
            content="Please upload a text video to begin!",
            accept=[".mp4"],
            max_size_mb=100,
            timeout=180,
        ).send()

    file = files[0]

    msg = cl.Message(
        content=f"Processing `{file.name}`...", disable_human_feedback=True
    )
    
    await msg.send()
    transcriber = VideoTranscriber()
    await cl.make_async(transcriber.transcribe_video)(file.content, "outputs/trascripts.txt")
    # transcriber.transcribe_video(file.content, "outputs/trascripts.txt")
    index=await cl.make_async(create_index)()
    msg.content = f"Processing `{file.name}` done in format '. You can now ask questions!"
    await msg.update()
    llm_predictor = LLMPredictor(
        llm=ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
            streaming=True,
        ),
    )
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor,
        chunk_size=512,
        callback_manager=CallbackManager([cl.LlamaIndexCallbackHandler()]),
    )

    query_engine = index.as_query_engine(
        service_context=service_context,
        streaming=True,
    )

    cl.user_session.set("query_engine", query_engine)


@cl.on_message
async def main(message: cl.Message):
    query_engine = cl.user_session.get("query_engine")  # type: RetrieverQueryEngine
    response = await cl.make_async(query_engine.query)(message.content)

    response_message = cl.Message(content="")

    for token in response.response_gen:
        await response_message.stream_token(token=token)

    if response.response_txt:
        response_message.content = response.response_txt

    await response_message.send()