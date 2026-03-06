import logging
from aiogram import Bot, Dispatcher, executor, types

TOKEN = "8732129393:AAFF9LrmeAw-1v0pr_XxsCwUghcJs5mkvzE"
OWNER_ID = 8407619610  # твой Telegram ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# главное меню
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📦 Компилировать JNI")
    kb.add("🎮 Компилировать PWN")
    return kb


# меню NDK
def ndk_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("ndk-r25c", "ndk-r21e", "ndk-r16b")
    return kb


# команда старт
@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    if message.from_user.id == OWNER_ID:
        text = (
            "👑 Привет, Администратор!\n\n"
            "Ты владелец бота.\n\n"
            "📊 Лимиты компиляций\n"
            "🟢 Статус: Доступно\n"
            "📈 Использовано: 0/5"
        )
    else:
        text = (
            "👋 Привет!\n"
            "Ты в лучшем компиляторе JNI.\n\n"
            "📊 Лимиты компиляций\n"
            "🟢 Статус: Доступно\n"
            "📈 Использовано: 0/5\n\n"
            "📦 Отправь архив с JNI чтобы начать."
        )

    await message.answer(text, reply_markup=main_menu())


@dp.message_handler(lambda message: message.text == "📦 Компилировать JNI")
async def jni(message: types.Message):

    text = (
        "Теперь выбери NDK для твоего JNI:\n\n"
        "🔹 Новый — ndk-r25c\n"
        "🔹 Средний — ndk-r21e\n"
        "🔹 Старый — ndk-r16b"
    )

    await message.answer(text, reply_markup=ndk_menu())


@dp.message_handler(lambda message: message.text in ["ndk-r25c","ndk-r21e","ndk-r16b"])
async def ndk(message: types.Message):

    await message.answer(
        f"✅ Выбран {message.text}\n\n"
        "📦 Теперь отправь архив (.zip или .7z) с JNI."
    )


@dp.message_handler(lambda message: message.text == "🎮 Компилировать PWN")
async def pwn(message: types.Message):

    text = (
        "🎮 Компиляция Pawn (SA-MP)\n\n"
        "📦 Отправь .pwn файл или архив\n"
        "Я скомпилирую и отправлю .amx"
    )

    await message.answer(text)


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def file_handler(message: types.Message):

    if message.from_user.id == OWNER_ID:
        await message.answer("👑 Файл получил владелец бота.")
    else:
        await message.answer("📥 Файл получен. Начинаю компиляцию...")


if __name__ == "__main__":
    executor.start_polling(dp)