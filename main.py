from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import os
import twitter
import viz_berlin
import datetime, pytz
from googletrans import Translator
import logging


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


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await context.job_queue.run_daily(tweets,
#                                       datetime.time(hour=8, minute=00, tzinfo=pytz.timezone('Europe/Berlin')),
#                                       data=update.message.chat_id)


async def website_with_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        latest_news = viz_berlin.get_latest_news()
        english_news = translate(latest_news)
        for obj in english_news:
            text = obj.text
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
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
    tweets_handler = CommandHandler('tweets', tweets)
    application.add_handler(tweets_handler)
    news_handler = CommandHandler('news', website_with_news)
    application.add_handler(news_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
