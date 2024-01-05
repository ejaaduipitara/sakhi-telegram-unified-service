import json
import os
from typing import Union, TypedDict

import requests
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import __version__ as TG_VER
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, \
    CallbackQueryHandler, Application

from logger import logger

"""
start - Start the bot
set_engine - To choose the engine 
set_language - To choose language of your choice
"""

load_dotenv()

botName = os.environ['TELEGRAM_BOT_NAME']

concurrent_updates = int(os.getenv('concurrent_updates', '1'))
pool_time_out = int(os.getenv('pool_timeout', '10'))
connection_pool_size = int(os.getenv('connection_pool_size', '100'))

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

language_msg_mapping: dict = {
    "en": """
*My Jaadui Pitara*
I am here to help you with amazing stories and activities that you can engage your children with.

Please select Story Sakhi for creating your own story
Please select Parent Sakhi for getting suggestions of activities that you can engage with your children at home
Please select Teacher Sakhi for getting suggestions of activities that you can engage with your children at school
""",
    "hi": """
*मेरा जादुई पिटारा*
मैं यहां अद्भुत कहानियों और गतिविधियों के साथ आपकी मदद करने के लिए हूं, जिनमें आप अपने बच्चों को शामिल कर सकते हैं।

अपनी कहानी बनाने के लिए कहानी सखी का चयन करें
आप घर पर अपने बच्चों के साथ शामिल करनेके गतिविधियों के सुझाव प्राप्त करने के लिए अभिभवक सखी का चयन करें 
आप स्कूल में अपने बच्चों के साथ शामिल करनेके गतिविधियों के सुझाव प्राप्त करने के लिए शिक्षक सखी  का चयन करें 
"""
}

lang_bot_name_mapping = {
    "en": {
        "story" : "Story Sakhi",
        "teacher": "Teacher Sakhi",
        "parent": "Parent Sakhi"
    },
    "hi": {
        "story" : "कहानी सखी",
        "teacher": "शिक्षक सखी",
        "parent": "अभिभावक सखी"
    }
}

bot_default_msg = {
    "en": {
        "story": """
Wecome to *Story Sakhi!*
I can create a story for you about what you ask for. 

For example:
- I can tell a story about a girl who saw the sea for the first time.
- I can tell a story about a Monkey and a Frog

Ask me about anything that you want. You can type or speak.
""",
    "teacher": """
Wecome to *Teacher Sakhi!*
I can suggest you activities that you can do with your students (of age 3 to 8 years) at schools. 
I can also answer your questions about the play based learning suggested in the new NCF for Foundational Stage.
Here are few examples of what you can ask.

Examples:
- What activity can I do with students to teach sorting or counting numbers
- How can I conduct my class with children with special needs
- What can I do to engage a child who is always distracted.
I can answer your questions about the new NCF

Ask me about anything that you want. You can type or speak.
""",
    "parent": """
Wecome to *Parent Sakhi!*
I can suggest you activities that you can do with your children at home. Here are few examples of what you can ask:

Examples:
- What activity can I do with my child using vegetables in your kitchen
- Suggest how I can make my child interested in household activities
- My child does not eat nutritious food, what to do

Ask me about anything that you want. You can type or speak.
"""
    },
    "hi": {
       "story": """
*कहानी सखी* में आपका स्वागत है!
आप जो मांगेंगे उसके बारे में मैं आपके लिए एक कहानी बना सकता हूं।

उदाहरण के लिए:
- मैं उस लड़की की कहानी बता सकता हूँ जिसने पहली बार समुद्र देखा।
- मैं एक बंदर और मेंढक के बारे में एक कहानी बता सकता हूँ

आप जो चाहते हो वो मुझसे पूछ सकते हैं। आप टाइप कर सकते हैं या बोल सकते हैं।"
""",
    "teacher": """
*शिक्षक सखी* में आपका स्वागत है!
मैं आपको ऐसी गतिविधियाँ सुझा सकता हूँ जो आप स्कूलों में अपने छात्रों (3 से 8 वर्ष की आयु के) के साथ कर सकते हैं।
मैं फाउंडेशनल स्टेज के लिए नए एनसीएफ में सुझाए गए खेल आधारित शिक्षण के बारे में आपके सवालों का जवाब भी दे सकता हूं।
यहां कुछ उदाहरण दिए गए हैं कि आप क्या पूछ सकते हैं।

उदाहरण:
- संख्याओं को क्रमबद्ध करना या गिनना सिखाने के लिए मैं विद्यार्थियों के साथ कौन सी गतिविधि कर सकता हूँ?
- मैं विशेष आवश्यकता वाले बच्चों के साथ अपनी कक्षा कैसे संचालित कर सकता हूँ?
- मैं उस बच्चे को व्यस्त रखने के लिए क्या कर सकता हूं जो हमेशा विचलित रहता है?
- मैं नए एनसीएफ के बारे में आपके सवालों का जवाब दे सकता हूं

आप जो चाहते हो वो मुझसे पूछ सकते हैं। आप टाइप कर सकते हैं या बोल सकते हैं।
""",
    "parent": """
*अभिबवक सखी* में आपका स्वागत है!
मैं आपको ऐसी गतिविधियाँ सुझा सकता हूँ जो आप घर पर अपने बच्चों के साथ कर सकते हैं। यहां कुछ उदाहरण दिए गए हैं कि आप क्या पूछ सकते हैं:

उदाहरण:
- मैं आपकी रसोई में सब्जियों का उपयोग करके अपने बच्चे के साथ कौन सी गतिविधि कर सकता हूँ?
- सुझाव दीजिए कि मैं अपने बच्चे की घरेलू गतिविधियों में रुचि कैसे पैदा कर सकता हूँ
- मेरा बच्चा पौष्टिक खाना नहीं खाता, क्या करूं?

आप जो चाहते हो वो मुझसे पूछ सकते हैं। आप टाइप कर सकते हैं या बोल सकते हैं।
""" 
    }
    
}

