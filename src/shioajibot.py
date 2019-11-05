import hashlib
import logging
import json
import shioaji as sj
from shioaji.constant import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle


with open("user.json") as json_file:
    user = json.load(json_file)

USERID = user["id"]
PASSWORD = user["password"]
API_TOKEN = user["api_token"]

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
api = sj.Shioaji()
api.login(USERID, PASSWORD)
api.activate_ca(f"C:/ekey/551/{user['id']}/SinoPac.pfx", user["id"], user["id"])


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp="(^cat[s]?$|puss)")
async def cats(message: types.Message):
    with open("data/cats.jpg", "rb") as photo:
        """
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        """

        await message.reply_photo(photo, caption="Cats are here 😺")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    """
    DEBUG:aiogram:Response for getUpdates: [200] "'{"ok":true,"result":[]}'"
    DEBUG:aiogram:Make request: "getUpdates" with data: "{'offset': 691492579, 'timeout': 20}" and files "None"
    DEBUG:aiogram:Response for getUpdates: [200] "'{"ok":true,"result":[{"update_id":691492579,\n"message":{"message_id":414,"from":{"id":199738660,"is_bot":false,"first_name":"\\u751f\\u9b5a\\u7247","username":"ypochien","language_code":"zh-hans"},"chat":{"id":199738660,"first_name":"\\u751f\\u9b5a\\u7247","username":"ypochien","type":"private"},"date":1567478856,"text":"3338,b,1"}}]}'"
    DEBUG:aiogram.dispatcher.dispatcher:Received 1 updates.
    DEBUG:aiogram:Make request: "sendMessage" with data: "{'chat_id': 199738660, 'text': '3338,b,1'}" and files "None"
    DEBUG:aiogram:Make request: "getUpdates" with data: "{'offset': 691492580, 'timeout': 20}" and files "None"
    DEBUG:aiogram:Response for sendMessage: [200] "'{"ok":true,"result":{"message_id":415,"from":{"id":243077419,"is_bot":true,"first_name":"ypochien Bot","username":"ypochienbot"},"chat":{"id":199738660,"first_name":"\\u751f\\u9b5a\\u7247","username":"ypochien","type":"private"},"date":1567478857,"text":"3338,b,1"}}'"
    INFO:aiogram.dispatcher.dispatcher:Stop polling...
    """

    """
    {"message_id": 417, "from": {"id": 199738660, "is_bot": false, "first_name": "生魚片", "username": "ypochien", "language_code": "zh-hans"}, "chat": {"id": 199738660, "first_name": "生魚片", "username": "ypochien", "type": "private"}, "date": 1567478996, "text": "3338,b,1"}
    """
    rtn = message.text
    if message["from"]["username"] == "ypochien" and message["text"][0:2] == "ha":
        _, code, bs, price,qty,first = message["text"].split(",")
        contract = api.Contracts.Stocks[code]
        if price == 0:
            price_type=STOCK_PRICE_TYPE_LIMITDOWN if bs == "s" else STOCK_PRICE_TYPE_LIMITUP
        else :
            price_type=STOCK_PRICE_TYPE_LIMITPRICE
        sample_order = api.Order(
            price= price,
            first_sell=STOCK_FIRST_SELL_NO if first==0 else STOCK_FIRST_SELL_YES,
            quantity=qty,
            action=ACTION_SELL if bs == "s" else ACTION_BUY,
            price_type=price_type,
            order_type=STOCK_ORDER_TYPE_COMMON,
        )
        rtn = api.place_order(contract, sample_order)

    # await message.reply(message.text, reply=False)
    await message.reply(rtn, reply=False)


"""
#@dp.inline_handler()
#async def inline_echo(inline_query: InlineQuery):

    text = inline_query.query or "echo"
    input_content = InputTextMessageContent(text)
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    item = InlineQueryResultArticle(id=result_id, title=f"Result {text!r}", input_message_content=input_content)
    # don't forget to set cache_time=1 for testing (default is 300s or 5m)
    await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
"""

if __name__ == "__main__":

    executor.start_polling(dp, skip_updates=True)
