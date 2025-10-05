# bot.py
import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

import tempfile
from pathlib import Path

import pdfplumber
from docx import Document

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Put it in .env")

# В aiogram 3.7+ parse_mode передаём через default=DefaultBotProperties(...)
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def extract_text_from_pdf(path: Path) -> str:
    text_parts = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            if txt:
                text_parts.append(txt)
    return "\n".join(text_parts).strip()

def extract_text_from_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs).strip()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! 👋 Я бот для работы с резюме.\n\n"
        "Команды:\n"
        "• /resume — пришли PDF или DOCX, я вытащу текст\n"
        "• /search — покажу 3 заглушки вакансий с кнопками"
    )

@dp.message(Command("resume"))
async def cmd_resume(message: Message):
    await message.answer("Пришли файл резюме (PDF или DOCX) одним документом.")

@dp.message(F.document)
async def handle_document(message: Message):
    doc = message.document
    filename = (doc.file_name or "").lower()

    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        await message.reply("Поддерживаю только .pdf и .docx 🙏")
        return

    # сохраняем во временный файл
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / filename
        await bot.download(doc, destination=path)

        try:
            if filename.endswith(".pdf"):
                text = extract_text_from_pdf(path)
            else:
                text = extract_text_from_docx(path)
        except Exception as e:
            await message.reply(f"Не удалось извлечь текст: {e}")
            return

    if not text:
        await message.reply("Текст не найден (возможно, это скан).")
        return

    # Telegram лимит 4096 — делаем усечённый предпросмотр
    preview = (text[:3500] + "…") if len(text) > 3500 else text
    await message.reply(f"<b>Текст резюме:</b>\n\n{preview}")

@dp.message(Command("search"))
async def cmd_search(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вакансия 1 — Data Analyst", callback_data="vacancy_1")],
        [InlineKeyboardButton(text="Вакансия 2 — Python Dev",   callback_data="vacancy_2")],
        [InlineKeyboardButton(text="Вакансия 3 — AI Engineer",  callback_data="vacancy_3")],
    ])
    await message.answer("Вот примеры вакансий:", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

