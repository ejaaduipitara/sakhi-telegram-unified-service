# Sakhi Telegram Unified Bot Service

The Sakhi Telegram Bot is a Python-based bot that interacts with the Sakhi API Server via Telegram. It allows users to perform various actions and access information from the API Server through the convenience of a Telegram chat interface.

## Prerequisites

- Python 3.8+
- Starlette
- Redis (for user session)
- python-telegram-bot library
- Telegram bot token
- Secure public domain to configure webhook URL. (use [ngrok](https://ngrok.com/) for local setup)

## Installation

1. Clone the repository

   ```bash
   git clone https://github.com/Sunbird-AIAssistant/sakhi-telegram-unified-service.git
   cd sakhi-telegram-unified-service

2. Install required python dependencies

   ```bash
   pip install -r requirements.txt

3. Set up your Telegram bot:
   - Create a new bot on Telegram and obtain the [bot token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token).
   - Set up a webhook URL (using a public domain with [SSL/TLS support](https://core.telegram.org/bots/webhooks#always-ssl-tls))

     If you're having any trouble setting up webhooks, please check out this [amazing guide to webhooks](https://core.telegram.org/bots/webhooks).

4. Set up environment variables:
   - Create a .env file in the project root and add the following variables:
   ```bash
   SERVICE_ENVIRONMENT=dev
   TELEGRAM_BASE_URL=https://your-telegram-callback-url.com
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   TELEGRAM_BOT_NAME=your-telegram-bot-name
   ACTIVITY_API_BASE_URL=https://your-activity-api-url.com
   STORY_API_BASE_URL=https://your-story-api-url.com
   TELEMETRY_ENDPOINT_URL=https://your-telemetry-endpoint-url.com
   TELEMETRY_LOG_ENABLED=true # true or false
   LOG_LEVEL=DEBUG # INFO, DEBUG, ERROR
   SUPPORTED_LANGUAGES=en,bn,gu,hi,kn,ml,mr,or,pa,ta,te
   REDIS_HOST=your-redis-host
   REDIS_PORT=your-redis-port
   REDIS_INDEX=your-redis-index
   ```
   **Note:** This telegram bot only supports the following languages: en, bn, gu, hi, kn, ml, mr, or, pa, ta, te.

## Usage

1. Ensure Redis is running. If not installed, you can download it from [official Redis website](https://redis.io/).

2. Start the Starlette app:
   ```bash
   python3 telegram_webhook.py

3. Once the Telegram bot is up and running, you can interact with it through your Telegram chat. Start a chat with the bot and use the available commands and features to perform actions and retrieve information from the API Server.

   - The bot provides the following commands:

      ```bash 
      /start: Start the conversation with the bot

   - Select preferred language
   - Select the context (If multiple context configurations are configured)
   - Start querying questions

## Configuration (config.ini)

| Variable                        | Description                                                                                    | Default Value                        |
|:--------------------------------|------------------------------------------------------------------------------------------------|--------------------------------------|
| default.context                | Context of the bot based on which indexing and retrieval of documents and LLM response is based on |             story                         |
| default.language      | This configuration sets the default language for the chatbot interaction. When a user starts a conversation, the chatbot will use this language unless explicitly changed. | en                                    |
| default.welcome_msg         | This configuration defines the initial message displayed by the chatbot when a user starts a conversation.      | Namaste 🙏 Welcome to *e-Jaadui Pitara* _(Powered by Bhashini)_                                |
| default.languages    | This configuration specifies the list of languages displayed by the chatbot  when a user starts a conversation.                                                           |  For example: [{"text": "English", "code": "en","index": 1}...{}]    |
| default.converse_enabled    | This option is a flag (either true or false) that controls whether the chatbot can engage in a conversational chat style interaction.                                                | false     |
| telemetry.telemetry_log_enabled | Flag to enable or disable telemetry events logging to Sunbird Telemetry service                | true                                 |
| telemetry.environment           | service environment from where telemetry is generated from, in telemetry service               | dev                                  |
| telemetry.service_id            | service identifier to be passed to Sunbird telemetry service                                   |                                      |
| telemetry.service_ver           | service version to be passed to Sunbird telemetry service                                      |                                      |
| telemetry.actor_id              | service actor id to be passed to Sunbird telemetry service                                     |                                      |
| telemetry.channel               | channel value to be passed to Sunbird telemetry service                                        |                                      |
| telemetry.pdata_id              | pdata_id value to be passed to Sunbird telemetry service                                       |                                      |
| telemetry.events_threshold      | telemetry events batch size upon which events will be passed to Sunbird telemetry service      | 5                                    |


## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.
