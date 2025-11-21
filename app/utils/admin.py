from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.users import CRUDUser


async def safe_edit_message(msg: Message, text: str, reply_markup=None):
    try:
        old_text = msg.text
        old_kb = msg.reply_markup.model_dump() if msg.reply_markup else None
        new_kb = reply_markup.model_dump() if reply_markup else None

        if old_text == text and old_kb == new_kb:
            return  # ничего не менять

        await msg.edit_text(text, reply_markup=reply_markup)

    except Exception as e:
        if "message is not modified" not in str(e):
            raise e


async def admin_users_page(cb: CallbackQuery, page: int = 0):
    limit = 10

    async with AsyncSession() as session:
        total_users = await CRUDUser.count_users(session)  # добавить метод count_users
        users = await CRUDUser.list_users(session, limit=limit, offset=page*limit)

    if not users:
        await safe_edit_message(cb.message, "Users not found.", reply_markup=None)
        return

    total_pages = (total_users - 1) // limit + 1

    text = "\n".join(
        [f"{u.tg_id} — @{u.username or '-'} — {u.first_name or ''} {u.last_name or ''}" for u in users]
    )

    user_buttons = [
        [InlineKeyboardButton(text=f"{u.tg_id} @{u.username or '-'}", callback_data=f"admin:user:view:{u.tg_id}")]
        for u in users
    ]

    # Навигация
    nav_buttons = []

    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="◀️ Prev", callback_data=f"admin:users:{page-1}"))

    nav_buttons.append(InlineKeyboardButton(text="🔙 Menu", callback_data="admin:menu"))

    if page + 1 < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="Next ▶️", callback_data=f"admin:users:{page+1}"))

    keyboard = InlineKeyboardMarkup(inline_keyboard=user_buttons + [nav_buttons])

    await safe_edit_message(
        cb.message,
        f"📋 Список пользователей (страница {page+1}/{total_pages}):\n\n{text}",
        reply_markup=keyboard
    )
    await cb.answer()
