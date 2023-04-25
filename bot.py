import requests, time, random, telebot
from telebot import types
from bs4 import BeautifulSoup
from datetime import datetime

Users = []
client = telebot.TeleBot('2035553905:AAGNcIRehfe0aU1oaEX0_hsHaQ8Y2XbHMas')
features = str(open('features.txt', encoding='utf-8').read())
on_working = False;

def nulling(user):
    global Users
    try:
        Users[find_user(user)] = {
            'user_id': user,
            'Rus': [],
            'Cze': [],
            'lekce': 0,
            'counter': 0,
            'attempt': 2,            
            'Ok': '',
            'right_trans': ''
        }
    except:
        return False
    
def get_user_properties(user_id):
    global Users
    print(user_id, Users)
    user_properties = {
        'user_id': Users[find_user(user_id)]['user_id'],
        'Rus': Users[find_user(user_id)]['Rus'],
        'Cze': Users[find_user(user_id)]['Cze'],
        'lekce': Users[find_user(user_id)]['lekce'],
        'counter': Users[find_user(user_id)]['counter'],
        'attempt': Users[find_user(user_id)]['attempt'],            
        'Ok': Users[find_user(user_id)]['Ok'],
        'right_trans': Users[find_user(user_id)]['right_trans']
        }
    return user_properties

def find_user(user_id):
    global Users
    k = 0
    for user_properties in Users:
        if user_properties['user_id'] == user_id:
            return k
        k += 1

def get_words(file, lekce_num, message):
    global Users
    for i in file:
        print(message.from_user.id, find_user(message.from_user.id))
        Users[find_user(message.from_user.id)]['Rus'].append(i.split('–')[1].replace('\n' , ''))
        Users[find_user(message.from_user.id)]['Cze'].append(i.split('–')[0].replace('(F)', '').replace('(M)', '').replace('(N)', '').replace('\n' , ''))   
    print(Users)
        
def call_menu():
    try:
        key = types.InlineKeyboardMarkup(row_width = 1)
        
        dictionary = types.InlineKeyboardButton(text = 'Словарь', callback_data = 'Dictionary')
        choose = types.InlineKeyboardButton(text = 'Выбрать слово', callback_data = 'Choose')
        choose_in_four = types.InlineKeyboardButton(text = 'Выбор из 4х', callback_data = 'Choose_in_four')
        translate_rus = types.InlineKeyboardButton(text = 'Перевести на русский', callback_data = 'translate_rus')
        translate_cze = types.InlineKeyboardButton(text = 'Перевод на чешский', callback_data= 'translate_cze')
        
        key.add(dictionary, choose, choose_in_four, translate_rus, translate_cze)
        return key
    except:
        print(f'Произошла ошибка основного меню. Обратитесь к администрации')
        return
    
def get_image(name):
    try:
        response = requests.get(f'https://www.google.ru/search?q={name}&newwindow=1&sxsrf=AOaemvIwaBbayLkUfD9uhZhF6wK4MADvog:1632900751583&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiS84Cq1aPzAhUOh_0HHTERCN0Q_AUoAXoECAIQAw&cshid=1632900776173221&biw=1856&bih=1004&dpr=1')
        soup = BeautifulSoup(response.text, 'html.parser')
        return str(soup.find_all("img")[2]).split()[3][5:][:-5]
    except:
        print(f'Произошла ошибка поиска изображения. Обратитесь к администрации')
        return

def check_word(message, right_translate):
    try:
        right_trans = right_translate.replace(' ', '').replace('\n', '')
        input_word = message.text.replace(' ', '').replace('\n', '')
        #logs(f'Проверка слова. Правильное слово: {right_trans}. Введенное слово: {input_word}', message.from_user.first_name)
        if (input_word == right_trans):
            return True
        else:
            return False
        
    except:
        client.send_message(message.chat.id, f'Произошла ошибка проверка слова. Обратитесь к администрации')
        return


