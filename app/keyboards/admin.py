from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def admin_main_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Users", callback_data="admin:users:0")
            ],
            [
                InlineKeyboardButton(text="Stats", callback_data="admin:stats")
            ]
        ]
    )


def admin_user_actions(tg_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👁 View Profile",
                    callback_data=f"admin:user:view:{tg_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Delete User",
                    callback_data=f"admin:user:delete:{tg_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Back",
                    callback_data="admin:back_to_list"
                )
            ]
        ]
    )
