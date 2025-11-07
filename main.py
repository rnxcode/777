import sqlite3
import os
import time
import random
import platform
import asyncio
import logging
from datetime import datetime
from colorama import init, Fore, Style
from aiohttp import ClientSession
from pyrogram import Client, filters, idle

# Настройка логирования для подавления ненужных ошибок
logging.getLogger("pyrogram").setLevel(logging.ERROR)

# Инициализация colorama
init(autoreset=True)

class RNXColors:
    RED = Fore.LIGHTRED_EX
    DARK_RED = Fore.RED
    GRAY = Fore.LIGHTBLACK_EX
    WHITE = Fore.LIGHTWHITE_EX
    GREEN = Fore.LIGHTGREEN_EX
    YELLOW = Fore.LIGHTYELLOW_EX
    BOLD = Style.BRIGHT
    DIM = Style.DIM

class JackpotConsole:
    def __init__(self):
        self.typing_speed = 0.02

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def typewriter(self, text, color=RNXColors.WHITE, delay=None):
        if delay is None:
            delay = self.typing_speed
        print(color, end='')
        for ch in text:
            print(ch, end='', flush=True)
            time.sleep(delay)
        print(RNXColors.GRAY, end='\n')

    async def check_telegram_subscription(self):
        os.makedirs('statistics/opened_telegram_channels', exist_ok=True)
        try:
            async with ClientSession() as session:
                async with session.get('http://public-ssh.site/channel_link.txt') as resp:
                    channel_link = (await resp.text()).strip()

            channel_username = channel_link.split('/')[3]
            if channel_username in os.listdir('statistics/opened_telegram_channels'):
                self.typewriter(f"[SUCCESS] Telegram channel already checked", RNXColors.GREEN)
                return True
            else:
                with open(f'statistics/opened_telegram_channels/{channel_username}', 'w') as f:
                    pass

                link = f"https://t.me/{channel_username}"
                if platform.system().lower() == 'windows':
                    os.system(f'start https://t.me/{channel_link.split("/", 3)[3]}')
                elif platform.system().lower() in ('linux', 'darwin'):
                    os.system(f'xdg-open {link}')

                self.typewriter(f"[IMPORTANT] Подпишитесь на канал автора: {link}", RNXColors.YELLOW)
                input(f"\n{RNXColors.GREEN}Нажмите Enter после подписки чтобы продолжить...")
                return True

        except Exception as e:
            self.typewriter(f"[WARNING] Could not check Telegram channel: {str(e)}", RNXColors.DARK_RED)
            return True

    def glitch_logo(self, duration=0.3):
        text = "JACKPOT TRACKER"
        chars = "#$@%&*?!"
        start = time.time()
        while time.time() - start < duration:
            glitched = ''.join(random.choice(chars) if random.random() > 0.7 else c for c in text)
            print(f'\r{RNXColors.DARK_RED}{glitched}', end='', flush=True)
            time.sleep(0.05)
        print('\r' + ' ' * len(text) + '\r', end='')

    def logo(self):
        # Графити стиль
        graffiti = [
            ".--------..--------..--------.",
            "|   __   '|   __   '|   __   '",
            "`--' .  / `--' .  / `--' .  /",
            "    /  /      /  /      /  /",
            "   .  /      .  /      .  /",
            "  /  /      /  /      /  /",
            " `--'      `--'      `--'"
        ]

        for line in graffiti:
            print(RNXColors.RED + RNXColors.BOLD + line)
            time.sleep(0.03)
        print()

        # Основной логотип
        print("\n" + RNXColors.GRAY + "     Telegram Dice Statistics  |  by RNXCODE\n")

    def boot(self):
        self.typewriter("[SYSTEM] Initializing Jackpot Tracker...", RNXColors.WHITE)
        messages = [
            "[OK] Database connection established",
            "[OK] Telegram client configured",
            "[OK] Statistics engine loaded",
            "[OK] Rank system activated",
            "[INFO] Monitoring target chat...",
        ]
        for msg in messages:
            self.typewriter(msg, RNXColors.GRAY, 0.02)
            time.sleep(0.2)
        print()

    def show_status(self):
        """Показать статус системы"""
        self.clear()
        self.logo()

        # Статистика базы данных
        try:
            conn = sqlite3.connect('jackpot_stats.db')
            c = conn.cursor()

            c.execute("SELECT COUNT(*) FROM jackpots")
            total_jackpots = c.fetchone()[0]

            c.execute("SELECT COUNT(*) FROM dice_rolls")
            total_rolls = c.fetchone()[0]

            c.execute("SELECT COUNT(DISTINCT user_id) FROM dice_rolls")
            unique_users = c.fetchone()[0]

            conn.close()

            print(f"\n{RNXColors.WHITE}{RNXColors.BOLD}📊 SYSTEM STATUS:")
            print(f"{RNXColors.GRAY}├─ Total Jackpots: {RNXColors.GREEN}{total_jackpots}")
            print(f"{RNXColors.GRAY}├─ Total Rolls: {RNXColors.YELLOW}{total_rolls}")
            print(f"{RNXColors.GRAY}├─ Unique Users: {RNXColors.WHITE}{unique_users}")
            print(f"{RNXColors.GRAY}└─ Target Chat: {RNXColors.RED}-1002951677798")

        except Exception as e:
            self.typewriter(f"[ERROR] Database error: {e}", RNXColors.DARK_RED)

    async def run_async(self):
        self.clear()
        self.glitch_logo()
        self.logo()
        self.boot()
        await self.check_telegram_subscription()
        self.show_status()

        print(f"\n{RNXColors.GRAY}Press Enter to start monitoring...")
        input()

        # Запуск основного приложения
        self.typewriter("[SYSTEM] Starting Telegram client...", RNXColors.GREEN)
        return True