# выбор из 2х
def choose(call):
    try: 
        global Users
        #user_properties = get_user_properties(call.from_user.id)
        
        if (Users[find_user(call.from_user.id)]['counter']) == len(Users[find_user(call.from_user.id)]['Cze']):
            Users[find_user(call.from_user.id)]['counter'] = 0
            client.send_message(call.message.chat.id, f"Выбери, каким образом будешь изучать слова: \n{features} \nЕсли надоест упраждение, можно ввести команду /start", reply_markup=call_menu())
            return
            
        right_word, worth_word = Users[find_user(call.from_user.id)]['Cze'][Users[find_user(call.from_user.id)]['counter']], Users[find_user(call.from_user.id)]['Cze'][random.randint(0, len(Users[find_user(call.from_user.id)]['Cze'])-1)]
        key = types.InlineKeyboardMarkup()
        if bool(random.randint(0, 1)):
            first_word, second_word = types.InlineKeyboardButton(text = right_word, callback_data='True'), types.InlineKeyboardButton(text = worth_word, callback_data='False')
        else:
            second_word, first_word = types.InlineKeyboardButton(text = right_word, callback_data='True'), types.InlineKeyboardButton(text = worth_word, callback_data='False')
        key.add(first_word, second_word)
        client.send_photo(call.message.chat.id, get_image(Users[find_user(call.from_user.id)]['Rus'][Users[find_user(call.from_user.id)]['counter']]), 
                          caption=f'{Users[find_user(call.from_user.id)]["counter"]+1}. {Users[find_user(call.from_user.id)]["Rus"][Users[find_user(call.from_user.id)]["counter"]]}', reply_markup=key) 
        #logs(f'Прошел цикл игры choose {Counter+1}. Слово: {Rus[Counter]}. Варианты: {right_word}(R), {worth_word}', call.message.from_user.first_name)
    except:
        client.send_message(call.message.chat.id, f'Произошла ошибка выбора из 2-х.')
        return
    
#выбор из 4х
def choose_in_four(call):
    try: 
        global Users
        user_properties = get_user_properties(call.from_user.id)             
        
        if (user_properties['counter']) == len(user_properties['Cze']):
            Users[find_user(call.from_user.id)]['counter'] = 0
            client.send_message(call.message.chat.id, f"Выбери, каким образом будешь изучать слова: {features} \nЕсли надоест упраждение, можно ввести команду /start", reply_markup=call_menu())
            return
        
        key = types.InlineKeyboardMarkup(row_width=2)
        Words = {
            'word_1': user_properties['Rus'][random.randint(0, len(user_properties['Rus'])-1)],
            'word_2': user_properties['Rus'][random.randint(0, len(user_properties['Rus'])-1)],
            'word_3': user_properties['Rus'][random.randint(0, len(user_properties['Rus'])-1)],
            'word_4': user_properties['Rus'][random.randint(0, len(user_properties['Rus'])-1)]
        }
        word_1, word_2, word_3, word_4 = types.InlineKeyboardButton(text = Words['word_1'], callback_data='False'), types.InlineKeyboardButton(text = Words['word_2'], callback_data = 'False'), types.InlineKeyboardButton(
            text = Words['word_3'], callback_data = 'False'), types.InlineKeyboardButton(text = Words['word_4'], callback_data = 'False')    
        position = random.randint(0, 4)
        if position == 0: word_1 = types.InlineKeyboardButton(text = user_properties['Rus'][user_properties['counter']], callback_data='True')
        elif position == 1: word_2 = types.InlineKeyboardButton(text = user_properties['Rus'][user_properties['counter']], callback_data='True')
        elif position == 2: word_3 = types.InlineKeyboardButton(text = user_properties['Rus'][user_properties['counter']], callback_data='True')
        else: Words['word_4'] = word_4 = types.InlineKeyboardButton(text = user_properties['Rus'][user_properties['counter']], callback_data='True')
        key.add(word_1, word_2, word_3, word_4)
        client.send_photo(call.message.chat.id, get_image(user_properties['Rus'][user_properties['counter']]), caption=f'{user_properties["counter"]+1}. {user_properties["Cze"][user_properties["counter"]]}', reply_markup=key)
        #logs(f'Прошел цикл игры choose_in_four {Counter+1}. Слово: {Cze[Counter]}. Варианты: {word_1.text, word_2.text, word_3.text, word_4.text}', call.message.from_user.first_name)
    except:
        client.send_message(call.message.chat.id, f'Произошла ошибка выбора из 4-х. Обратитесь к администрации')
        return
        
def translate_rus(user_id, chat_id):
    try:      
        global Users
        user_properties = get_user_properties(user_id)
        
        if (user_properties['counter']) == len(user_properties['Cze']):
            client.send_message(chat_id, f"Выбери, каким образом будешь изучать слова: \n{features} \nЕсли надоест упраждение, можно ввести команду /start", reply_markup=call_menu())
            Users[find_user(user_id)]['counter'] = 0
            return False
        
        Users[find_user(user_id)]['right_trans'] = user_properties['Rus'][user_properties['counter']]
        client.send_photo(chat_id, get_image(user_properties['Rus'][user_properties['counter']]), caption=f'{user_properties["counter"]+1}. {user_properties["Cze"][user_properties["counter"]]}')
        #logs(f'Прошел цикл игры translate_rus {Counter+1}. Слово: {right_trans}. Попыток: {attempt}', message.from_user.first_name)
    except:
        client.send_message(chat_id, f'Произошла ошибка перевода на русский.')
        return
    
