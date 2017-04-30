import telebot
from PIL import Image as IMG
import image, db, os

bot = telebot.TeleBot('TOKEN')

def cleanup(files):
    for filename in files:
        os.remove(filename)

@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Hello there!')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Just send me '/play' command! You can reply with a coordinate (A0, for example) to open one more image part, or with the hiding subject's name.")


@bot.message_handler(commands=['play'])
def game(message):
    cnt = 0
    actor_image_p, db_handle, actual_name = db.start_game()
    actor_image = IMG.open(actor_image_p)
    i_mode = image.optimalmode(actor_image.size)
    shatters = image.splitim(actor_image, i_mode)
    back = image.generatebackground(tuple(map(lambda x: x + 30, actor_image.size)), i_mode)
    actor_image.close()
    image.temp(back, message.chat.id)
    fname = str(message.chat.id)
    imobj = open(fname + '.jpg', 'rb')
    a = bot.send_photo(message.chat.id, imobj, reply_markup=telebot.types.ForceReply())
    imobj.close()
    def guess(message):
        nonlocal cnt, a
        if message.text[0].isalpha() and message.text[1].isdigit():
            ins_pos = image.msg_to_pos(message.text, i_mode)
            if ins_pos < len(shatters) and ord(message.text[0].lower()) - 97 < i_mode and ord(message.text[1]) - 48 < i_mode:
                image.addguessed(back, shatters[ins_pos])
                image.temp(back, fname)
                cnt += 1
                tmpd = open(fname + '.jpg', 'rb')
                a = bot.send_photo(message.chat.id, tmpd, reply_markup=telebot.types.ForceReply())
                tmpd.close()
            else:
                a = bot.send_message(message.chat.id, 'Out of range! Use available area only.', reply_markup=telebot.types.ForceReply())
            bot.register_for_reply(a, guess)
        else:
            if message.text.lower() in actual_name.split(','):
                bot.send_message(message.chat.id, 'You won! It took you {} attempts, nice result!'.format(cnt))
                cleanup([fname + '.jpg', actor_image_p])
            else:
                a = bot.send_message(message.chat.id, 'Nope :(', reply_markup=telebot.types.ForceReply())
                cnt += 1
                bot.register_for_reply(a, guess)
    bot.register_for_reply(a, guess)
    if cnt == len(shatters):
        bot.send_message(message.chat.id, 'You`ve Lost.')
        cleanup([fname, vactor_image_p])
        return None

bot.polling()

