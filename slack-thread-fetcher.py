import json
import re
import argparse
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

user_cache = {}  # Initialize user cache

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
            json_message['text'] = message["text"]

            # Fetch user info
            user_id = message.get('user')
            if user_id:
                if user_id not in user_cache:  # If not cached, fetch and cache
                    user_info = client.users_info(user=user_id)
                    user_cache[user_id] = {
                        'id': user_info['user']['id'],
                        'name': user_info['user']['name'],
                        'real_name': user_info['user']['real_name'],
                        'display_name': user_info['user']['profile']['display_name']
                    }

                json_message['user_info'] = user_cache[user_id]  # Retrieve from cache

            json_message['ts'] = message.get('ts')
            json_messages.append(json_message)

        print(json.dumps(json_messages, indent=4, ensure_ascii=False))
    except SlackApiError as e:
        print(f"Slack API Error: {e.response['error']}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch Slack thread messages')
    parser.add_argument('thread_link', type=str, help='Slack thread link to fetch')

    args = parser.parse_args()
    fetch_text_from_slack_thread(args.thread_link)