from aiogram import Bot, Dispatcher, executor, types
import emoji
import os
from dotenv import load_dotenv
from utils import *


load_dotenv()


bot = Bot(os.environ.get('TOKEN_BOT'))
dp = Dispatcher(bot)
base_keyboard_buttons = ['Get a random movie', 'Select a movie by year','Select a movie by genre', 'Donate']
base_keyboard = set_keyboards(base_keyboard_buttons, 'inline')

  
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  user = message.from_user.first_name
  image = open('cinema.jpeg', 'rb')
  greeting = f"Welcome {user}! This is a free movie random adviser\n Let's go?"
  button_list = ["Let's go", "help", "Donate"]
  keyboard = set_keyboards(button_list, 'reply')
  await bot.send_photo(message.chat.id, image, caption=greeting, reply_markup=keyboard)
   
    
@dp.message_handler(text="Let's go")
async def start(message: types.Message):
  await bot.send_message(message.chat.id, "Ok, let's start!", reply_markup=base_keyboard)
  
@dp.message_handler(text="help")
async def start(message: types.Message):
    emj = emoji.emojize(':red_question_mark:')
    await bot.send_message(message.chat.id, f"{emj} This is a free movie random adviser. Choose options to filter your search and get a random movie for your search.\n Let's go?", reply_markup=base_keyboard)
    
  
@dp.message_handler(text="Donate")
async def donate(message: types.Message):
    await bot.send_invoice(message.chat.id, 'Donation payment', 'Help us to pay for internet provider and services improvement) \n Donation payment for MovieBot supporting', 'Donation invoice',os.environ.get('PAY_TOKEN'), 'USD', [types.LabeledPrice('Donation payment', 2 * 100)])
    
  
@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def donate(message: types.Message):
  await message.answer(f'Successful payment has been done! Thank you very much for your support)')
  
       
@dp.callback_query_handler(text = ['Action','Adventure', 'Horror', 'Sci-Fi','Comedy', 'Drama', 'Musical', 'Short', 'Biography', 'Romance','Crime', 'Mystery', 'Thriller'])
async def get_random_movie_by_genre(call: types.CallbackQuery):
  genre_list = ['Action','Adventure', 'Horror', 'Sci-Fi','Comedy', 'Drama', 'Musical', 'Short', 'Biography', 'Romance','Crime', 'Mystery', 'Thriller']
  for genre in genre_list:
    if call.data == genre:
      film = get_random_film(f"WHERE genre LIKE '%{genre}%'")
      post, image = create_post(film)
      await bot.send_photo(call.message.chat.id, image, caption=post, parse_mode="HTML", reply_markup=base_keyboard)
      

@dp.callback_query_handler(text = base_keyboard_buttons)
async def get_random_movie(call: types.CallbackQuery):
  if call.data == 'Select a movie by genre':
    button_list = ['Action','Adventure', 'Horror', 'Sci-Fi','Comedy', 'Drama', 'Musical', 'Short', 'Biography', 'Romance','Crime', 'Mystery', 'Thriller']
    keyboard = set_keyboards(button_list, 'inline', rows=3)
    await call.message.answer('Choose genre?', reply_markup=keyboard)
  if call.data == 'Get a random movie':
    film = get_random_film()
    post, image = create_post(film)
    await bot.send_photo(call.message.chat.id, image, caption=post, parse_mode="HTML" , reply_markup=base_keyboard)
  if call.data == 'Select a movie by year':
    button_list = ['20th', '21st']
    keyboard = set_keyboards(button_list, 'inline')
    await call.message.answer('What century?', reply_markup=keyboard)
  if call.data == 'Donate':
    await bot.send_message(call.message.chat.id, "Sorry, we are working on it!", reply_markup=base_keyboard)

 
@dp.callback_query_handler(text = ['20th', '21st', '1st half', '2nd half', 'Another from 1st half', 'Another from 2nd half', 'Another one from 21st century'])
async def get_random_movie_for_century(call: types.CallbackQuery):
  if call.data == '21st':
    film = get_random_film("WHERE year >= 2000")
    post, image = create_post(film)
    button_list = ['Get a random movie', 'Select a movie by year', 'Another one from 21st century']
    keyboard = set_keyboards(button_list, 'inline')
    await bot.send_photo(call.message.chat.id, image, caption=post, parse_mode="HTML", reply_markup=keyboard)
  if call.data == 'Another one from 21st century':
    film = get_random_film("WHERE year >= 2000")
    post, image = create_post(film)
    button_list = ['Get a random movie', 'Select a movie by year', 'Another one from 21st century']
    keyboard = set_keyboards(button_list, 'inline')
    await bot.send_photo(call.message.chat.id, image, caption=post, parse_mode="HTML", reply_markup=keyboard) 
  if call.data == '20th':
    button_list = ['1st half', '2nd half']
    keyboard = set_keyboards(button_list, 'inline')
    await call.message.answer('What half of the 20th century?', reply_markup=keyboard)
  if call.data == '1st half':  
    film = get_random_film("WHERE year BETWEEN '1900' AND '1950'")
    post, image = create_post(film)
    button_list = ['Get a random movie', 'Select a movie by year', 'Another from 1st half']
    keyboard = set_keyboards(button_list, 'inline')
    await bot.send_photo(call.message.chat.id, image, caption=post, parse_mode="HTML", reply_markup=keyboard)
  if call.data == '2nd half':  
    film = get_random_film("WHERE year BETWEEN '1950' AND '2000'")
    post, image = create_post(film)
    button_list = ['Get a random movie', 'Select a movie by year', 'Another from 2nd half']
    keyboard = set_keyboards(button_list, 'inline')
    await bot.send_photo(call.message.chat.id, image, caption=post, parse_mode="HTML", reply_markup=keyboard)
  if call.data == 'Another from 1st half':
    film = get_random_film("WHERE year BETWEEN '1900' AND '1950'")
    post, image = create_post(film)
    button_list = ['Get a random movie', 'Select a movie by year', 'Another from 1st half']
    keyboard = set_keyboards(button_list, 'inline')
    await bot.send_photo(call.message.chat.id, image, caption=post, parse_mode="HTML", reply_markup=keyboard)
  if call.data == 'Another from 2nd half':
    film = get_random_film("WHERE year BETWEEN '1950' AND '2000'")
    post, image = create_post(film)
    button_list = ['Get a random movie', 'Select a movie by year', 'Another from 2nd half']
    keyboard = set_keyboards(button_list, 'inline')
    await bot.send_photo(call.message.chat.id, image, caption=post, parse_mode="HTML", reply_markup=keyboard)   
    

# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
