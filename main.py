# -*- coding: UTF-8 -*-
from datetime import datetime
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import logging
import pyfiglet
import time
import threading
from threading import Thread
# import telegram_send
import asyncio

from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events

setting_time = 10
nick_name = ''
api_id = '5252543'
api_hash = '4208bed21f587e13ad47e2066377b825'
bot_token = '1722929989:AAEsMgECCa3aNzVJWNS0AkwvwjitHQDJuF0'
# your phone number
phone = '+12363045540'

lock = threading.Lock() # threading에서 Lock 함수 가져오기
start_time = datetime.now()
send_msg = False
send_msg_hour = False
class timeUpdate(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
        self.timeCheck = timeChecker()
        with MouseListener(on_click=self.timeCheck.on_click, on_move=self.timeCheck.on_move,
                           on_scroll=self.timeCheck.on_scroll) as listener:
            with KeyboardListener(on_press=self.timeCheck.on_press) as listener:
                listener.join()

    def check_warning(self):
        global send_msg
        global send_msg_hour
        global start_time
        y = datetime.now()
        z = y - start_time
        # print(z.total_seconds())
        print("spend time : {0} ".format(z))
        if z.total_seconds() > setting_time * 60 and send_msg is False:
            print('warning for time over')
            self.timeCheck.check_users(setting_time)
            send_msg = True

        if z.total_seconds() > 50 * 60 and send_msg_hour is False:
            print('warning for time over')
            self.timeCheck.check_users(50)
            send_msg_hour = True


    def run(self):
        global start_time
        while True:
            lock.acquire()
            print("check start from : {0} ".format(start_time))
            self.check_warning()
            lock.release()
            time.sleep(1)

class timeChecker():

    def __init__(self):
        print("init")
        self.reset_time()

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # creating a telegram session and assigning
        # it to a variable client
        self.client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
        # connecting and building the session
        self.client.connect()

    def __del__(self):
        print('Destructor called')
        # disconnecting the telegram session
        self.loop.close()
        self.client.disconnect()

    def reset_time(self):
        global start_time
        global send_msg
        global send_msg_hour
        lock.acquire()
        start_time = datetime.now()
        send_msg = False
        send_msg_hour = False
        lock.release()

    def on_move(self, x, y):
        # print("mouse moved to ({0},{1})".format(x, y))
        self.print_time_check()
        self.reset_time()

    def on_click(self,x, y, button, pressed):
        if pressed:
            pass
            # print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
        self.print_time_check()
        self.reset_time()

    def on_scroll(self,x, y, dx, dy):
        # print('Mouse scrolled at ({0},{1})({2},{3})'.format(x, y, dx, dy))
        self.print_time_check()
        self.reset_time()

    def on_press(self, key):
        # print("key press ({0})".format(key))
        self.print_time_check()
        self.reset_time()

    def print_time_check(self):
        y = datetime.now()
        z = y - start_time
        # print(z.total_seconds())

    def check_users(self, minute):

        # in case of script ran first time it will
        # ask either to input token or otp sent to
        # number or sent or your telegram id
        # if not self.client.is_user_authorized():
        #     self.client.send_code_request(phone)
        #     # signing in the client
        #     self.client.sign_in(phone, input('Enter the code: '))

        try:
            self.loop.run_until_complete(self.send_msg(self.client, minute))
            # self.loop.close()

        except Exception as e:

            # there may be many error coming in while like peer
            # error, wwrong access_hash, flood_error, etc
            print(e);


    async def send_msg(self, client, minute):

        # get_entity = await client.get_entity(last_name + first_name)
        get_entity = await client.get_entity(nick_name)
        async for user in client.iter_participants(get_entity):
            print(user.id)

        receiver = InputPeerUser(get_entity.id, get_entity.access_hash)

        # sending message using telegram client
        await client.send_message(receiver, str(minute)+"분 이 초과됬습니다.", parse_mode='html')


if __name__ == '__main__':
    print('사용법 : https://t.me/input_check_bot 로 텔레그램에 봇을 추가해주시고 본 프로그램을 실행하시면 됩니다.')
    print('본 프로그램은 사용자 입력정보를 저장하거나 송신하지 않습니다.')
    logo = pyfiglet.figlet_format("e-suck Timer")
    print(logo)
    nick_name = input('텔레그램 사용자명을 입력해주세요(사용자명은 @로 시작하는 영어/숫자 형태의 id입니다. 텔레그램 설정 -> 편집 -> 사용자명 에서 확인): ')
    print('nick name : ' + nick_name)

    time_select = input('알림시간을 설정해주세요: 예)10분 -> 10 입력 , 17분 -> 17 입력')
    print(time_select)
    setting_time = int(time_select)

    timeUpdater = timeUpdate()