loader_msg_mapping = {
    "en": "Please wait, crafting response. It might take upto a minute.",
    "hi": "कृपया प्रतीक्षा करें, प्रतिक्रिया तैयार कर रहा हूँ। इसमें एक मिनट तक लग सकता है."
}

async def send_message_to_bot(chat_id, text, context: CallbackContext, parse_mode="Markdown", ) -> None:
    """Send a message  to bot"""
    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user_name = update.message.chat.first_name
    logger.info({"id": update.effective_chat.id, "username": user_name, "category": "logged_in", "label": "logged_in"})
    await send_message_to_bot(update.effective_chat.id, f"Namaste 🙏\nWelcome to *My Jaadui Pitara*", context)
    await relay_handler(update, context)


async def relay_handler(update: Update, context: CallbackContext):
    # setting engine manually
    language = context.user_data.get('language')

    if language is None:
        await language_handler(update, context)
    else:
        await bot_handler(update, context)


async def language_handler(update: Update, context: CallbackContext):
    inline_keyboard_buttons = [
        [InlineKeyboardButton('English', callback_data='lang_en')],
        [InlineKeyboardButton('বাংলা', callback_data='lang_bn')],
        [InlineKeyboardButton('ગુજરાતી', callback_data='lang_gu')],
        [InlineKeyboardButton('हिंदी', callback_data='lang_hi')],
        [InlineKeyboardButton('ಕನ್ನಡ', callback_data='lang_kn')],
        [InlineKeyboardButton('മലയാളം', callback_data='lang_ml')],
        [InlineKeyboardButton('मराठी', callback_data='lang_mr')], 
        [InlineKeyboardButton('ଓଡ଼ିଆ', callback_data='or')],
        [InlineKeyboardButton('ਪੰਜਾਬੀ', callback_data='lang_pa')],
        [InlineKeyboardButton('தமிழ்', callback_data='lang_ta')],
        [InlineKeyboardButton('తెలుగు', callback_data='lang_te')]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard_buttons)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="\nPlease select a Language to proceed", reply_markup=reply_markup)


async def preferred_language_callback(update: Update, context: CallbackContext):
    callback_query = update.callback_query
    preferred_language = callback_query.data.lstrip('lang_')
    context.user_data['language'] = preferred_language
    logger.info(
        {"id": update.effective_chat.id, "username": update.effective_chat.first_name, "category": "language_selection",
         "label": "engine_selection", "value": preferred_language})
    await bot_handler(update, context)
    # return query_handler

async def bot_handler(update: Update, context: CallbackContext):
    language = context.user_data.get('language') or 'en'
    button_labels = get_lang_mapping(language, lang_bot_name_mapping)
    inline_keyboard_buttons = [
        [InlineKeyboardButton(button_labels["story"], callback_data='botname_story')],
        [InlineKeyboardButton(button_labels["teacher"], callback_data='botname_teacher')],
        [InlineKeyboardButton(button_labels["parent"], callback_data='botname_parent')]]    
    reply_markup = InlineKeyboardMarkup(inline_keyboard_buttons)  
    text_message = get_lang_mapping(language, language_msg_mapping)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_message, reply_markup=reply_markup, parse_mode="Markdown")

async def preferred_bot_callback(update: Update, context: CallbackContext):
    language = context.user_data.get('language') or 'en'
    callback_query = update.callback_query
    preferred_bot = callback_query.data[len("botname_"):]
    context.user_data['botname'] = preferred_bot
    text_msg = get_lang_mapping(language, bot_default_msg)[preferred_bot]
    logger.info(
        {"id": update.effective_chat.id, "username": update.effective_chat.first_name, "category": "bot_selection",
         "label": "bot_selection", "value": preferred_bot})
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text= text_msg, parse_mode="Markdown")
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

