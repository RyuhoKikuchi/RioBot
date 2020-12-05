from instabot import Bot


user_name = input("Enter your username: ")
user_password = input("Enter the password: ")
sentence = input("Enter your caption: ")
bot = Bot()
bot.login(username = user_name, password = user_password)
bot.upload_photo("photo.jpg", caption = sentence)
