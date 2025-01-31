from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext
from telegram import Update
import os
import twitter
import viz_berlin
import datetime, pytz
from googletrans import Translator
import logging
import re


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def translate(texts):
    try:
        result = []
        for text in texts:
            text_new = Translator().translate(text, dest="en")
            result.append(text_new)
        return result
    except Exception as e:
        logging.exception(e)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! This is Berlin traffic news. Every day we show the latest news about traffic in Berlin.')


async def news(context: CallbackContext) -> None:
    try:
        latest_news = viz_berlin.get_latest_news()
        english_news = translate(latest_news)
        for obj in english_news:
            text = obj.text
            modified_text = re.sub(r"\n\n\n\n", r"\n", text)
            while len(modified_text) >= 4096:
                split_pos = modified_text.rfind(" ", 0, 4096)  # find space before 4096 symbol
                if split_pos == -1:  # the space didn't find
                    split_pos = 4096
                part = modified_text[:split_pos]
                await context.bot.send_message(chat_id=context.job.chat_id, text=part)
                modified_text = modified_text[split_pos:].lstrip()
            await context.bot.send_message(chat_id=context.job.chat_id, text=modified_text)
    except Exception as e:
        logging.exception(e)


async def tweets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        latest_tweets = twitter.get_latest_tweets(username="VIZ_Berlin")
        if isinstance(latest_tweets, str):
            await context.bot.send_message(chat_id=update.effective_chat.id, text=latest_tweets)
        else:
            english_tweets = translate(latest_tweets)
            for tweet in english_tweets:
                text = tweet.text
                await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        logging.exception(e)


def main():
    application = ApplicationBuilder().token(os.getenv('TOKEN_TELEGRAM')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('tweets', tweets))

    job_queue = application.job_queue
    job_queue.run_daily(news,
                        datetime.time(hour=22, minute=00, tzinfo=pytz.timezone('Europe/Berlin')),
                        name= "news")

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
