from datetime import datetime
from instabot import Bot
from os import system
from PIL import Image, ImageDraw
from time import sleep
import sys


def bot_instantiate(user_name, user_password):
    # Initiate
    bot = Bot()
    bot.login(username=user_name, password=user_password)
    return bot


def clock(user_name, user_password):
    # Ticking Main Process
    current_time = str(datetime.now().time())
    dial_time = current_time[0] + current_time[1],\
        current_time[3] + current_time[4]
    dial_imager(dial_time)
    post_interface(user_name, user_password)
    tick_admin()


def dial_imager(time):
    # This function tells dial_developer what image to develop.
    dial_developer(" : ", "2", 8, 8, -4, -3)
    for dial_order, dial_time in enumerate(time):
        dial_developer(dial_time, dial_order, 13, 13, 1, 1)


def dial_developer(text, name, size_x, size_y, coord_x, coord_y):
    # Depended by dial_imager
    # This function saves some lines and literally develop specified image.
    new_dial = Image.new("RGB", (size_x, size_y), "black")
    inking = ImageDraw.Draw(new_dial)
    inking.text((coord_x, coord_y), text)
    new_dial.save(str(name) + ".jpg")


def post_interface(user_name, user_password):
    # Refreshing posts by del and add
    my_bot = bot_instantiate(user_name, user_password)
    medias = my_bot.get_total_user_medias(my_bot.user_id)
    my_bot.delete_medias(medias)
    my_bot.upload_photo("1.jpg", caption="str(datetime.now().time())[3] + \
    str(datetime.now().time())[4] #minutes")
    my_bot.upload_photo("2.jpg", caption="str(datetime.now().time())[2]")
    my_bot.upload_photo("0.jpg", caption="str(datetime.now().time())[0] + \
    str(datetime.now().time())[1] #hours")


def shut_down(user_name, user_password):
    # Shut Down Process
    for i in range(3):
        system(f"rm {i}.jpg.REMOVE_ME")
    my_bot = bot_instantiate(user_name, user_password)
    medias = my_bot.get_total_user_medias(my_bot.user_id)
    my_bot.delete_medias(medias)
    dial_developer("BOT\nOFFLINE", 0, 50, 50, 3, 0)
    my_bot.upload_photo("0.jpg", caption="shut_down()")
    system("rm -r config")
    sys.exit()


def tick_admin():
    # Implementing Refresh Rate
    while True:
        current_tick = str(datetime.now().time())
        current_seconds = current_tick[6] + current_tick[7]
        current_minutes = current_tick[4]
        if ((current_minutes == '0') and (current_seconds == '00')) or ((current_minutes == '5') and (current_seconds == '00')):
            break
        sleep(1)


try:
    user_name = input("USER NAME: ")
    user_password = input("PASSWORD: ")
    tick_admin()
    while True:
        clock(user_name, user_password)
except KeyboardInterrupt:
    shut_down(user_name, user_password)
