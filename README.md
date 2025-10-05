# HR_test
# Mini Job Bot + Skills API

## 1) Установка
python -m venv .venv && . .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
cp .env.example .env   # вставь реальный BOT_TOKEN

## 2) Запуск бота
python bot.py

## 3) Запуск API
uvicorn api:app --reload --port 8000

## 4) Проверка API
curl -X POST http://127.0.0.1:8000/extract_skills -H "Content-Type: application/json" \
  -d "{\"text\": \"Python, FastAPI, Telegram bots, Docker\"}"


