"""
 * @author        yasir <yasiramunandar@gmail.com>
 * @date          2022-12-01 09:12:27
 * @lastModified  2022-12-01 09:32:31
 * @projectName   MissKatyPyro
 * Copyright @YasirPedia All rights reserved
"""
import os

from pyrogram import filters
from telegraph import upload_file

from NekoRobot import pgram as app
from NekoRobot.utils.errors import capture_err
from NekoRobot import http


@app.on_message(filters.command(["ocr"]))
@capture_err
async def ocr(_, message):
    reply = message.reply_to_message
    if not reply or not reply.photo and not reply.sticker:
        return await message.reply_text(f"Reply photo with /{message.command[0]} command")
    msg = await message.reply("Reading image...")
    try:
        file_path = await reply.download()
        if reply.sticker:
            file_path = await reply.download(f"ocr{message.from_user.id}.jpg")
        response = upload_file(file_path)
        url = f"https://telegra.ph{response[0]}"
        req = (
            await http.get(
                f"https://script.google.com/macros/s/AKfycbwURISN0wjazeJTMHTPAtxkrZTWTpsWIef5kxqVGoXqnrzdLdIQIfLO7jsR5OQ5GO16/exec?url={url}",
                follow_redirects=True,
            )
        ).json()
        await msg.edit(f"Hasil OCR:\n<code>{req['text']}</code>")
        os.remove(file_path)
        await msg.edit(str(e))
        os.remove(file_path)


__help__ = """
 ❍ /ocr [reply to photo]*:* Extract texts from the photo.
"""

__mod_name__ = "𝙾ᴄʀ"
