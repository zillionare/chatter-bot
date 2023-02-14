import logging
import cfg4py

import arrow
from async_timeout import timeout
from revChatGPT.V2 import Chatbot

logger = logging.getLogger(__name__)

class GPT35:
    def __init__(self) -> None:
        cfg = cfg4py.get_instance()
        logger.info("logging to chatGPT")
        self.gpt = Chatbot(
            cfg.openai.user,
            cfg.openai.passwd
        )

        if self.gpt.api_key is None:
            logger.error("login failed")
            raise Exception("login failed")

        
        self.chat_sessions = {}

    async def ask(self, prompt: str, session_id: str, time_out:int=10):
        self.chat_sessions.update({session_id: arrow.now()})

        bot_utterance = []
        try:
            async with timeout(time_out) as cm:
                async for line in self.gpt.ask(
                    prompt=prompt, 
                    conversation_id=session_id
                ): # type: ignore
                    result = line["choices"][0]["text"].replace("<|im_end|>", "")
                    bot_utterance.append(result)
                    cm.shift(1)
        except Exception as e:
            logger.exception(e)
            return "机器人忙，请稍候重试"
                
        if len(bot_utterance) == 0:
            return "机器人忙，请稍候重试。"
        
        answer = "".join(bot_utterance)
        logger.info("got answer from GPT:%s", answer)
        return answer
