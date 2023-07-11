
import sqlite3
from aiogram import types
import emoji



# Connect to the SQLite3 database
conn = sqlite3.connect('mymovies.db')
cursor = conn.cursor()

def set_keyboards(buttons: list, type: str, rows = 2):
    if type == 'inline':
        ikb = types.InlineKeyboardMarkup(row_width=rows)
        for button_text in buttons:
            ikb.insert(types.InlineKeyboardButton(text=button_text, callback_data=button_text))
        return ikb
    elif type == 'reply':
        ikb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for button_text in buttons:
            ikb.add(button_text)
        return ikb
        
  
def create_post(film_data):
    if film_data:
        title = film_data['title']
        image = film_data['image']
        description = film_data['description']
        rating = film_data['rating']
        genre = film_data['genre']
        runtime = film_data['runtime']
        year = film_data['year']
        emj = emoji.emojize(":film_frames:")
        post = f"""{emj} <b>{title}</b>\n<i>{genre}</i>\n\n{description}\n\n<b>Year:</b> {year}\n<b>Imdb:</b> {rating}\n<b>Runtime:</b> {runtime}"""
        return post, image
    else:
        image = open('cinema.jpeg', 'rb')
        post = 'No data'
        return post, image
  
    
def get_random_film(condition="") -> dict:
    """Retrieve a random film from the database."""
    query = f"SELECT * FROM films {condition} ORDER BY RANDOM() LIMIT 1;"
    cursor.execute(query)
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
