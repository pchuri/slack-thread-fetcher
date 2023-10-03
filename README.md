# Slack Thread Fetcher

## Purpose

This project is a Python script for fetching messages and user information from a specific thread in Slack.

## Prerequisites

- Python 3.x
- Slack SDK for Python
- Slack Bot Token stored in a `.env` file

## Installation

1. Clone this repository.

    ```bash
    git clone https://github.com/pchuri/slack-thread-fetcher.git
    ```

2. Install the dependencies.

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file and store your Slack Bot Token.

    ```env
    BOT_TOKEN=your_slack_bot_token_here
    ```

## Usage

Run the following command in your terminal:

```bash
python main.py --thread_link "Your Slack Thread Link Here"
```

## Example

```bash
python main.py --thread_link "https://slack.com/archives/CHANNEL_ID/THREAD_ID"
```