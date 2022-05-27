import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from env import bot_token

os.system('pytest cases -s -v > report.log ')

with open('./report.log','r') as f:
    data = f.read()

client = WebClient(token=bot_token)

try:
    response = client.chat_postMessage(channel='tkeel', text=data)
except SlackApiError as e:
    # You will get a SlackApiError if "ok" is False
    assert e.response["ok"] is False
    assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
    print(f"Got an error: {e.response['error']}")