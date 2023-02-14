"""Main module."""
import asyncio
import logging

import cfg4py
from sanic import Sanic, response

from chatter.config import get_config_dir
from chatter.dingtalk import ding
from chatter.gpt import GPT35
from chatter.gpt3 import GPT3

application = Sanic("chatter")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

bots = {
    "gpt3": None,
    "gpt35": None
}

"""
{
    "conversationId": "xxx",
    "atUsers": [
        {
            "dingtalkId": "xxx",
            "staffId":"xxx"
        }
    ],
    "chatbotCorpId": "dinge8a565xxxx",
    "chatbotUserId": "$:LWCP_v1:$Cxxxxx",
    "msgId": "msg0xxxxx",
    "senderNick": "杨xx",
    "isAdmin": true,
    "senderStaffId": "user123",
    "sessionWebhookExpiredTime": 1613635652738,
    "createAt": 1613630252678,
    "senderCorpId": "dinge8a565xxxx",
    "conversationType": "2",
    "senderId": "$:LWCP_v1:$Ff09GIxxxxx",
    "conversationTitle": "机器人测试-TEST",
    "isInAtList": true,
    "sessionWebhook": "https://oapi.dingtalk.com/robot/sendBySession?session=xxxxx",
    "text": {
        "content": " 你好"
    },
    "msgtype": "text"
}
"""
def find_agent(staff_id: str):
    cfg = cfg4py.get_instance()
    for user in cfg.users:
        if user.get("userid") == staff_id:
            logger.info("user %s use model %s", staff_id, user.get("model"))
            return user.get("model")

    return "gpt3"
        
@application.route("/abcde/chatter", methods=["GET", "POST"])
async def root(request):
    global bots

    params = request.json or {}
    question = params.get("text", {}).get("content", "")
    sender_id = params.get("senderStaffId", "")
    nickname = params.get("senderNick", "")
    logger.info("chat with %s, received:\n%s", nickname, params)

    if len(question) == 0:
        return response.text("ok")

    bot = find_agent(sender_id)
    msg = await bot.ask(question, session_id=sender_id)

    logger.info("got answer from GPT:%s", msg)
    await ding(msg)
    return response.text("OK")

@application.route("/abcde/status")
async def status(request):
    return response.text("OK")

@application.listener("before_server_start")
async def application_init(app, *args):
    global bots

    cfg4py.init(get_config_dir())
    while True:
        try:
            bots["gpt35"] = GPT35() # type: ignore
            break
        except Exception as e:
            logger.error("init gpt35 failed, retry in 5s", exc_info=e)
            await asyncio.sleep(5)

    while True:
        try:
            bots["gpt3"] = GPT3() # type: ignore
            break
        except Exception as e:
            logger.error("init gpt 3 failed, retry in 5s", exc_info=e)
            await asyncio.sleep(5)


@application.listener("after_server_stop")
async def application_exit(app, *args):
    pass


def start(port=2130):
    application.config.RESPONSE_TIMEOUT = 60 * 10

    application.run(host="0.0.0.0", port=port, register_sys_signals=True, workers=1)
    logger.info("chatter server stopped")
