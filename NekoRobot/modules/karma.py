"""
MIT License

Copyright (c) 2022 Aʙɪsʜɴᴏɪ

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# ""DEAR PRO PEOPLE,  DON'T REMOVE & CHANGE THIS LINE
# TG :- @Abishnoi1M
#     MY ALL BOTS :- Abishnoi_bots
#     GITHUB :- KingAbishnoi ""

import asyncio

from pyrogram import filters

from NekoRobot import pgram as app
from NekoRobot.modules.mongo.karma_mongo import (
    alpha_to_int,
    get_karma,
    get_karmas,
    int_to_alpha,
    update_karma,
)
from NekoRobot.utils.errors import capture_err

regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍|nice|noice|piro)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|noob|Noob|gross|fuck off)$"

karma_positive_group = 3
karma_negative_group = 4


from pymongo import MongoClient

from NekoRobot import MONGO_DB_URI

worddb = MongoClient(MONGO_DB_URI)
k = worddb["NekoKarma"]["karma_status"]


async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in app.iter_chat_members(chat_id, filter="administrators")
    ]


@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_positive_group,
)
async def upvote(_, message):
    chat_id = message.chat.id
    is_karma = k.find_one({"chat_id": chat_id})
    if not is_karma:
        if not message.reply_to_message.from_user:
            return
        if not message.from_user:
            return
        if message.reply_to_message.from_user.id == message.from_user.id:
            return
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
        current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
        if current_karma:
            current_karma = current_karma["karma"]
            karma = current_karma + 1
        else:
            karma = 1
        new_karma = {"karma": karma}
        await update_karma(chat_id, await int_to_alpha(user_id), new_karma)
        await message.reply_text(
            f"ɪɴᴄʀᴇᴍᴇɴᴛᴇᴅ ᴋᴀʀᴍᴀ  ᴏғ +1 {user_mention} \nᴛᴏᴛᴀʟ ᴘᴏɪɴᴛs: {karma}"
        )


@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_negative_group,
)
async def downvote(_, message):
    chat_id = message.chat.id
    is_karma = k.find_one({"chat_id": chat_id})
    if is_karma:
        if not message.reply_to_message.from_user:
            return
        if not message.from_user:
            return
        if message.reply_to_message.from_user.id == message.from_user.id:
            return
        user_id = message.reply_to_message.from_user.id
        user_mention = message.reply_to_message.from_user.mention
