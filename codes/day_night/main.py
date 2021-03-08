from astropy.time import Time
from datetime import datetime
from getpass import getpass
from instabot import Bot
from os import system
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from time import sleep, time
import astropy.coordinates as coord
import astropy.units as u
import sys


def bot_instantiate(user_name, user_password):
    bot = Bot()
    bot.login(username=user_name, password=user_password)
    return bot


def cycles(user_name, user_password):
    day_night = terminator()
    for order, image in enumerate(image_split(day_night)):
        image.save(f"{order}.jpg")
    post_interface(user_name, user_password)
    system("rm -r config")
    timer()


def dial_developer(text, name, size_x, size_y, coord_x, coord_y, font_type, font_size):
    new_dial = Image.new("RGB", (size_x, size_y), "black")
    inking = ImageDraw.Draw(new_dial)
    fnt = ImageFont.truetype(font_type, font_size)
    inking.text((coord_x, coord_y), text, font=fnt)
    new_dial.save(f"{name}.jpg")


def post_interface(user_name, user_password):
    my_bot = bot_instantiate(user_name, user_password)
    medias = my_bot.get_total_user_medias(my_bot.user_id)
    my_bot.delete_medias(medias)
    for i in range(-17, 1):
        my_bot.upload_photo(f"{-i}.jpg")
        system(f"rm {-i}.jpg.REMOVE_ME")


def getTerm():
    # tz = astropy.time.TimezoneInfo(15*u.min)
    # gT = str(datetime.now())
    # time = datetime.datetime(int())
    current_time = Time.now()
    sun = coord.get_sun(current_time)
    longitudes = (i for i in range(-180, 181))
    latitudes = [i for i in range(-90, 91)]
    latitudes.reverse()
    coordinates = ((x, y) for x in longitudes for y in latitudes)
    terminator_pixels = []
    north_pole_sun_checker, north_pole_sun = True, True
    for coordinate in coordinates:
        loc = coord.EarthLocation(lon=coordinate[0] * u.deg, lat=coordinate[1] * u.deg)
        altaz = coord.AltAz(location=loc, obstime=current_time)
        solar_altitude = sun.transform_to(altaz).alt
        int_solar_altitude = int(str(solar_altitude).split('d')[0])
        double_solar_altitude = int(str(solar_altitude).split('m')[0].split('d')[1])
        if ((int_solar_altitude == 0) and (double_solar_altitude <= 3)) or ((int_solar_altitude == -0) and (double_solar_altitude <= 3)):
            pixel_Y = int((-coordinate[1] + 91)*11.0718)
            terminator_pixels.append(int((coordinate[0] + 181)*11.1025))
            terminator_pixels.append(pixel_Y)
        if (north_pole_sun_checker):
            if int_solar_altitude > 0:
                north_pole_sun = False
            north_pole_sun_checker = False
    connecting_point = terminator_pixels[1]
    terminator_pixels.append(4008)
    terminator_pixels.append(connecting_point)
    if north_pole_sun:
        for i in (connecting_point,0,0,0,0,4008):
            terminator_pixels.insert(0, i)
    else:
        for i in (connecting_point,0,2004,0,2004,4008):
            terminator_pixels.insert(0, i)
    print(terminator_pixels)
    return terminator_pixels


def image_split(image):
    image = image.rotate(-90, expand=True)
    area = 668
    for y in range(6):
        for x in range(3):
            e_x, e_y = (x*area), (y*area)
            yield image.crop((e_x, e_y, area + e_x, area + e_y))


def shut_down(user_name, user_password, font_type):
    # Shut Down Procedure
    for i in range(17, -1):
        system(f"rm {-i}.jpg.REMOVE_ME")
    my_bot = bot_instantiate(user_name, user_password)
    medias = my_bot.get_total_user_medias(my_bot.user_id)
    my_bot.delete_medias(medias)
    dial_developer("BOT\nOFFLINE\n:'(", 0, 1080, 1080, 10, -30, font_type, 400)
    my_bot.upload_photo("0.jpg", caption = "Sorry ,,,")
    system("rm -r config 0.jpg.REMOVE_ME")
    sys.exit()


def terminator():
    terminator = getTerm()
    land = Image.open("land.png")
    night = Image.open("night.png")
    day_night = land.copy()
    mask_night = Image.new("L", night.size, 0)
    draw = ImageDraw.Draw(mask_night)
    draw.polygon(terminator, fill=255)
    mask_night = mask_night.filter(ImageFilter.GaussianBlur(73.4))
    day_night.paste(night, (0, 0), mask_night)
    day_night.rotate(-90, expand=True)
    # day_night.save("day_night.png", quality=95)
    return day_night


def timer():
    while True:
        current_tick = str(datetime.now().time())
        current_seconds = current_tick[6] + current_tick[7]
        current_minutes = current_tick[3] + current_tick[4]
        if (current_minutes == '00') and (current_seconds == '00'):
            break
        sleep(1)


try:
    USER_NAME = input("USER NAME: ")
    USER_PASSWORD = getpass("PASSWORD: ")
    FONT_TYPE = "DearSunshine.otf"
    while True:
        cycles(USER_NAME, USER_PASSWORD)
except KeyboardInterrupt:
    shut_down(USER_NAME, USER_PASSWORD, FONT_TYPE)