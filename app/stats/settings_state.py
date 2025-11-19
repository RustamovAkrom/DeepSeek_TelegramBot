from aiogram.fsm.state import StatesGroup, State


class SettingsState(StatesGroup):
    waiting_api_key = State()
    waiting_model = State()
