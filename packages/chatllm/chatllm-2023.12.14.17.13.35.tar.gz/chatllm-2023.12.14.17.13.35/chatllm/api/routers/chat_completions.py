#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : completions
# @Time         : 2023/7/31 10:55
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

from meutils.async_utils import sync_to_async

from fastapi import APIRouter, File, UploadFile, Query, Form
from sse_starlette import EventSourceResponse
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk

from chatllm.llmchain.completions import github_copilot
from chatllm.llmchain.completions import moonshot_kimi
from chatllm.llmchain.completions import deepseek

router = APIRouter()

ChatCompletionResponse = Union[ChatCompletion, List[ChatCompletionChunk]]


# @app.post("/chat/completions", dependencies=[Depends(check_api_key)])
@router.post("/chat/completions")
async def do_chat(request: ChatCompletionRequest):
    logger.debug(request)

    model = request.model or "gpt-3.5-turbo"
    stream = request.stream

    if model.startswith(('gpt-3.5c', 'gpt-4c')):
        completions = github_copilot.Completions()

    elif model.startswith(('kimi')):

        state_file = os.getenv('KIMI_STATE')
        if not Path(state_file).exists():
            state_file = '/Users/betterme/PycharmProjects/AI/MeUtils/examples/爬虫/state.json'
        api_key = kimi.Completions.load_state(state_file)
        completions = kimi.Completions(api_key=api_key, stream=stream)
    else:  # 兜底
        completions = OpenAI(base_url=os.getenv('OPENAI_API_BASE'), max_retries=3).chat.completions

    response: ChatCompletionResponse = completions.create(
        messages=messages,
        model=model,
        stream=stream
    )  # todo: 异步

    if stream:
        def generator():
            for chunk in response:
                # logger.debug(chunk)

                chunk = chunk.model_dump_json()
                # logger.debug(chunk)

                yield chunk

        return EventSourceResponse(generator(), ping=10000)

    return response


@sync_to_async(thread_sensitive=False)
def do_chat():
    return Completions().create("你是谁")


# print([do_chat() for _ in range(10)] | xAsyncio)


if __name__ == '__main__':
# print(arun(do_chat))
# print([do_chat() for _ in range(10)] | xAsyncio)
