import tortoise

from bot.settings import settings

db = tortoise.Tortoise()

MODELS_MODULES_PREFIX: str = "bot.database.models"

MODELS_MODULES: list[str] = [
    f"{MODELS_MODULES_PREFIX}.user",
]

TORTOISE_CONFIG = {
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES + ["aerich.models"],
            "default_connection": "default"
        },

    },
    'timezone': 'Europe/Moscow',

}