def translate_cze(user_id, chat_id):
    try: 
        global Users
        user_properties = get_user_properties(user_id)
        
        if (user_properties['counter']) == len(user_properties['Cze']):
            client.send_message(chat_id, f"Выбери, каким образом будешь изучать слова: \n{features} \nЕсли надоест упраждение, можно ввести команду /start", reply_markup=call_menu())
            Users[find_user(user_id)]['counter'] = 0
            return False
        
        Users[find_user(user_id)]['right_trans'] = user_properties['Cze'][user_properties['counter']]
        client.send_photo(chat_id, get_image(user_properties['Rus'][user_properties['counter']]), caption=f'{user_properties["counter"]+1}. {user_properties["Rus"][user_properties["counter"]]}')
        #logs(f'Прошел цикл игры translate_cze {Counter+1}. Слово: {right_trans}. Попытка: {attempt}', message.from_user.first_name)
    except:
        client.send_message(chat_id, f'Произошла ошибка с переводом на чешском. Обратитесь к администрации')
        return

@client.message_handler(commands=['start'])
def on_start(message):
    global on_working
    on_working = False;
    user_properties = {
        'user_id': message.from_user.id,
        'Rus': [],
        'Cze': [],
        'lekce': 0,
        'counter': 0,
        'attempt': 2,
        'Ok': '',
        'right_trans': ''
    }
    Users.append(user_properties)
    
    client.send_message(message.chat.id, "Привет! Введи номер лекции, слова которой ты хочешь изучить, через команду /lekce! Пример: /lekce 1. \nТакже можешь посмотреть грамматику: /gramatika")
    
@client.message_handler(commands=['translate-cze'])
def on_translate_cze(message):
    try:
        word = message.text.replace('/translate-cze ', '')
        print(word)
        response = requests.get(f'https://slovnik.seznam.cz/preklad/rusky_cesky/{word}')
        soup = BeautifulSoup(response.text, 'html.parser')    
        answ = str(soup.find_all("a")[3])[156:].replace('</a>', '')
        client.send_message(message.chat.id, answ)
    except: pass;

@client.message_handler(commands=['lekce'])
def on_lekce(message):
    try:
        nulling(message.from_user.id)
        Users[find_user(message.from_user.id)]['lekce'] = N = message.text.replace('/lekce ', '')
        try:
            file = open(f'lekci/lekce {N}.txt', encoding="utf8").readlines()
        except:
            client.send_message(message.chat.id, 'Данной лекции не существует!')        
            return
        random.shuffle(file)
        print(file, N, message.from_user.id)
        get_words(file, N, message)
        client.send_message(message.chat.id, 
                            f"Выбери, каким образом будешь изучать слова: \n{features} \nЕсли надоест упраждение, можно ввести команду /start",
                            reply_markup=call_menu()
                            )
    except:
        client.send_message(message.chat.id, 'Ошибка вывода лекции! Либо вы забыли ввести команду /start, либо данной лекции не существует!')
        return
    
@client.message_handler(commands=['gramatika'])
def gramatika(message):
    try:
        key = types.InlineKeyboardMarkup(row_width=1)
        
        l_1 = types.InlineKeyboardButton(text = 'Vzory Substaniv', callback_data='gram_1')
        l_2 = types.InlineKeyboardButton(text = 'Posesivní Zájmena', callback_data='gram_2')
        l_3 = types.InlineKeyboardButton(text = 'Přechylování Rodů', callback_data='gram_3')
        l_4 = types.InlineKeyboardButton(text = 'Prézens imperfektivních sloves', callback_data='gram_4')
        l_5 = types.InlineKeyboardButton(text = 'NOMINATIV PLURÁLU -mužský rod životný', callback_data='gram_5')
        l_6 = types.InlineKeyboardButton(text = 'NOMINATIV PLURÁLU mužský rod neživotný a ženský rod', callback_data='gram_6')
        l_7 = types.InlineKeyboardButton(text = 'NOMINATIV PLURÁLU střední rod', callback_data='gram_7')
        l_8 = types.InlineKeyboardButton(text = 'AKUZATIV SINGULÁRU mužský rod životný', callback_data='gram_8')
        l_9 = types.InlineKeyboardButton(text = 'AKUZATIV SINGULÁRU ženský rod', callback_data='gram_9')
        l_10 = types.InlineKeyboardButton(text = 'OSOBNÍ ZÁJMENA V AKUZATIVU', callback_data='gram_10')
        l_11 = types.InlineKeyboardButton(text = 'VOKATIV', callback_data='gram_11')


        key.add(l_1, l_2, l_3, l_4, l_5, l_6, l_7, l_8, l_9, l_10, l_11)
        client.send_message(message.chat.id, 'Выберите тему для изучения: ', reply_markup=key)
        #logs('Ввел комманду /gramatika', message.from_user.first_name)
    except:
        client.send_message(message.chat.id, 'Произошла ошибка граматики')
        
    
    
