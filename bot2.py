import telepot
import sys
import time
import random
import datetime
import numpy as np
import matplotlib.pyplot as plt
import logging
from sympy import symbols, solve
from sympy import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import BotTokenCode


logging.basicConfig(filename='log.txt', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def fsolve(equation):
    x = symbols('x')
    s = f"sol = solve({equation})\n" \
        f"sv.solved = sol"
    exec(s)


class Saver:
    def __init__(self):
        self.t = np.linspace(0, 2, 20)
        self.chatId = 0
        self.chatLevel = 0
        self.grid = False
        self.solved = None
        self.lastmsg = None
        return


def handle(msg):
    if sv.chatId == 0:
        chat_id = msg['chat']['id']
        sv.chatId = chat_id
    else:
        chat_id = sv.chatId
    command = msg['text']

    logger.info(command)
    # print(f'Got command: %s {command}')
    if sv.chatLevel == 0:
        if command == '/start':

            s = """
                Hi, I'm a math Bot. :)
menu : 
    /solve
    /plot
    /show
    /clear
    /grid
    /help
"""
            bot.sendMessage(chat_id, s)
        elif command == '/show':
            bot.sendMessage(chat_id, "pls wait ...")
            plt.savefig(f'plot{chat_id}.png', dpi=300, bbox_inches='tight')
            bot.sendPhoto(chat_id, photo=open(f'plot{chat_id}.png', 'rb'))
            bot.sendMessage(chat_id, "Done!  /show /clear /grid /help")
        elif command == '/clear':
            plt.clf()
            bot.sendMessage(chat_id, "Done!  /menu /help")
        elif command == '/yes':
            bot.sendMessage(chat_id, "Ok! pls wait ...")
            plt.clf()
            plot(sv.lastmsg)
            plt.savefig(f'plot{chat_id}.png', dpi=300, bbox_inches='tight')
            bot.sendPhoto(chat_id, photo=open(f'plot{chat_id}.png', 'rb'))
            bot.sendMessage(chat_id, "Done!  /grid /menu")
        elif command == '/plot':
            s = """
Use the following command to draw a diagram:
    plot(" f(x) ")
Use the following command to set the diagram limits:
    limit(A , B , C) 
>> A is START point and B is END point
>> C is NUMBER_OF_NODES
Use the following commands to view or clear previous charts:
    /show , /clear
Send /help for help about imported libraries.
"""
            bot.sendMessage(chat_id, s)
        elif command == '/menu':
            s = """
            menu : 
    /solve
    /plot
    /show
    /clear
    /grid
    /help
            """
            bot.sendMessage(chat_id, s)
        elif command == '/solve':
            sv.chatLevel = 1
            s = """
            Done! Enter your Equation by x :
in this format << f(x) = 0 >>
            """
            bot.sendMessage(chat_id, s)
        elif command == '/grid':
            if not sv.grid:
                plt.grid(True)
                sv.grid = True
            else:
                plt.grid(False)
                sv.grid = False

            bot.sendMessage(chat_id, "Done!  /show /clear /grid /help")
        elif command == '/help':
            s = """
import sys
import time
import random
import datetime
import numpy as np
import matplotlib.pyplot as plt
                """
            bot.sendMessage(chat_id, s)
        else:
            x = sv.t
            exec(command)
            bot.sendMessage(chat_id, "Done!  /show /clear /grid /help")
    elif sv.chatLevel == 1:
        print(command)
        fsolve(command)
        bot.sendMessage(chat_id, f"Solved! {len(sv.solved)} answers were obtained: ")
        for i in sv.solved:
            bot.sendMessage(chat_id, f"    {N(i)}")
        sv.lastmsg = command
        bot.sendMessage(chat_id, f"Done! are you interested to plot this equation?\n   1)/yes\n   2)no,back me to /menu")
        sv.chatLevel = 0
def plot(text):
    x = sv.t
    s = f"plt.plot(x,{text})"
    exec(s)


def limit(a, b, c):
    sv.t = np.linspace(a, b, c)


bot = telepot.Bot(BotTokenCode.BOT_TOCKEN_CODE)

sv = Saver()
bot.message_loop(handle)
print('I am listening ...')

while 1:
    time.sleep(10)
