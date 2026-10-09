import sqlite3
import threading
import time
from datetime import datetime
import telebot
import random
import string
import json
import os

BOT_TOKEN = ''

bot = telebot.TeleBot(BOT_TOKEN)
CODES_FILE = 'temp_codes.json'


def generate_binding_code(owner_id):
    codes = {}
    if os.path.exists(CODES_FILE):
        with open(CODES_FILE, 'r') as f:
            codes = json.load(f)

    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    codes[code] = {
        'owner_id': owner_id,
        'expires': time.time() + 300
    }

    with open(CODES_FILE, 'w') as f:
        json.dump(codes, f)

    return code


def check_binding_status(owner_id):
    con = sqlite3.connect('account.db')
    cur = con.cursor()
    cur.execute("SELECT telegram_username FROM telegram_connections WHERE owner_id = ?", (owner_id,))
    res = cur.fetchone()
    con.close()

    if res:
        return True, res[0]
    return False, None


def load_codes():
    if os.path.exists(CODES_FILE):
        with open(CODES_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_codes(codes):
    with open(CODES_FILE, 'w') as f:
        json.dump(codes, f)


def check_code(code):
    codes = load_codes()
    if code in codes:
        if codes[code]['expires'] > time.time():
            return codes[code]['owner_id']
        else:
            del codes[code]
            save_codes(codes)
    return None


def _remove_code(code):
    codes = load_codes()
    if code in codes:
        del codes[code]
        save_codes(codes)


def _setup_database():
    con = sqlite3.connect('account.db')
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS telegram_connections (
            telegram_id TEXT PRIMARY KEY,
            owner_id INTEGER,
            telegram_username TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS task_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            notification_type TEXT
        )
    """)
    con.commit()
    con.close()


@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg,
                 "👋 Привет!\n\nОтправь /code КОД для привязки аккаунта\n\nКод можно получить в приложении, нажав кнопку '📱 Привязать TG'")


@bot.message_handler(commands=['help'])
def help_cmd(msg):
    bot.reply_to(msg,
                 "📚 Команды:\n\n/code КОД - привязать аккаунт\n/unbind - отвязать аккаунт\n/tasks - показать задачи\n/help - справка")


@bot.message_handler(commands=['code'])
def code_cmd(msg):
    try:
        parts = msg.text.split()
        if len(parts) != 2:
            bot.reply_to(msg, "❌ Используй: /code КОД\n\nПример: /code ABC123")
            return
        code = parts[1].upper()
    except:
        bot.reply_to(msg, "❌ Используй: /code КОД")
        return

    owner_id = check_code(code)

    if not owner_id:
        bot.reply_to(msg, "❌ Неверный или просроченный код!\n\nПолучите новый код в приложении.")
        return

    tg_id = str(msg.from_user.id)
    tg_name = msg.from_user.username or msg.from_user.first_name

    con = sqlite3.connect('account.db')
    cur = con.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO telegram_connections (telegram_id, owner_id, telegram_username) VALUES (?, ?, ?)",
        (tg_id, owner_id, tg_name))
    con.commit()
    con.close()

    _remove_code(code)
    bot.reply_to(msg,
                 f"✅ Аккаунт успешно привязан!\n\nTelegram: @{tg_name}\n\nТеперь вы будете получать уведомления о задачах.")


@bot.message_handler(commands=['unbind'])
def unbind(msg):
    tg_id = str(msg.from_user.id)
    con = sqlite3.connect('account.db')
    cur = con.cursor()
    cur.execute("DELETE FROM telegram_connections WHERE telegram_id = ?", (tg_id,))
    con.commit()
    con.close()
    bot.reply_to(msg, "✅ Аккаунт отвязан от Telegram")


@bot.message_handler(commands=['tasks'])
def tasks(msg):
    tg_id = str(msg.from_user.id)
    con = sqlite3.connect('account.db')
    cur = con.cursor()

    cur.execute("SELECT owner_id FROM telegram_connections WHERE telegram_id = ?", (tg_id,))
    res = cur.fetchone()
    if not res:
        bot.reply_to(msg, "❌ Аккаунт не привязан!\n\nИспользуйте /code КОД для привязки")
        con.close()
        return

    owner_id = res[0]
    cur.execute("""
        SELECT Name, priority.title, Time FROM target
        INNER JOIN priority ON target.Priority = priority.id
        WHERE ownerID=? AND Ready=0 AND isDelete=0 AND Time!=''
    """, (owner_id,))
    tasks_list = cur.fetchall()
    con.close()

    if not tasks_list:
        bot.reply_to(msg, "📭 У вас нет активных задач с указанным временем")
        return

    text = "📋 Ваши задачи:\n\n"
    for i, (name, priority, time) in enumerate(tasks_list, 1):
        text += f"{i}. {name}\n   Приоритет: {priority}\n   Дедлайн: {time}\n\n"
    bot.reply_to(msg, text)


def check_deadlines():
    while True:
        now = datetime.now()
        con = sqlite3.connect('account.db')
        cur = con.cursor()

        # Добавляем условие Time != '' и Time IS NOT NULL
        cur.execute("""
            SELECT target.idtarget, target.Name, target.Time, telegram_connections.telegram_id
            FROM target
            LEFT JOIN telegram_connections ON target.ownerID = telegram_connections.owner_id
            WHERE target.Ready=0 AND target.isDelete=0 
            AND target.Time != '' AND target.Time IS NOT NULL
        """)

        for task_id, name, time_str, tg_id in cur.fetchall():
            if not tg_id or not time_str:
                continue

            try:
                task_date = datetime.strptime(time_str, "%d.%m.%Y")
                days = (task_date - now).days

                cur.execute("SELECT id FROM task_notifications WHERE task_id=? AND notification_type=?",
                            (task_id, f"days_{days}"))

                if not cur.fetchone():
                    if days == 3:
                        bot.send_message(tg_id,
                                         f"⚠️ Напоминание!\n\nЗадача '{name}' осталось 3 дня до дедлайна ({time_str})")
                        cur.execute("INSERT INTO task_notifications (task_id, notification_type) VALUES (?, ?)",
                                    (task_id, "days_3"))
                    elif days == 1:
                        bot.send_message(tg_id,
                                         f"🔔 Внимание!\n\nЗадача '{name}' остался 1 день до дедлайна ({time_str})")
                        cur.execute("INSERT INTO task_notifications (task_id, notification_type) VALUES (?, ?)",
                                    (task_id, "days_1"))
                    elif days == 0 and now.hour == 9:
                        bot.send_message(tg_id,
                                         f"⏰ Срочно!\n\nЗадача '{name}' должна быть выполнена сегодня! Дедлайн: {time_str}")
                        cur.execute("INSERT INTO task_notifications (task_id, notification_type) VALUES (?, ?)",
                                    (task_id, "days_0"))
                    con.commit()
            except Exception as e:
                print(f"Ошибка с задачей {task_id}: {e}")
                continue

        con.close()
        time.sleep(3600)


if __name__ == '__main__':
    _setup_database()
    threading.Thread(target=check_deadlines, daemon=True).start()
    print("Telegram бот запущен!")
    bot.infinity_polling()