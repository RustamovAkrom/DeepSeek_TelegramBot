# DeepSeek Telegram Bot  
AI-powered multi-language chatbot built with **Aiogram 3**, **DeepSeek API**, and **OpenRouter**.  
Supports model switching, smart history, per-user configuration, and clean modular architecture.

---

## 🚀 Features

### 🧠 **AI Chat Powered by DeepSeek**
- Supports multiple DeepSeek models  
- Each user can select their own model  
- Smart chat history with automatic trimming  
- Configurable system prompt  
- Fast async requests through OpenRouter

<!-- ### 🌍 **Full i18n (EN / RU / UZ)**
- Smart language detection  
- Language selection menu  
- JSON-based translation system  
- Auto fallback to English -->

### 👤 **Per-user Settings**
- Selected model
- Language
- Custom API key (optional)
- All saved in meta-JSON in DB

### 🗂 **Powerful Architecture**
- Clean project structure  
- Modular handlers  
- CRUD layer for DB operations  
- Service layer for business logic  
- SQLAlchemy + Async engine  

---

## 📁 Project Structure

```

app/
├─ handlers/
│   ├─ help.py
│   ├─ models.py
│   ├─ language_change.py
│   └─ chat.py
├─ services/
│   ├─ ai_service.py
│   └─ user_service.py
├─ crud/
│   ├─ users.py
│   └─ history.py
├─ models/
│   ├─ users.py
│   └─ ai_history.py
├─ db/
│   ├─ base.py
│   └─ session.py
├─ run.py
└─ config.py

````

---

## ⚙️ Installation

### 1️⃣ Clone project
```bash
git clone https://github.com/RustamovAkrom/DeepSeek_TelegramBot.git
cd DeepSeek_TelegramBot
````

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create `.env`

**You can get your api keys from this resources and set into .env file:**
 - DEEPSEEK_API_KEY -> https://openrouter.ai/ **AI token**
 - TELEGRAM_BOT_TOKEN -> https://t.me/BotFather **Telegram bot token**
 - ADMIN_IDS -> https://t.me/TgramUserIDBot **Your telegram ID**
 - 
```bash
DEEPSEEK_API_KEY=DEEPSEEK_API_KEY 
TELEGRAM_BOT_TOKEN=TELEGRAM_BOT_TOKEN
ADMIN_IDS=6572863564
ENV=dev # dev or prod
DATABASE_URL=DATABASE_URL # production database 
TEST_DATABASE_URL=sqlite+aiosqlite:///./test.db # development database and for testing

```

---

## ▶️ Run bot

```bash
python run.py
```

---

## 🧩 Main Commands

| Command     | Description             |
| ----------- | ----------------------- |
| `/start`    | Start bot and init user |
| `/help`     | Show help message       |
| `/models`   | Choose AI model         |
| `/admin`    | Manage users            |
| `/models`   | Change model DeepSeek   |
| `/profile`  | User profile            |
| text        | Simply chat with the AI |

---

<!-- ## 🌐 Multi-language Example

User selects language:
✔ English → "Available commands"
✔ Русский → "Доступные команды"
✔ O‘zbekcha → "Mavjud buyruqlar"

Everything works automatically through `i18n.t(lang, key)`. -->

---

## 🤝 Contributing

Pull requests and improvements are welcome!
Feel free to open issues or suggest features.

---

## ⭐️ Support

If this bot helped you — leave a star ⭐️ in the repository!
Your support motivates me to continue improving it 💙

---

## 📜 License

MIT — free for personal and commercial use.
