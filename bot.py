import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from user_model import User
from transaction_model import Transaction
from utils import API_TOKEN, register_user, add_transaction, users, transactions

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Commands
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    referred_by = context.args[0] if context.args else None
    register_user(user.id, user.username, referred_by)
    update.message.reply_text(f'Welcome {user.username}!')

def show_referrals(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in users:
        user = users[user_id]
        referrals = ', '.join([ref.username for ref in user.referrals])
        update.message.reply_text(f'Your referrals: {referrals}')
    else:
        update.message.reply_text('You are not registered yet!')

def add_balance(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in users:
        try:
            amount = float(context.args[0])
            description = ' '.join(context.args[1:])
            add_transaction(user_id, amount, description)
            update.message.reply_text(f'Added {amount} to your balance.')
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /addbalance <amount> <description>')
    else:
        update.message.reply_text('You are not registered yet!')

def show_balance(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in users:
        user = users[user_id]
        update.message.reply_text(f'Your balance: {user.balance}')
    else:
        update.message.reply_text('You are not registered yet!')

def show_transactions(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in users:
        user_transactions = [t for t in transactions if t.user_id == user_id]
        if user_transactions:
            transaction_list = '\n'.join([f'{t.amount} - {t.description}' for t in user_transactions])
            update.message.reply_text(f'Your transactions:\n{transaction_list}')
        else:
            update.message.reply_text('No transactions found.')
    else:
        update.message.reply_text('You are not registered yet!')

def main() -> None:
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("referrals", show_referrals))
    dispatcher.add_handler(CommandHandler("addbalance", add_balance))
    dispatcher.add_handler(CommandHandler("balance", show_balance))
    dispatcher.add_handler(CommandHandler("transactions", show_transactions))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
