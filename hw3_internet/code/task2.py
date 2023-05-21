import sys
import time
import datetime
import os
import requests
import io
from dotenv import load_dotenv


chat_id = None  # write your telegram chat_id

def telegram_logger(chat_id):
    def decorator(func):
        def inner_func():
            func_name = func.__name__
            load_dotenv()
            token = os.getenv("TG_API_TOKEN")

            try:
                buffer = io.StringIO()
                buffer.name = func_name + '.log'
                sys.stdout = buffer
                sys.stderr = buffer
                start_work = datetime.datetime.now()
                func()
                end_work = datetime.datetime.now()
                
                working_time = end_work - start_work
                status_info = f'Function <code>{func_name}</code> successfully finished in <code>{working_time}</code>'
                
            except Exception as ex:
                status_info = f'Function <code>{func_name}</code> failed with an exception:\n\n<code>{type(ex).__name__}: {ex}</code>'
                
            buffer.seek(0)
            requests.post(f'https://api.telegram.org/bot{token}/sendDocument', 
                              data={'chat_id': chat_id}, files={'document': buffer})
            requests.post(f'https://api.telegram.org/bot{token}/sendMessage',
                              data={'chat_id': chat_id, 'text': status_info, 'parse_mode': 'HTML'})

        return inner_func
    return decorator


@telegram_logger(chat_id)
def good_function():
    print("This goes to stdout")
    print("And this goes to stderr", file=sys.stderr)
    time.sleep(2)
    print("Wake up, Neo")

@telegram_logger(chat_id)
def bad_function():
    print("Some text to stdout")
    time.sleep(2)
    print("Some text to stderr", file=sys.stderr)
    raise RuntimeError("Ooops, exception here!")
    print("This text follows exception and should not appear in logs")
    
@telegram_logger(chat_id)
def long_lasting_function():
    time.sleep(1000)


good_function()

try:
    bad_function()
except Exception:
    pass

long_lasting_function()

