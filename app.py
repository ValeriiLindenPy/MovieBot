from aiogram import Bot, Dispatcher, executor, types
import sqlite3
import emoji
import os
from dotenv import load_dotenv

load_dotenv()

#Connect to the SQLite3 database
conn = sqlite3.connect('filmsdb.db')
cursor = conn.cursor()




def get_random_film() -> dict:
    """Retrieve a random film from the database."""
    cursor.execute("SELECT * FROM films ORDER BY RANDOM() LIMIT 1;")
    film = cursor.fetchone()
    if film:
        # Map the fields to a dictionary for easier access
        film_data = {
            'title': film[0],
            'description': film[1],
            'rating': film[2],
            'genre': film[3],
            'runtime': film[4],
            'year': film[5],
            'image': film[6]
        }
        return film_data
    return None


bot = Bot(os.environ.get('TOKEN_BOT'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    film = get_random_film()
    title = film['title']
    image = film['image']
    description = film['description']
    rating = film['rating']
    genre = film['genre']
    runtime = film['runtime']
    year = film['year']
    emj = emoji.emojize(":film_frames:")
    post = f"""{emj} <b>{title}</b>\n<i>{genre}</i>\n\n{description}\n\n<b>Year:</b> {year}\n<b>Imdb:</b> {rating}\n<b>Runtime:</b> {runtime}
    """
    await bot.send_photo(message.chat.id, image, caption=post,  parse_mode="HTML")


# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
