from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext, MessageHandler, filters
from telegram import Update
from dotenv import load_dotenv
import os
import twitter
import viz_berlin
import datetime, pytz
from googletrans import Translator
import logging
import re

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
load_dotenv()


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


async def translate(texts):
    try:
        result = []
        for text in texts:
            text_new = await Translator().translate(text, dest="en")
            result.append(text_new)
        return result
    except Exception as e:
        logging.exception(e)


async def start(update: Update, context: CallbackContext) -> None:
    greetings = 'Hello! This is Berlin traffic news. Every day we show the latest news about traffic in Berlin.'
    await context.bot.send_message(chat_id=os.getenv('CHANNEL_ID'), text=greetings)


async def news(context: CallbackContext) -> None:
    try:
        job = context.job
        latest_news = viz_berlin.get_latest_news()
        english_news = await translate(latest_news)
        for obj in english_news:
            text = obj.text
            modified_text = re.sub(r"\n\n\n\n", r"\n", text)
            while len(modified_text) >= 4096:
                split_pos = modified_text.rfind(" ", 0, 4096)  # find space before 4096 symbol
                if split_pos == -1:  # the space didn't find
                    split_pos = 4096
                part = modified_text[:split_pos]
                await context.bot.send_message(job.chat_id, text=part)
                modified_text = modified_text[split_pos:].lstrip()
            await context.bot.send_message(job.chat_id, text=modified_text)
    except Exception as e:
        logging.exception(e)


async def set_timer(update: Update, context: CallbackContext) -> None:
    context.job_queue.run_daily(
            news,
            datetime.time(hour=22, minute=00, tzinfo=pytz.timezone('Europe/Berlin')),
            chat_id=os.getenv('CHANNEL_ID'),
            name="timer_news")


async def tweets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        latest_tweets = twitter.get_latest_tweets(username="VIZ_Berlin")
        if isinstance(latest_tweets, str):
            await context.bot.send_message(chat_id=os.getenv('CHANNEL_ID'), text=latest_tweets, timeout=600)
        else:
            english_tweets = await translate(latest_tweets)
            for tweet in english_tweets:
                text = tweet.text
                await context.bot.send_message(chat_id=os.getenv('CHANNEL_ID'), text=text, timeout=600)
    except Exception as e:
        logging.exception(e)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main():
    application = ApplicationBuilder().token(os.getenv('TOKEN_TELEGRAM')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('tweets', tweets))
    application.add_handler(CommandHandler('set', set_timer))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling(poll_interval=3600, allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