@client.callback_query_handler(func = lambda call: True)
def handle(call):
    try:
        global Users, on_working
        user_properties = get_user_properties(call.from_user.id)
        
        if call.data == 'True':
            client.send_message(call.message.chat.id, 'Верно! ✅')
            Users[find_user(call.from_user.id)]['counter'] += 1
            if Users[find_user(call.from_user.id)]['Ok'] == 'choose':
                choose(call)
            elif Users[find_user(call.from_user.id)]['Ok'] == 'choose_in_four':
                choose_in_four(call)
                
        if call.data == 'False': 
            client.send_message(call.message.chat.id, 'Не верно!❌')
        
        # словарь
        if call.data == 'Dictionary':
            client.send_message(call.message.chat.id, f'Сейчас будут появляться слова с картинками с интервалом в 3 секунды. \nВсего слов в lekce {user_properties["lekce"]}: {len(user_properties["Cze"])}')
            for i in range(len(user_properties["Cze"])):
                if on_working == True: return;
                img = get_image(user_properties["Rus"][i])
                client.send_photo(call.message.chat.id, 
                                  img, 
                                  caption=f'{i+1}. {user_properties["Cze"][i]}– {user_properties["Rus"][i]}')
                time.sleep(3)
            
            #Users.find_user(call.callback_query.from_user.id)['counter'] = 0
            client.send_message(call.message.chat.id, f"Выбери, каким образом будешь изучать слова: \n{features} \nЕсли надоест упраждение, можно ввести команду /start", reply_markup=call_menu())
            
        # выбор из 2х
        if call.data == 'Choose':
            on_working = True;
            Users[find_user(call.from_user.id)]['Ok'] = 'choose'
            client.send_message(call.message.chat.id, f'Сейчас будут появляться слова на русском языке с картинками. Ваша задача выбрать правильное слово на чешском. \nВсего слов в lekce {Users[find_user(call.from_user.id)]["lekce"]}: {len(Users[find_user(call.from_user.id)]["Cze"])}')
            choose(call)  
            
        # выбор из 4х
        if call.data == 'Choose_in_four':
            Users[find_user(call.from_user.id)]['Ok'] = 'choose_in_four'
            client.send_message(call.message.chat.id, f'Сейчас будут появляться слова на чешском языке с картинками. Ваша задача выбрать правильное слово на русском. \nВсего слов в lekce {user_properties["lekce"]}: {len(user_properties["Cze"])}')
            choose_in_four(call)        
            
        # перевод на русский
        if call.data == 'translate_rus':
            Users[find_user(call.from_user.id)]['Ok'] = 'translate_rus'
            client.send_message(call.message.chat.id, f'Сейчас будут появляться слова на чешском языке с картинками. Ваша задача будет написать на русском. На каждое слово будет дано 2 попытки. \nВсего слов в lekce {user_properties["lekce"]}: {len(user_properties["Cze"])}')
            translate_rus(call.from_user.id, call.message.chat.id)        
            
        # перевод на чешский
        if call.data == 'translate_cze':
            nulling()
            Users[find_user(call.from_user.id)]['Ok'] = 'translate_cze'
            client.send_message(call.message.chat.id, f'Сейчас будут появляться слова на чешском языке с картинками. Ваша задача будет написать на русском. На каждое слово будет дано 2 попытки. \nВсего слов в lekce {user_properties["lekce"]}: {len(user_properties["Cze"])}')
            translate_cze(call.from_user.id, call.message.chat.id)  
            
        if 'gram' in call.data:
            if call.data == 'gram_1': client.send_photo(call.message.chat.id, photo = open('gramatika/Vzory Substantiv.png', 'rb'), caption='Vzory Substantiv')
            if call.data == 'gram_2': client.send_photo(call.message.chat.id, photo = open('gramatika/posesivní zájmena.png', 'rb'), caption='Posesivní Zájmena')
            if call.data == 'gram_3': client.send_photo(call.message.chat.id, photo = open('gramatika/přechylování rodů.png', 'rb'), caption='Přechylování Rodů')
            if call.data == 'gram_4': client.send_photo(call.message.chat.id, photo = open('gramatika/Prézens imperfektivních sloves.png', 'rb'), caption='Prézens imperfektivních sloves')
            if call.data == 'gram_5': client.send_photo(call.message.chat.id, photo = open('gramatika/NOMINATIV PLURÁLU -mužský rod životný.png', 'rb'), caption='NOMINATIV PLURÁLU -mužský rod životný')
            if call.data == 'gram_6': client.send_photo(call.message.chat.id, photo = open('gramatika/NOMINATIV PLURÁLU mužský rod neživotný a ženský rod.png', 'rb'), caption='NOMINATIV PLURÁLU mužský rod neživotný a ženský rod')
            if call.data == 'gram_7': client.send_photo(call.message.chat.id, photo = open('gramatika/NOMINATIV PLURÁLU střední rod.png', 'rb'), caption='NOMINATIV PLURÁLU střední rod')
            if call.data == 'gram_8': client.send_photo(call.message.chat.id, photo = open('gramatika/AKUZATIV SINGULÁRU mužský rod životný.png', 'rb'), caption='AKUZATIV SINGULÁRU mužský rod životný')
            if call.data == 'gram_9': client.send_photo(call.message.chat.id, photo = open('gramatika/AKUZATIV SINGULÁRU ženský rod.png', 'rb'), caption='AKUZATIV SINGULÁRU ženský rod')
            if call.data == 'gram_10': client.send_photo(call.message.chat.id, photo = open('gramatika/OSOBNÍ ZÁJMENA V AKUZATIVU.png', 'rb'), caption='OSOBNÍ ZÁJMENA')
            if call.data == 'gram_11': client.send_photo(call.message.chat.id, photo = open('gramatika/Vokativ.jpg', 'rb'), caption='VOKATIV')
            
    except:
        client.send_message(call.message.chat.id, f'Произошла ошибка нажатия кнопки. Возможно вы забыли /start')
        return
        
