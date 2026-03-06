import logging
import os
import subprocess
from aiogram import Bot, Dispatcher, executor, types

# ======= Настройки =======
TOKEN = "8732129393:AAFF9LrmeAw-1v0pr_XxsCwUghcJs5mkvzE"
OWNER_ID = 8407619610  # твой Telegram ID, число без кавычек

# ======= Логирование =======
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# ======= Меню =======
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("📦 Компилировать JNI", "🎮 Компилировать PWN")
    return kb

def ndk_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("ndk-r25c", "ndk-r21e", "ndk-r16b")
    return kb

# ======= Команда старт =======
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id == OWNER_ID:
        text = (
            "👑 Привет, Администратор!\n"
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

# ======= Компиляция JNI =======
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
async def ndk_select(message: types.Message):
    await message.answer(
        f"✅ Выбран {message.text}\n\n"
        "📦 Теперь отправь архив (.zip или .7z) с JNI."
    )

# ======= Компиляция PWN =======
@dp.message_handler(lambda message: message.text == "🎮 Компилировать PWN")
async def pwn(message: types.Message):
    text = (
        "🎮 Компиляция Pawn (SA-MP)\n\n"
        "📦 Отправь .pwn файл или архив\n"
        "Я скомпилирую и отправлю .amx"
    )
    await message.answer(text)

# ======= Обработка файлов =======
@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def file_handler(message: types.Message):
    # Создаем папки, если их нет
    os.makedirs("files", exist_ok=True)
    os.makedirs("jni_build", exist_ok=True)

    # Сохраняем файл
    file_path = f"files/{message.document.file_name}"
    await message.document.download(destination_file=file_path)
    await message.answer("⚙️ Файл получен. Начинаю компиляцию...")

    # ======= PWN =======
    if file_path.endswith(".pwn"):
        output = file_path.replace(".pwn", ".amx")
        # Запуск компилятора pawncc (он должен быть в папке с bot.py и иметь права +x)
        subprocess.run(["./pawncc", file_path, f"-o{output}"])
        if os.path.exists(output):
            await message.answer_document(open(output, "rb"))
        else:
            await message.answer("❌ Ошибка компиляции PWN")

    # ======= JNI =======
    elif file_path.endswith(".zip") or file_path.endswith(".7z"):
        # Распаковка архива
        subprocess.run(["unzip", "-o", file_path, "-d", "jni_build"])
        # Сборка через ndk-build (NDK должен быть установлен)
        result = subprocess.run(["ndk-build"], cwd="jni_build")
        if result.returncode == 0:
            await message.answer("✅ JNI скомпилирован!")
        else:
            await message.answer("❌ Ошибка компиляции JNI")

    else:
        await message.answer("❌ Неподдерживаемый формат файла!")

# ======= Админ панель =======
@dp.message_handler(commands=["admin"])
async def admin_panel(message: types.Message):
    if message.from_user.id != OWNER_ID:
        return
    await message.answer("👑 Панель администратора")

# ======= Запуск бота =======
if __name__ == "__main__":
    executor.start_polling(dp)г