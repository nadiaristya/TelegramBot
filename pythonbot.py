import telebot
import datetime
import os
import pymongo
from bson.objectid import ObjectId   


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['TBot']
mycol = mydb["tugas"]

api = '1392786808:AAHITh8aOulxPOhbwRqDL7PNN-kHV64W3AI'
bot = telebot.TeleBot(api)

times = datetime.datetime.now()


def get_id(filen):
    user = mycol.find_one({"file_name": filen})
    return (user['_id'])

def find_id(ids):
    cari = mycol.find_one({"_id": ObjectId(ids)})
    return (cari)

def get_filename(filen):
    user = mycol.find_one({"file_name": filen})
    checker = 0
    if (user == None):
        checker = 0
    else:
        checker = 1
    return (checker)

def upload_file(df, file_names):

    with open(file_names, 'wb') as new_file:
        new_file.write(df)
    print('file downloaded')

def inject_mongo(firstn, file_names, chattype, roomname):
    full_path = os.path.realpath(__file__)
    path = os.path.dirname(full_path)
    path_file = os.path.join(path, file_names)
    mydict = { "first_name": firstn , "file_name": file_names, "times": times , "path_file": path_file, "status": chattype, "room_name": roomname }
    mycol.insert_one(mydict)
    print('file inserted')

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'hai {} {}'.format(message.from_user.first_name, message.from_user.last_name))

@bot.message_handler(content_types=['document'])
def mengumpulkan(message):
    print('start proccessing')
    file_names = message.document.file_name
    firstn = message.from_user.first_name
    file_ids = bot.get_file(message.document.file_id)
    df = bot.download_file(file_ids.file_path)
    upload_file(df, file_names)
    roomname = message.chat.title
    chattype = message.chat.type
    checker = get_filename(file_names)
    inject_mongo(firstn, file_names, chattype, roomname)
    id_submit = get_id(file_names)
    bot.reply_to(message,'Terimakasih {}, file {} terkirim pada {} dengan identitas file {} (PENTING).'.format(firstn, file_names, times, id_submit)) if checker == 0 else bot.reply_to(message,'Terimakasih {}, file {} telah terupdate pada {} dengan identitas {} (PENTING)'.format(firstn, file_names, times, id_submit))

@bot.message_handler(commands=['check'])
def check(message):
    try:
        texts= message.text.split(' ')
        ids= texts[1]
        cari = find_id(ids)
        bot.reply_to(message,'file {} telah tersimpan dalam database pada tanggal {}.'.format(cari["file_name"], cari["times"]))
    except:
        bot.reply_to(message, 'Tolong masukkan identitas file anda.')


print('bot running')
bot.polling()
