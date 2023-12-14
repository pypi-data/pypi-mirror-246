#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : deepseek
# @Time         : 2023/12/11 14:27
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying
from meutils.queues.uniform_queue import UniformQueue

from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

requests.post = retrying(requests.post)


# DeepSeek-LLM-67B-chat
class Completions(object):
    def __init__(self, **client_params):
        self.client_params = client_params
        api_key = self.client_params.get('api_key')
        self.access_token = self.get_access_token(api_key)

    def create(self, messages: Union[str, List[Dict[str, Any]]], **kwargs):
        """
                messages=messages,
                model=model,
                stream=stream
        :param messages:
        :param kwargs:
        :return:
        """

        data = {
            "model": 'gpt-4',
            "messages": messages,

            "message": messages[-1].get('content'),
            "model_preference": None,
            "model_class": "deepseek_chat",

            **kwargs
        }
        interval = 0.01
        if data['model'].startswith("gpt-4"):
            data['model'] = "gpt-4"
            interval = 0.05

        # logger.debug(data)

        if data.get('stream'):
            if data.get('smooth'):
                # logger.debug('Smooth')
                return UniformQueue(self._stream_create(**data)).consumer(interval=interval, break_fn=self.break_fn)
            else:
                return self._stream_create(**data)
        else:
            return self._create(**data)

    def _stream_create(self, **data):
        response = self._post(**data)

        for chunk in response.iter_lines(chunk_size=1024 * 8):
            # logger.debug(chunk)
            if chunk and b'created' in chunk:

                chunk = chunk.strip(b"data: ")
                # chunk = json.loads(chunk)
                # chunk = ChatCompletionChunk.model_validate(chunk)
                chunk = ChatCompletionChunk.model_validate_json(chunk)

                chunk.choices[0].delta.role = 'assistant'
                content = chunk.choices[0].delta.content or ''
                chunk.choices[0].delta.content = content

                if content or chunk.choices[0].finish_reason:
                    yield chunk

    def _post(self, **data):
        headers = {
            'Authorization': f"Bearer {self.access_token}",  # access_token
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/119.0.0.0 Safari/537.36'
        }

        url = "https://chat.deepseek.com/api/v0/chat/completions"
        response = requests.post(
            url,
            json=data,
            headers=headers,
            stream=data.get('stream')
        )

        return response

    def get_access_token(self, api_key: Optional[str] = None):
        api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoiZDQ0NDc4MmMtZWMyOC00Y2MzLWIwNWMtOWEwZDFjMGNhZmQ2IiwiZW1haWwiOiIzMTMzMDMzMDNAcXEuY29tIiwibW9iaWxlX251bWJlciI6IjE4NTUwMjg4MjMzIiwiYXJlYV9jb2RlIjoiKzg2IiwibW9iaWxlIjoiMTg1NTAyODgyMzMiLCJleHAiOjE3MDI5MDY1NzksImF1ZCI6IjY1MjhhZDM5NmZhYTEzNjdmZWU2ZDE2YyJ9.rim3f12-rIPorw-5M8H4FN-vmBw7yRu24rSsyshm9a8"
        return api_key

    @staticmethod
    def break_fn(line: ChatCompletionChunk):
        return line.choices[0].finish_reason


if __name__ == '__main__':
    data = {'model': 'gpt-4', 'messages': [{'role': 'user', 'content': '1+1'}], 'stream': True}
    _ = Completions().create(**data, smooth=0)

    # 我是DeepSeek Chat，一个由深度求索公司开发的智能助手，旨在通过自然语言处理和机器学习技术来提供信息查询、对话交流和解答问题等服务。

    # for i in tqdm(_):
    for i in _:
        content = i.choices[0].delta.content
        # content = (content.replace('Deep', 'X').replace('Seek', 'X'))

        print(content, end='')
