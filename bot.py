import telegram
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler,CallbackQueryHandler
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import pyupbit

from config import api_key,Access_key,Secret_key


bot = telegram.Bot(token = api_key)
upbit = pyupbit.Upbit(Access_key, Secret_key)

def start(update, context):       
    bot.sendMessage(chat_id =update.effective_chat.id,text='Test') 

def UpbitGUI_buttons(update, context):
    task_buttons = [[
        InlineKeyboardButton( '잔고 확인', callback_data=1 )
        ,InlineKeyboardButton( '수익률 확인', callback_data=2 )
    ], [
        InlineKeyboardButton( '3.취소', callback_data=3 )
    ]]
    
    reply_markup = InlineKeyboardMarkup(task_buttons)
    
    context.bot.send_message(
        chat_id=update.message.chat_id
        , text='작업을 선택해주세요!'
        , reply_markup=reply_markup
    ) 
    
def callback_button(update, context):
    query = update.callback_query
    data = query.data
    name1= query.message.chat.first_name
    name2= query.message.chat.last_name
    
        
    context.bot.send_chat_action(
        chat_id=update.effective_user.id
        , action=ChatAction.TYPING
    )
    
    if data=='1':
        
        price=int(upbit.get_balance(ticker="KRW"))
        
        print(price)
        context.bot.edit_message_text(
            text=f'{name1} {name2}님의 잔고\n\n{price} 원'
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
    else:
        context.bot.edit_message_text(
            text='{price}원'
            , chat_id=query.message.chat_id
            , message_id=query.message.message_id
        )
                
def handler(update, context):
    user_text = update.message.text 
    print(update.effective_chat.id)
    
    if user_text.split()[0]=='안녕':
        bot.send_message(chat_id=update.effective_chat.id, text=f"뭘봐")
        
        
if __name__ == "__main__":
    
    updater = Updater(token=api_key, use_context=True)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start',start)
    upbitGUI_handler = CommandHandler('upbit', UpbitGUI_buttons)
    callback_handler = CallbackQueryHandler(callback_button)  
    
    echo_handler = MessageHandler(Filters.text,handler)
      
 
    dispatcher.add_handler(upbitGUI_handler)
    dispatcher.add_handler(callback_handler)
    dispatcher.add_handler(start_handler)
    
    dispatcher.add_handler(echo_handler)

    updater.start_polling() 
	