@client.message_handler(content_types=['text'])
def get_text(message):
    try:
        global Users
        user_properties = get_user_properties(message.from_user.id)
        
        #logs(f'Введено сообщение: {message.text}', message.from_user.first_name)
        if str(message.from_user.id) == '2035553905': 
            return False;
        
        if user_properties['Ok'] == 'translate_rus':
            if check_word(message, user_properties['right_trans']):
                client.send_message(message.chat.id, 'Верно! ✅')
                Users[find_user(message.from_user.id)]['counter'] += 1
                Users[find_user(message.from_user.id)]['attempt'] = 2
                translate_rus(message.from_user.id, message.chat.id)
            else:
                Users[find_user(message.from_user.id)]['attempt'] -= 1
                if Users[find_user(message.from_user.id)]['attempt'] == 1:
                    client.send_message(message.chat.id, f'Неверно! Попыток осталось: {user_properties["attempt"]-1}')
                else:
                    client.send_message(message.chat.id, f'К сожалению, не верно! Правильное слово было: {user_properties["right_trans"]}❌')
                    Users[find_user(message.from_user.id)]['counter'] += 1
                    Users[find_user(message.from_user.id)]['attempt'] = 2
                    translate_rus(message.from_user.id, message.chat.id)
                    
        if user_properties['Ok'] == 'translate_cze':
            if check_word(message, user_properties['right_trans']):
                client.send_message(message.chat.id, 'Верно! ✅')
                Users[find_user(message.from_user.id)]['counter'] += 1
                Users[find_user(message.from_user.id)]['attempt'] = 2
                translate_cze(message.from_user.id, message.chat.id)
            else:
                Users[find_user(message.from_user.id)]['attempt'] -= 1
                if Users[find_user(message.from_user.id)]['attempt'] == 1:
                    client.send_message(message.chat.id, f'Неверно! Попыток осталось: {user_properties["attempt"]-1}')
                else:
                    client.send_message(message.chat.id, f'К сожалению, не верно! Правильное слово было: {user_properties["right_trans"]}❌')
                    Users[find_user(message.from_user.id)]['counter'] += 1
                    Users[find_user(message.from_user.id)]['attempt'] = 2
                    translate_cze(message.from_user.id, message.chat.id)
                    
                
                
    except:
        client.send_message(message.chat.id, f'Произошла ошибка получения сообщения.')
        return

client.polling()