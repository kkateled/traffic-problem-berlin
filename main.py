from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import os
import twitter
import viz_berlin
import datetime, pytz
from googletrans import Translator


def translate(texts):
    result = []
    for text in texts:
        text_new = Translator().translate(text, dest="en")
        result.append(text_new)
    return result


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.job_queue.run_daily(tweets,
                                      datetime.time(hour=8, minute=00, tzinfo=pytz.timezone('Europe/Berlin')),
                                      data=update.message.chat_id)


async def website_with_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        latest_news = viz_berlin.get_latest_news()
        english_news = translate(latest_news)
        for text in english_news:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except Exception as e:
        return [f"Error fetching news: {e}"]


async def tweets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        latest_tweets = twitter.get_latest_tweets(username="VIZ_Berlin")
        english_tweets = translate(latest_tweets)
        for tweet in english_tweets:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=tweet)
    except Exception as e:
        return [f"Error fetching tweets: {e}"]


def main():
    application = ApplicationBuilder().token(os.getenv('TOKEN_TELEGRAM')).build()
    tweets_handler = CommandHandler('start', start)
    application.add_handler(tweets_handler)
    website_with_news = CommandHandler('website_with_news', website_with_news)
    application.add_handler(website_with_news)
    application.run_polling()


if __name__ == '__main__':
    main()
