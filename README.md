# Sakhi Telegram Unified Bot Service

The Sakhi Telegram Bot is a Python-based bot that interacts with the Sakhi API Server via Telegram. It allows users to perform various actions and access information from the API Server through the convenience of a Telegram chat interface.

## Prerequisites

- Python
- Telegram Bot API token
- Telegram Bot Name
- Activity API Server URL
- Story API Server URL
- Log Level

## Installation

1. Clone the repository

   ```bash
   git  clone https://github.com/DJP-Digital-Jaaduii-Pitara/sakhi-telegram-unified-service.git

2. Install required python packages

   ```bash
   pip install -r requirements.txt

3. Set up the configuration

   - SERVICE_ENVIRONMENT -  (dev, prod)
   - TELEGRAM_BASE_URL - (Telegram callback URL)
   - TELEGRAM_BOT_TOKEN
   - TELEGRAM_BOT_NAME
   - ACTIVITY_API_BASE_URL
   - STORY_API_BASE_URL - (Default, Teacher, Parent)
   - TELEMETRY_ENDPOINT_URL
   - TELEMETRY_LOG_ENABLED - (true/false)
   - LOG_LEVEL - (DEBUG, INFO, ERROR)
   - SUPPORTED_LANGUAGES - (en,bn,gu,hi,kn,ml,mr,or,pa,ta,te)

5. Start the Telegram bot

   - python telegram_webhook.py

## Usage

Once the Telegram bot is up and running, you can interact with it through your Telegram chat. Start a chat with the bot and use the available commands and features to perform actions and retrieve information from the Sakhi API Server.

  - The bot provides the following commands:

    ```bash
    /start: Start the conversation with the bot

  - Select preferred language
  - Select story or activites
  - Start querying questions

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
