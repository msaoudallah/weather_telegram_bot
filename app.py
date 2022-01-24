## imports
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,  URL

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)



## application and routes

app = Flask(__name__)



@app.route('/{}'.format(TOKEN) , methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True),bot)
    
    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    
    text = update.message.text.encode('utf-8').decode()
    print('got text message: ', text)
    
    if text == "/start":
        bot_welcome = '''
        welcome to our first bot , we are using weather api from xxx to send you weather every day
        please enter city name to get weather info
        '''
        
        bot.send_message(chat_id=chat_id, text=bot_welcome,reply_to_message_id = msg_id)
        
    else:
        try:
            text = re.sub(r'\W','_',text)
            url = "https://goweather.herokuapp.com/weather/{}".format(text)
            
            bot.send_message(chat_id=chat_id, text=url,reply_to_message_id = msg_id)
        except Exception:
            bot.send_message(chat_id=chat_id, text="there is no city with this name, or service is down", reply_to_message_id= msg_id)
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL))
    if s:
        return 'webhook is ok'
    else:
        return 'webhook setup failed'
    
    


@app.route('/')
def index():
    return 'app is running'


if __name__=="__main__":
    app.run(threaded=True)