#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kimi
# @Time         : 2023/11/29 17:00
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.cache_utils import ttl_cache
from meutils.decorators.retry import retrying

from chatllm.llmchain.utils import tiktoken_encoder
from chatllm.schemas.kimi.protocol import EventData

from openai.types.chat import chat_completion_chunk, chat_completion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk

from meutils.queues.uniform_queue import UniformQueue

post = retrying(requests.post)


class Completions(object):
    def __init__(self, **client_params):
        self.client_params = client_params
        api_key = self.client_params.get('api_key')  # state_file
        self.access_token = self.get_access_token(api_key)

    def create(
        self,
        messages: Union[str, List[Dict[str, Any]]],
        **kwargs,
    ):
        data = {
            "model": 'gpt-4',
            "messages": messages if isinstance(messages, list) else [{"role": "user", "content": messages}],
            **kwargs
        }

        # 额外参数
        refs = data.get('model', '').strip('kimi-').split('|')  # ['']
        refs = data.pop('refs', refs[0] and refs or [])
        use_search = False if refs else data.pop('use_search', True)
        data["refs"] = refs
        data["use_search"] = use_search

        logger.debug(f"RequestData：{data}")

        if data.get('stream'):
            return UniformQueue(self._stream_create(**data)).consumer(interval=0.01, break_fn=self.break_fn)
            # return self._stream_create(**data)
        else:
            return self._create(**data)

    def _create(self, **data):

        # todo
        # response = requests.post(url, json=json_str, headers=headers)
        # response.encoding = 'utf-8'
        # response.text.strip().split('\n\n')

        content = ''
        chunk_id = created = None
        model = data.get('model', 'kimi')
        for chunk in self._stream_create(**data):
            chunk_id = chunk.id
            created = chunk.created
            content += chunk.choices[0].delta.content

        message = chat_completion.ChatCompletionMessage(role='assistant', content=content or '[ERROR]授权过期')

        choice = chat_completion.Choice(
            index=0,
            message=message,
            finish_reason='stop'
        )

        prompt_tokens, completion_tokens = map(len, tiktoken_encoder.encode_batch([str(data.get('messages')), content]))
        total_tokens = prompt_tokens + completion_tokens

        usage = chat_completion.CompletionUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens
        )

        completion = chat_completion.ChatCompletion(
            id=chunk_id,
            choices=[choice],
            created=created,
            model=model,
            object="chat.completion",
            usage=usage

        )

        return completion

    def _stream_create(self, **data):  # {'messages': messages, "refs": refs, "use_search": use_search}
        response = self._post(**data)

        chunk_id = f"chatcmpl-{uuid.uuid1()}"
        created = int(time.time())
        model = data.get('model', 'kimi')  # "kimi-clk4da83qff43om28p80|clk4da83qff43om28p80"
        finish_reason = None

        for chunk in response.iter_lines(chunk_size=1024 * 8):
            if chunk:
                chunk = chunk.strip(b"data: ")
                event_data = EventData(**json.loads(chunk))

                if event_data.event == "all_done" or event_data.error_type:
                    finish_reason = 'stop'
                    logger.debug(chunk.decode())
                ##############################AGI#################################
                if event_data.event == 'debug':
                    logger.debug(event_data.message)
                if event_data.event == 'search_plus':
                    logger.debug(event_data.msg)
                ##############################AGI#################################
                if event_data.text or finish_reason:
                    chunk = {
                        'id': chunk_id,
                        'choices': [
                            {
                                'delta': {
                                    'content': event_data.text,
                                    'function_call': None,
                                    'role': 'assistant',
                                    'tool_calls': None
                                },
                                'finish_reason': finish_reason,
                                'index': 0
                            }
                        ],
                        'created': created,
                        'model': model,
                        'object': 'chat.completion.chunk',
                        'system_fingerprint': None
                    }

                    chunk = ChatCompletionChunk.model_validate(chunk)

                    # logger.debug(chunk)

                    yield chunk

    def _post(self, **data):
        headers = {
            'Authorization': f"Bearer {self.access_token}",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }

        url = self._create_url(headers=headers, **data)  # 可以传入额外参数 比如conversation_name， file_id

        response = post(
            url,
            json=data,
            headers=headers,
            stream=data.get('stream'),
        )

        # logger.debug(response.text)
        return response

    @staticmethod
    @ttl_cache(ttl=3600)
    def _create_url(conversation_name: Optional[str] = None, headers: Optional[dict] = None, **kwargs):
        conversation_name = conversation_name or f"「Xchat：{time.ctime()}」"

        headers = headers or {}
        url = "https://kimi.moonshot.cn/api/chat"
        payload = {"name": conversation_name, "is_example": False}
        response = requests.post(url, json=payload, headers=headers).json()
        # logger.debug(response)

        conversation_id = response.get('id')
        return f"{url}/{conversation_id}/completion/stream"

    @staticmethod
    @retrying
    @ttl_cache(ttl=60)
    def get_access_token(state_file):
        cookies = json.loads(Path(state_file).read_text())
        storage = cookies.get('origins', [{}])[0].get('localStorage', [{}])

        access_token = refresh_token = None
        for name2value in storage:
            if name2value.get('name') == 'access_token':
                access_token = name2value.get('value')
            if name2value.get('name') == 'refresh_token':
                refresh_token = name2value.get('value')

        return access_token

    @staticmethod
    def break_fn(line: ChatCompletionChunk):
        return line.choices[0].finish_reason


if __name__ == '__main__':
    state_file = "/Users/betterme/PycharmProjects/AI/MeUtils/examples/爬虫/kimi_cookies.json"
    completion = Completions(api_key=state_file)

    data = {'model': 'kimi-clk4da83qff43om28p80|clk4da83qff43om28p80',
            'messages': [{'role': 'user', 'content': '总结一下'}], 'stream': True, 'use_search': False}

    r = completion.create(**data)
    for i in r:
        print(i.choices[0].delta.content, end='')
