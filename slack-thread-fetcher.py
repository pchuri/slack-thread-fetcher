import json
import re
import argparse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

def fetch_text_from_slack_thread(thread_link):
    try:
        bot_token = os.getenv("BOT_TOKEN")
        client = WebClient(token=bot_token)
        channel_id, message_ts = re.search("\/archives\/(.+)\/p(\d+)", thread_link).groups()
        thread_ts = f"{message_ts[:-6]}.{message_ts[-6:]}"
        
        response = client.conversations_replies(channel=channel_id, ts=thread_ts)

        messages = response["messages"]
        json_messages = []

        for message in messages:
            json_message = {}
            user_id = message.get('user')
            
            # Fetching the entire user information
            user_info = client.users_info(user=user_id)
            
            processed_text = message["text"]
            if processed_text.strip():
                json_message['text'] = processed_text
                json_message['user_info'] = user_info['user']  # Adding the entire user_info
                json_message['ts'] = message.get('ts')
                json_messages.append(json_message)

        print(json.dumps(json_messages, indent=4, ensure_ascii=False))
    except SlackApiError:
        print("Slack API Error")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch Slack thread messages')
    parser.add_argument('thread_link', type=str, help='Slack thread link to fetch')

    args = parser.parse_args()
    fetch_text_from_slack_thread(args.thread_link)