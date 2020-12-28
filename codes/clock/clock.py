from datetime import datetime
from getpass import getpass
from instabot import Bot
from os import system
from PIL import Image, ImageDraw, ImageFont
from time import sleep
import pytz
import sys


def bot_instantiate(user_name, user_password):
    # Initialize
    bot = Bot()
    bot.login(username=user_name, password=user_password)
    return bot


def cycles(user_name, user_password, font_type):
    # Ticking Main Process
    timer()
    current_time = str(datetime.now(pytz.timezone('Asia/Tokyo')).time())
    dial_time = current_time[0] + current_time[1],\
        current_time[3] + current_time[4]
    dial_imager(dial_time, font_type)
    post_interface(user_name, user_password)


def dial_imager(time, font_type):
    # This function tells dial_developer what image to develop.
    dial_developer(" : ", "2", 1080, 1080, 300, 30, font_type, 1000)
    for dial_order, dial_time in enumerate(time):
        dial_developer(dial_time, dial_order, 1080, 1080, 130, 30, font_type, 1000)


def dial_developer(text, name, size_x, size_y, coord_x, coord_y, font_type, font_size):
    # Depended by dial_imager
    # This function saves some lines and literally develop specified image.
    new_dial = Image.new("RGB", (size_x, size_y), "black")
    inking = ImageDraw.Draw(new_dial)
    fnt = ImageFont.truetype(font_type, font_size)
    inking.text((coord_x, coord_y), text, font=fnt)
    new_dial.save(str(name) + ".jpg")


def post_interface(user_name, user_password):
    # Refreshing posts by delete and add
    my_bot = bot_instantiate(user_name, user_password)
    medias = my_bot.get_total_user_medias(my_bot.user_id)
    my_bot.delete_medias(medias)
    my_bot.upload_photo("1.jpg", caption = "#minutes")
    my_bot.upload_photo("2.jpg", caption = "ticking...")
    my_bot.upload_photo("0.jpg", caption = "#hours")


def shut_down(user_name, user_password, font_type):
    # Shut Down Procedure
    for i in range(3):
        system(f"rm {i}.jpg.REMOVE_ME")
    my_bot = bot_instantiate(user_name, user_password)
    medias = my_bot.get_total_user_medias(my_bot.user_id)
    my_bot.delete_medias(medias)
    dial_developer("BOT\nOFFLINE\n:'(", 0, 1080, 1080, 10, -30, font_type, 400)
    my_bot.upload_photo("0.jpg", caption = "Sorry ,,,")
    system("rm -r config 0.jpg.REMOVE_ME")
    sys.exit()


def timer():
    # Implementing Refresh Rate
    while True:
        current_tick = str(datetime.now(pytz.timezone('Asia/Tokyo')).time())
        current_seconds = current_tick[6] + current_tick[7]
        current_minutes = current_tick[4]
        if ((current_minutes == '0') and (current_seconds == '00')) or ((current_minutes == '5') and (current_seconds == '00')):
            break
        sleep(1)


try:
    USER_NAME = input("USER NAME: ")
    USER_PASSWORD = getpass("PASSWORD: ")
    FONT_TYPE = "DearSunshine.otf"
    while True:
        cycles(USER_NAME, USER_PASSWORD, FONT_TYPE)
except KeyboardInterrupt:
    shut_down(USER_NAME, USER_PASSWORD, FONT_TYPE)
