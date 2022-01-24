## imports
import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name,  URL
import requests
from requests.exceptions import HTTPError



global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)



## application and routes

app = Flask(__name__)



@app.route('/' , methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True),bot)
    print("123")
    chat_id = update.message.chat_id
    msg_id = update.message.message_id
    
    text = update.message.text.encode('utf-8').decode()
    print('got text message: ', text)
    
    if text == "/start":
        bot_welcome = '''
        welcome to our first bot , we are using weather api from xxx to send you weather every day
        please enter city name to get weather info
        '''
        
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,reply_to_message_id = msg_id)
        
    else:

        try:
            text = re.sub(r'\W','_',text)
            url = "https://goweather.herokuapp.com/weather/{}".format(text)
            response = requests.get(url)
            response.raise_for_status()
            # access JSOn content
            jsonResponse = response.json()
            day1temp = jsonResponse['forecast'][0]['temperature']
            day2temp = jsonResponse['forecast'][1]['temperature'] 
            day3temp = jsonResponse['forecast'][2]['temperature']

            text = '''
            Day 1 Temp: {}
            Day 2 Temp: {}
            Day 3 Temp: {}            
            '''.format(day1temp,day2temp,day3temp) if day1temp != '' else "no city with this name"
   
            
            bot.sendMessage(chat_id=chat_id, text=text,reply_to_message_id = msg_id)
            
            


        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')    
            
        
    return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}'.format(URL=URL))
    if s:
        return 'webhook is ok'
    else:
        return 'webhook setup failed'
    
    


@app.route('/')
def index():
    return 'app is running'


if __name__=="__main__":
    app.run(threaded=True)