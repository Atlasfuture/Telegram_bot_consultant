"""Project main file which contains Telegram API handlers for bot"""

import telebot
import os
from telebot import types
from bot.conversation import Conversation


from quest.questioning import Variant, Question, Questioning
from orm.orm_smartphones import Smartphone, Brand




"""============================CREATING CONVERSATION==============================="""

"""Forming questioning for conversation object"""
os_quest = Question("What mobile OS do you prefer?", Smartphone.os,
                        [
                            Variant("Android"),
                            Variant("iOS"),
                        ])

battery_quest = Question("What kind of battery do you prefer?", Smartphone.battery,
                             [
                                 Variant("Dont care", 0),
                                 Variant("Small battery is enough", 1),
                                 Variant("Good battery", 2),
                                 Variant("Advanced battery", 3)
                             ])

brand_quest = Question("What brand do you prefer?", Brand.name,
                           [
                               Variant("Apple"),
                               Variant("Xiaomi"),
                               Variant("Meizu"),
                               Variant("Samsung")
                           ])

screen_quest = Question("What do you think about screen?", Smartphone.screen,
                            [
                                Variant("Dont care", 0),
                                Variant("Simple screen", 1),
                                Variant("Good screen", 2),
                                Variant("Perfect screen", 3)
                            ])

questioning = Questioning([os_quest, battery_quest, brand_quest, screen_quest])



"""Creating conversation object with questioning initialization"""
conversation = Conversation(questioning)




"""========================HANDLING CONVERSATION VIA TELEBOT========================="""

os.chdir('..')
os.chdir('./config_files')

with open('api_key') as f:
    token = f.readline().strip()

bot = telebot.TeleBot(token)



def reply_keyboard(variants):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in variants])
    return keyboard

def inline_keyboard(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text="Order", callback_data=message)])
    return keyboard



@bot.message_handler(content_types=["text"])
def resend(message):
    conversation.ask(message.text)

    if conversation.current_state() == "conversation":
        bot.send_message(message.chat.id, conversation.response(), reply_markup=types.ReplyKeyboardRemove())
    elif conversation.current_state() == "quest_request":
        quest = conversation.response()
        bot.send_message(message.chat.id, quest["Text"], reply_markup=reply_keyboard(quest["Variants"]))
    elif conversation.current_state() == "questioning":
        quest = conversation.response()
        if isinstance(quest, dict):
            bot.send_message(message.chat.id, quest["Text"], reply_markup=reply_keyboard(quest["Variants"]))
        elif isinstance(quest, list):
            for item in quest:
                if isinstance(item, Smartphone):
                    bot.send_message(message.chat.id, item, reply_markup=inline_keyboard(item.name))
                elif isinstance(item, str):
                    bot.send_message(message.chat.id, item)

    elif conversation.current_state() == "refresh":
        quest = conversation.response()
        bot.send_message(message.chat.id, quest["Text"], reply_markup=reply_keyboard(quest["Variants"]))




@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    conversation.order(c)
    message = conversation.response()
    bot.send_message(c.message.chat.id, message, reply_markup=types.ReplyKeyboardRemove())



if __name__ == '__main__':
    bot.polling(none_stop=True)
