
import logging

import cfg4py
import openai

logger = logging.getLogger(__name__)

class GPT3:
    def __init__(self) -> None:
        self.sessions = {

        }
        cfg = cfg4py.get_instance()
        openai.api_key = cfg.openai.api_key
        self._gpt = openai.Completion

    async def ask(self, question: str, session_id: str, time_out:int=10) -> str:

        chat_log = self.sessions.get(session_id, question)

        prompt = f"{chat_log}Human: {question}\nAI:"
        response = await self._gpt.acreate(
            prompt = prompt, 
            model =  "text-davinci-003",
            temperature = 0.85,
            top_p=1, 
            frequency_penalty=0, 
            presence_penalty=0.7, 
            best_of=1,
            max_tokens=150,
            timeout=time_out
        )

        bot_utterance = response.choices[0].text
        chat_log = self.sessions.get(session_id, "")
        chat_log += f"Human: {question}\nAI: {bot_utterance}\n"

        self.sessions[session_id] = chat_log[-1000:]
        logger.info("got answer from GPT-3:%s", bot_utterance)
        return bot_utterance

