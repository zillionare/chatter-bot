# ChatGPT/GPT 3.0钉钉机器人

将钉钉机器人的消息发送到GPT 3.0/ChatGPT，让GPT回复你的消息。

## 使用方法
在群里@机器人，消息就会传给服务器，服务器再与gpt通讯获得回答后，将消息传回钉钉群。

群里每个人都有与GPT的专属会话，不受其它人对话的干扰。

支持GPT 3.0/chatGPT，通过修改~/.chatter/config/defaults.yml来配置：
```yaml
users:
    - userid: 0356204035841823
      name: "张三"
      model: gpt3
    - userid: 0356204035841824
      name: "李四"
      model: gpt35
```
这里的userid是指群里用户的staffId。

需要配置钉钉的secrets和token，openai的用户名、密码和API Key。

## 模型
GPT 3.0: https://openai.com/blog/openai-api/
ChatGPT: 即3.5代GPT模型，比GPT 3.0更先进、智能。

## TODO
cli未调通。理想情况下，通过以下命令来启动：
```bash
chatter start
```
