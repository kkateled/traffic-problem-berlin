from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import os
import twitter
import datetime, pytz


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.job_queue.run_daily(tweets,
                                      datetime.time(hour=8, minute=00, tzinfo=pytz.timezone('Europe/Berlin')),
                                      data=update.message.chat_id)


async def tweets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        latest_tweets = twitter.get_latest_tweets(username="SBahnBerlin")
        english_tweets = twitter.translate(latest_tweets)
        for tweet in english_tweets:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=tweet)
    except Exception as e:
        return [f"Error fetching tweets: {e}"]


def main():
    application = ApplicationBuilder().token(os.getenv('TOKEN_TELEGRAM')).build()
    tweets_handler = CommandHandler('start', start)
    application.add_handler(tweets_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