def get_lang_mapping(language, mapping, default_lang = "en"):
    try:
        return mapping[language]
    except:
        return mapping[default_lang]

class ApiResponse(TypedDict):
    output: any


class ApiError(TypedDict):
    error: Union[str, requests.exceptions.RequestException]

def get_bot_endpoint(botName: str):
    if botName == "story":
        return os.environ["STORY_API_BASE_URL"] + '/v1/query'
    else:
        return os.environ["ACTIVITY_API_BASE_URL"] + '/v1/query'

async def get_query_response(query: str, voice_message_url: str, update: Update, context: CallbackContext) -> Union[
    ApiResponse, ApiError]:
    voice_message_language = context.user_data.get('language') or 'en'
    selected_bot = context.user_data.get('botname') or 'story'
    user_id = update.message.from_user.id
    message_id = update.message.message_id
    url = get_bot_endpoint(selected_bot)
    try:
        reqBody: dict
        if voice_message_url is None:
            reqBody = {
                "input": {
                    "language": voice_message_language,
                    "text": query
                },
                "output": {
                    'format': 'text'
                }
            }
        else:
            reqBody = {
                "input": {
                    "language": voice_message_language,
                    "audio": voice_message_url
                },
                "output": {
                    'format': 'audio'
                }
            }

        if selected_bot != "story":
            reqBody["input"]["audienceType"] = selected_bot
        logger.info(f" API Request Body: {reqBody}")
        headers = {
            "x-source": "telegram",
            "x-request-id": str(message_id),
            "x-device-id": f"d{user_id}",
            "x-consumer-id": str(user_id)

        }
        response = requests.post(url, data=json.dumps(reqBody), headers=headers)
        response.raise_for_status()
        data = response.json()
        requests.session().close()
        response.close()
        return data
    except requests.exceptions.RequestException as e:
        return {'error': e}
    except (KeyError, ValueError):
        return {'error': 'Invalid response received from API'}


async def response_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await query_handler(update, context)


async def query_handler(update: Update, context: CallbackContext):
    voice_message = None
    query = None
    selected_language = context.user_data.get('language') or 'en'
    if update.message.text:
        query = update.message.text
        logger.info(
            {"id": update.effective_chat.id, "username": update.effective_chat.first_name, "category": "query_handler",
             "label": "question", "value": query})
    elif update.message.voice:
        voice_message = update.message.voice

    voice_message_url = None
    if voice_message is not None:
        voice_file = await voice_message.get_file()
        voice_message_url = voice_file.file_path
        logger.info(
            {"id": update.effective_chat.id, "username": update.effective_chat.first_name, "category": "query_handler",
             "label": "voice_question", "value": voice_message_url})
    await context.bot.send_message(chat_id=update.effective_chat.id, text=get_lang_mapping(selected_language, loader_msg_mapping))
    await context.bot.sendChatAction(chat_id=update.effective_chat.id, action="typing")
    await handle_query_response(update, context, query, voice_message_url)
    return query_handler


async def handle_query_response(update: Update, context: CallbackContext, query: str, voice_message_url: str):
    response = await get_query_response(query, voice_message_url, update, context)
    if "error" in response:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                               text='An error has been encountered. Please try again.')
        info_msg = {"id": update.effective_chat.id, "username": update.effective_chat.first_name,
                    "category": "handle_query_response", "label": "question_sent", "value": query}
        logger.info(info_msg)
        merged = dict()
        merged.update(info_msg)
        merged.update(response)
        logger.error(merged)
    else:
        logger.info({"id": update.effective_chat.id, "username": update.effective_chat.first_name,
                     "category": "handle_query_response", "label": "answer_received", "value": query})
        answer = response['output']["text"]
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer, parse_mode="Markdown")
        if response['output']["audio"]:
            audio_output_url = response['output']["audio"]
            audio_request = requests.get(audio_output_url)
            audio_data = audio_request.content
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=audio_data)


def main() -> None:
    logger.info('################################################')
    logger.info('# Telegram bot name %s', botName)
    logger.info('################################################')

    logger.info({"concurrent_updates": concurrent_updates})
    logger.info({"pool_time_out": pool_time_out})
    logger.info({"connection_pool_size": connection_pool_size})

    application = Application.builder().token(os.environ['TELEGRAM_BOT_TOKEN']).pool_timeout(pool_time_out).connection_pool_size(connection_pool_size).concurrent_updates(concurrent_updates).connect_timeout(pool_time_out).read_timeout(pool_time_out).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler('select_language', language_handler))
    application.add_handler(CommandHandler('select_bot', bot_handler))

    application.add_handler(CallbackQueryHandler(preferred_language_callback, pattern=r'lang_\w*'))
    application.add_handler(CallbackQueryHandler(preferred_bot_callback, pattern=r'botname_\w*')) 

    application.add_handler(MessageHandler(filters.TEXT | filters.VOICE, response_handler))

    application.run_polling()


if __name__ == "__main__":
    main()