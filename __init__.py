import traceback

from nonebot.plugin import PluginMetadata

from zhenxun.builtin_plugins.sign_in.utils import (
    get_level_and_next_impression,
    level2attitude,
)
from zhenxun.configs.config import BotConfig
from zhenxun.configs.utils import PluginExtraData
from zhenxun.models.sign_user import SignUser
from zhenxun.services.log import logger

__plugin_meta__ = PluginMetadata(
    name="MaiM_connecter",
    description=f"{BotConfig.self_nickname}与MaiM的通讯插件",
    usage="""
    """.strip(),
    extra=PluginExtraData(author="The_elevenFD", version="0.1").to_dict(),
)

from nonebot import get_app

app = get_app()


@app.post("/get_info/{user_id}")
async def get_info(user_id: int):
    try:
        sign_user = await SignUser.get_or_none(user_id=user_id)
        if sign_user is None:
            return {"error": "User not found", "code": 404}
        impression = float(sign_user.impression)
        level, _, _ = get_level_and_next_impression(impression)
        level = level if level != 0 else 1
        attitude = level2attitude[str(level)]
        logger.error(
            f"Success get info, user_id: {user_id}, impression: {impression}, attitude: {attitude}, level: {level}"
        )
        return {"impression": impression, "attitude": attitude, "level": level}
    except Exception:
        return {"error": traceback.format_exc(), "code": 500}