# Конфигурация API
API_ID = 29604031
API_HASH = "d732b5d2a3ef41de0cb2e615f7818889"
TARGET_CHAT_ID = -1002951677798

# Система рангов
RANKS = {
    0: {"name": "Новичок", "emoji": "🔰", "min_jackpots": 0, "min_rolls": 0},
    1: {"name": "Игрок", "emoji": "🎯", "min_jackpots": 1, "min_rolls": 10},
    2: {"name": "Удачливый", "emoji": "🍀", "min_jackpots": 3, "min_rolls": 30},
    3: {"name": "Эксперт", "emoji": "🎲", "min_jackpots": 10, "min_rolls": 100},
    4: {"name": "Мастер", "emoji": "⭐", "min_jackpots": 25, "min_rolls": 250},
    5: {"name": "Легенда", "emoji": "👑", "min_jackpots": 50, "min_rolls": 500},
    6: {"name": "Бог удачи", "emoji": "🎰", "min_jackpots": 100, "min_rolls": 1000}
}

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('jackpot_stats.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jackpots
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  username TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS dice_rolls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  username TEXT,
                  emoji TEXT,
                  value INTEGER,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

app = Client("777", api_id=API_ID, api_hash=API_HASH)

class JackpotStats:
    def __init__(self):
        self.conn = sqlite3.connect('jackpot_stats.db', check_same_thread=False)

    def log_jackpot(self, user_id: int, username: str):
        """Запись джекпота в базу"""
        c = self.conn.cursor()
        c.execute('''INSERT INTO jackpots (user_id, username) VALUES (?, ?)''',
                  (user_id, username))
        self.conn.commit()

    def log_dice_roll(self, user_id: int, username: str, emoji: str, value: int):
        """Запись броска кубика в базу"""
        c = self.conn.cursor()
        c.execute('''INSERT INTO dice_rolls (user_id, username, emoji, value) VALUES (?, ?, ?, ?)''',
                  (user_id, username, emoji, value))
        self.conn.commit()

    def get_user_rank(self, user_id: int):
        """Определение ранга пользователя"""
        c = self.conn.cursor()

        # Количество джекпотов пользователя
        c.execute("SELECT COUNT(*) FROM jackpots WHERE user_id = ?", (user_id,))
        jackpots = c.fetchone()[0]

        # Количество бросков пользователя
        c.execute("SELECT COUNT(*) FROM dice_rolls WHERE user_id = ?", (user_id,))
        total_rolls = c.fetchone()[0]

        # Определяем ранг
        current_rank = 0
        for rank_id, rank_info in RANKS.items():
            if jackpots >= rank_info["min_jackpots"] and total_rolls >= rank_info["min_rolls"]:
                current_rank = rank_id
            else:
                break

        # Следующий ранг
        next_rank_id = current_rank + 1
        next_rank = RANKS.get(next_rank_id, None)

        # Прогресс до следующего ранга
        if next_rank:
            progress_jackpots = min(100, (jackpots / next_rank["min_jackpots"]) * 100) if next_rank[
                                                                                              "min_jackpots"] > 0 else 100
            progress_rolls = min(100, (total_rolls / next_rank["min_rolls"]) * 100) if next_rank[
                                                                                           "min_rolls"] > 0 else 100
            progress = (progress_jackpots + progress_rolls) / 2
        else:
            progress = 100

        return {
            "current_rank": RANKS[current_rank],
            "next_rank": next_rank,
            "jackpots": jackpots,
            "total_rolls": total_rolls,
            "progress": round(progress, 1)
        }

    def get_leaderboard(self, period: str = "all"):
        """Топ игроков по рангам"""
        c = self.conn.cursor()

        # Определяем временной диапазон
        if period == "today":
            time_filter = "timestamp >= datetime('now', 'start of day')"
        elif period == "week":
            time_filter = "timestamp >= datetime('now', '-7 days')"
        elif period == "month":
            time_filter = "timestamp >= datetime('now', '-30 days')"
        else:
            time_filter = "1=1"

        # Получаем топ игроков по джекпотам
        c.execute(f"""
            SELECT user_id, username, 
                   COUNT(*) as jackpot_count,
                   (SELECT COUNT(*) FROM dice_rolls WHERE user_id = jackpots.user_id) as total_rolls
            FROM jackpots 
            WHERE {time_filter}
            GROUP BY user_id 
            ORDER BY jackpot_count DESC 
            LIMIT 20
        """)
        top_players = []
        for user_id, username, jackpot_count, total_rolls in c.fetchall():
            rank_info = self.get_user_rank(user_id)
            top_players.append({
                "username": username,
                "jackpots": jackpot_count,
                "total_rolls": total_rolls,
                "rank": rank_info["current_rank"]
            })

        return top_players

    def get_stats(self, period: str = "all"):
        """Получение статистики джекпотов"""
        c = self.conn.cursor()

        # Определяем временной диапазон
        if period == "today":
            time_filter = "timestamp >= datetime('now', 'start of day')"
        elif period == "week":
            time_filter = "timestamp >= datetime('now', '-7 days')"
        elif period == "month":
            time_filter = "timestamp >= datetime('now', '-30 days')"
        else:
            time_filter = "1=1"

        # Общее количество джекпотов
        c.execute(f"SELECT COUNT(*) FROM jackpots WHERE {time_filter}")
        total_jackpots = c.fetchone()[0]

        # Уникальные пользователи
        c.execute(f"SELECT COUNT(DISTINCT user_id) FROM jackpots WHERE {time_filter}")
        unique_players = c.fetchone()[0]

        # Топ победителей
        c.execute(f"""
            SELECT username, COUNT(*) as jackpot_count 
            FROM jackpots 
            WHERE {time_filter}
            GROUP BY user_id 
            ORDER BY jackpot_count DESC 
            LIMIT 10
        """)
        top_winners = c.fetchall()

        # Последний джекпот
        c.execute(f"SELECT username, timestamp FROM jackpots ORDER BY timestamp DESC LIMIT 1")
        last_jackpot = c.fetchone()

        return {
            "total_jackpots": total_jackpots,
            "unique_players": unique_players,
            "top_winners": top_winners,
            "last_jackpot": last_jackpot
        }

    def get_dice_stats(self, period: str = "all"):
        """Получение статистики всех бросков"""
        c = self.conn.cursor()

        # Определяем временной диапазон
        if period == "today":
            time_filter = "timestamp >= datetime('now', 'start of day')"
        elif period == "week":
            time_filter = "timestamp >= datetime('now', '-7 days')"
        elif period == "month":
            time_filter = "timestamp >= datetime('now', '-30 days')"
        else:
            time_filter = "1=1"

        # Общее количество бросков
        c.execute(f"SELECT COUNT(*) FROM dice_rolls WHERE {time_filter}")
        total_rolls = c.fetchone()[0]

        # Уникальные пользователи
        c.execute(f"SELECT COUNT(DISTINCT user_id) FROM dice_rolls WHERE {time_filter}")
        unique_players = c.fetchone()[0]

        # Статистика по эмодзи
        c.execute(f"""
            SELECT emoji, COUNT(*) as count, AVG(value) as avg_value
            FROM dice_rolls 
            WHERE {time_filter}
            GROUP BY emoji
            ORDER BY count DESC
        """)
        emoji_stats = c.fetchall()

        # Самый активный игрок
        c.execute(f"""
            SELECT username, COUNT(*) as roll_count
            FROM dice_rolls 
            WHERE {time_filter}
            GROUP BY user_id 
            ORDER BY roll_count DESC 
            LIMIT 1
        """)
        most_active = c.fetchone()

        # Процент джекпотов от всех бросков
        c.execute(f"SELECT COUNT(*) FROM dice_rolls WHERE emoji = '🎰' AND {time_filter}")
        slot_rolls = c.fetchone()[0]
        jackpot_percentage = (self.get_stats(period)['total_jackpots'] / slot_rolls * 100) if slot_rolls > 0 else 0

        return {
            "total_rolls": total_rolls,
            "unique_players": unique_players,
            "emoji_stats": emoji_stats,
            "most_active": most_active,
            "jackpot_percentage": round(jackpot_percentage, 2)
        }

    def get_user_stats(self, user_id: int):
        """Статистика конкретного пользователя"""
        c = self.conn.cursor()

        # Общее количество бросков пользователя
        c.execute("SELECT COUNT(*) FROM dice_rolls WHERE user_id = ?", (user_id,))
        total_rolls = c.fetchone()[0]

        # Количество джекпотов пользователя
        c.execute("SELECT COUNT(*) FROM jackpots WHERE user_id = ?", (user_id,))
        jackpots = c.fetchone()[0]

        # Статистика по эмодзи пользователя
        c.execute("""
            SELECT emoji, COUNT(*) as count, AVG(value) as avg_value
            FROM dice_rolls 
            WHERE user_id = ?
            GROUP BY emoji
            ORDER BY count DESC
        """, (user_id,))
        emoji_stats = c.fetchall()

        # Первый и последний бросок
        c.execute("SELECT timestamp FROM dice_rolls WHERE user_id = ? ORDER BY timestamp ASC LIMIT 1", (user_id,))
        first_roll = c.fetchone()
        c.execute("SELECT timestamp FROM dice_rolls WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", (user_id,))
        last_roll = c.fetchone()

        # Ранг пользователя
        rank_info = self.get_user_rank(user_id)

        return {
            "total_rolls": total_rolls,
            "jackpots": jackpots,
            "emoji_stats": emoji_stats,
            "first_roll": first_roll,
            "last_roll": last_roll,
            "rank_info": rank_info
        }

stats = JackpotStats()

# Фильтр для проверки чата
def target_chat_filter(_, __, message):
    return message.chat.id == TARGET_CHAT_ID

target_chat = filters.create(target_chat_filter)

async def safe_reply(message, text):
    """Безопасная отправка ответа с обработкой ошибок"""
    try:
        await message.reply(text)
    except Exception as e:
        # Игнорируем ошибки связанные с peer_id и другие
        if "Peer id invalid" not in str(e) and "CHAT_WRITE_FORBIDDEN" not in str(e):
            print(f"{RNXColors.DARK_RED}[ERROR] {e}")

@app.on_message(filters.dice & target_chat)
async def dice_handler(client, message):
    try:
        emoji = message.dice.emoji
        value = message.dice.value
        user = message.from_user
        username = user.username or user.first_name

        # Логируем все броски
        stats.log_dice_roll(user.id, username, emoji, value)

        # Только джекпот 777 в слотах
        if emoji == "🎰" and value == 64:
            print(f"{RNXColors.GREEN}[JACKPOT] {username} выиграл джекпот 777!")

            # Логируем джекпот
            stats.log_jackpot(user.id, username)

            # Получаем обновленный ранг и статистику
            rank_info = stats.get_user_rank(user.id)
            user_stats = stats.get_user_stats(user.id)

            response = f"""
🏝️ Оп оп! Джекпот подъехал!

🎰 **Поздравляем {username}!** ❤️

🏆 **Ранг:** {rank_info['current_rank']['emoji']} {rank_info['current_rank']['name']}
📊 **Количество побед:** {user_stats['jackpots']}
🎯 **Всего бросков:** {user_stats['total_rolls']}

💫 **Прогресс до след. ранга:** {rank_info['progress']}%

Напиши @zhirtresina за призом 🎁
"""

            await safe_reply(message, response)
    except Exception as e:
        # Игнорируем все ошибки в обработчике dice
        pass

@app.on_message(filters.command("jackpot_stats") & target_chat)
async def stats_handler(client, message):
    """Статистика джекпотов"""
    try:
        args = message.text.split()
        period = "all"

        if len(args) > 1:
            period = args[1].lower()
            if period not in ["today", "week", "month", "all"]:
                period = "all"

        stats_data = stats.get_stats(period)

        response = f"🎰 **Статистика джекпотов 777** ({period})\n\n"
        response += f"• Всего джекпотов: `{stats_data['total_jackpots']}`\n"
        response += f"• Уникальных победителей: `{stats_data['unique_players']}`\n"

        if stats_data['last_jackpot']:
            last_time = datetime.strptime(stats_data['last_jackpot'][1], '%Y-%m-%d %H:%M:%S')
            response += f"• Последний: {stats_data['last_jackpot'][0]} ({last_time.strftime('%d.%m %H:%M')})\n"

        if stats_data['top_winners']:
            response += "\n**Топ победителей:**\n"
            for i, (username, count) in enumerate(stats_data['top_winners'][:5], 1):
                response += f"{i}. {username}: {count} джекпотов\n"

        await safe_reply(message, response)
    except Exception as e:
        # Игнорируем ошибки
        pass

@app.on_message(filters.command("info") & target_chat)
async def info_handler(client, message):
    """Общая информация о всех бросках"""
    try:
        args = message.text.split()
        period = "all"

        if len(args) > 1:
            period = args[1].lower()
            if period not in ["today", "week", "month", "all"]:
                period = "all"

        dice_stats = stats.get_dice_stats(period)
        jackpot_stats = stats.get_stats(period)

        response = f"📊 **Общая статистика** ({period})\n\n"
        response += f"• Всего бросков: `{dice_stats['total_rolls']}`\n"
        response += f"• Уникальных игроков: `{dice_stats['unique_players']}`\n"
        response += f"• Всего джекпотов: `{jackpot_stats['total_jackpots']}`\n"
        response += f"• Шанс джекпота: `{dice_stats['jackpot_percentage']}%`\n\n"

        if dice_stats['most_active']:
            response += f"• Самый активный: {dice_stats['most_active'][0]} ({dice_stats['most_active'][1]} бросков)\n\n"

        response += "**Статистика по эмодзи:**\n"
        for emoji, count, avg in dice_stats['emoji_stats']:
            response += f"  {emoji}: {count} бросков (ср. {avg:.1f})\n"

        await safe_reply(message, response)
    except Exception as e:
        # Игнорируем ошибки
        pass

@app.on_message(filters.command("ranks") & target_chat)
async def ranks_handler(client, message):
    """Информация о системе рангов"""
    try:
        response = "🎖️ **Система рангов:**\n\n"

        for rank_id, rank_info in RANKS.items():
            response += f"{rank_info['emoji']} **{rank_info['name']}**\n"
            response += f"   Джекпотов: {rank_info['min_jackpots']}+ | Бросков: {rank_info['min_rolls']}+\n\n"

        response += "💡 *Ранг определяется по количеству джекпотов И бросков*"

        await safe_reply(message, response)
    except Exception as e:
        # Игнорируем ошибки
        pass

@app.on_message(filters.command("myrank") & target_chat)
async def myrank_handler(client, message):
    """Показать свой ранг и статистику"""
    try:
        user = message.from_user
        username = user.username or user.first_name

        rank_info = stats.get_user_rank(user.id)
        user_stats = stats.get_user_stats(user.id)

        response = f"""
🎖️ **Ваша статистика** {username}:

🏆 **Текущий ранг:** {rank_info['current_rank']['emoji']} {rank_info['current_rank']['name']}
📊 **Джекпотов:** {user_stats['jackpots']}
🎯 **Всего бросков:** {user_stats['total_rolls']}
"""

        if rank_info['next_rank']:
            response += f"""
📈 **Следующий ранг:** {rank_info['next_rank']['emoji']} {rank_info['next_rank']['name']}
⏳ **Прогресс:** {rank_info['progress']}%

🎰 Нужно джекпотов: {rank_info['next_rank']['min_jackpots']} (ещё {rank_info['next_rank']['min_jackpots'] - user_stats['jackpots']})
🎲 Нужно бросков: {rank_info['next_rank']['min_rolls']} (ещё {rank_info['next_rank']['min_rolls'] - user_stats['total_rolls']})
"""
        else:
            response += "\n🎉 **Вы достигли максимального ранга!** 👑"

        await safe_reply(message, response)
    except Exception as e:
        # Игнорируем ошибки
        pass

@app.on_message(filters.command("top") & target_chat)
async def top_handler(client, message):
    """Топ игроков по рангам"""
    try:
        args = message.text.split()
        period = "all"

        if len(args) > 1:
            period = args[1].lower()
            if period not in ["today", "week", "month", "all"]:
                period = "all"

        leaderboard = stats.get_leaderboard(period)

        response = f"🏆 **Топ игроков** ({period})\n\n"

        for i, player in enumerate(leaderboard[:10], 1):
            response += f"{i}. {player['rank']['emoji']} **{player['username']}**\n"
            response += f"   {player['rank']['name']} | 🎰 {player['jackpots']} | 🎲 {player['total_rolls']}\n\n"

        await safe_reply(message, response)
    except Exception as e:
        # Игнорируем ошибки
        pass

async def main():
    console = JackpotConsole()
    if await console.run_async():
        print(f"{RNXColors.GREEN}[SYSTEM] Starting Telegram client...")
        await app.start()
        print(f"{RNXColors.GREEN}[SYSTEM] Telegram client started successfully!")
        print(f"{RNXColors.GRAY}[SYSTEM] Monitoring chat {TARGET_CHAT_ID}...")
        await idle()
        await app.stop()

if __name__ == "__main__":
    # Создаем новый event loop для избежания конфликтов
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print(f"\n{RNXColors.RED}[SYSTEM] Shutting down...")
    finally:
        loop.close()