from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from config import settings
from app.db.base import AsyncSessionLocal
from app.crud.users import CRUDUser
from app.keyboards.admin import admin_main_kb, admin_user_actions

router = Router()


def is_admin(tg_id: int) -> bool:
    return tg_id in settings.ADMIN_IDS


@router.message(Command("admin"))
async def admin_panel(message: Message):
    if not is_admin(message.from_user.id):
        await message.answer("Access denied!")
        return

    await message.answer("Administrator panel:", reply_markup=admin_main_kb())


@router.callback_query(lambda c: c.data and c.data.startswith("admin:users"))
async def admin_users(cb: CallbackQuery):
    if not is_admin(cb.from_user.id):
        await cb.answer("Access denied!", show_alert=True)
        return
    parts = cb.data.split(":")
    page = int(parts[2]) if len(parts) > 2 else 0
    await admin_users_page(cb, page)


@router.callback_query(lambda c: c.data and c.data.startswith("admin:user:delete"))
async def admin_user_delete(cb: CallbackQuery):
    if not is_admin(cb.from_user.id):
        await cb.answer("Нет доступа!", show_alert=True)
        return

    _, _, _, tg_id_str = cb.data.split(":")
    tg_id = int(tg_id_str)

    async with AsyncSessionLocal() as session:
        user = await CRUDUser.get_by_tg_id(session, tg_id)
        if not user:
            await cb.answer("Пользователь уже удалён", show_alert=True)
            return

        await CRUDUser.delete_by_tg_id(session, tg_id)

    await cb.answer("Удалено", show_alert=True)

    # Возвращаемся к списку пользователей
    await cb.message.answer("Пользователь удалён.")


@router.callback_query(lambda c: c.data and c.data.startswith("admin:user:view"))
async def admin_user_view(cb: CallbackQuery):
    if not is_admin(cb.from_user.id):
        await cb.answer("Нет доступа", show_alert=True)
        return

    _, _, _, tg_id_str = cb.data.split(":")
    tg_id = int(tg_id_str)

    async with AsyncSessionLocal() as session:
        user = await CRUDUser.get_by_tg_id(session, tg_id)

    if not user:
        await cb.answer("Пользователь не найден", show_alert=True)
        return

    text = (
        f"👤 Пользователь\n\n"
        f"ID: {user.tg_id}\n"
        f"Username: @{user.username}\n"
        f"Name: {user.first_name or ''} {user.last_name or ''}\n"
        f"Created: {user.created_at}\n"
    )

    keyboard = admin_user_actions(user.tg_id)

    await safe_edit_message(cb.message, text, reply_markup=keyboard)
    await cb.answer()


@router.callback_query(lambda c: c.data == "admin:back_to_list")
async def admin_back_to_list(cb: CallbackQuery):
    if not is_admin(cb.from_user.id):
        await cb.answer("Нет доступа", show_alert=True)
        return

    await admin_users_page(cb)


@router.callback_query(lambda c: c.data == "admin:menu")
async def admin_menu(cb: CallbackQuery):
    if not is_admin(cb.from_user.id):
        await cb.answer("Нет доступа!", show_alert=True)
        return
    
    await safe_edit_message(
        cb.message,
        text="Administrator panel:",
        reply_markup=admin_main_kb()
    )
    await cb.answer()


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

    async with AsyncSessionLocal() as session:
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
