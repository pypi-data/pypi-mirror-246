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

from fastapi import APIRouter, File, UploadFile, Query, Form
from sse_starlette import EventSourceResponse
from chatllm.schemas.openai_api_protocol import ChatCompletionRequest, UsageInfo

from openai import OpenAI, AsyncOpenAI
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

    model = request.model.strip().lower()
    stream = request.stream

    if model.startswith(('kimi', 'moonshot')):
        state_file = "/www/0_apps/cookies/kimi_cookies.json"
        completions = moonshot_kimi.Completions(api_key=Path(state_file).exists() and state_file or None)

    elif model.startswith(('deepseek',)):
        completions = deepseek.Completions()

    elif model.startswith(('gpt-4', 'gpt-3',)):
        completions = github_copilot.Completions()

    else:  # 兜底
        completions = AsyncOpenAI(base_url=os.getenv('OPENAI_API_BASE'), max_retries=3).chat.completions
        completions.acreate = completions.create

    # response: ChatCompletionResponse = completions.create(**request.model_dump())
    response: ChatCompletionResponse = await completions.acreate(**request.model_dump())

    if stream:
        generator = (chunk.model_dump_json() for chunk in response)

        # def generator():
        #     for chunk in response:
        #         # logger.debug(chunk)
        #
        #         chunk = chunk.model_dump_json()
        #         # logger.debug(chunk)
        #
        #         yield chunk

        return EventSourceResponse(generator, ping=10000)

    return response


if __name__ == '__main__':
    from meutils.serving.fastapi import App

    app = App()

    app.include_router(router, '/v1')

    app.run()
