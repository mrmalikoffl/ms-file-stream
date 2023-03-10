# This file is a part of ms-file-stream
# Coding : Mr Malik [@mrmalik_offl]

import logging
from pyrogram import filters, errors
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.vars import Var
from urllib.parse import quote_plus
from WebStreamer.bot import StreamBot, logger
from WebStreamer.utils.file_properties import get_name, get_hash, get_media_file_size
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@StreamBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.audio
        | filters.animation
        | filters.voice
        | filters.video_note
        | filters.photo
        | filters.sticker
    ),
    group=4,
)
async def media_receive_handler(_, m: Message):
    log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)
    file_hash = get_hash(log_msg, Var.HASH_LENGTH)
    stream_link = f"{Var.URL}{log_msg.id}/{quote_plus(get_name(m))}?hash={file_hash}"
    short_link = f"{Var.URL}{file_hash}{log_msg.id}"
    logger.info(f"Generated link: {stream_link} for {m.from_user.first_name}")
    try:
        
        msg_text ="""<i><u>๐ฌ๐ผ๐๐ฟ ๐๐ถ๐ป๐ธ ๐๐ฒ๐ป๐ฒ๐ฟ๐ฎ๐๐ฒ๐ฑ !</u></i>\n\n<b>๐ Fษชสแด ษดแดแดแด :</b> <i>{}</i>\n\n<b>๐ฆ Fษชสแด ๊ฑษชแดขแด :</b> <i>{}</i>\n\n<b>๐ฅ Dแดแดกษดสแดแดแด :</b> <i>{}</i>\n\n<b>๐ธ Nแดแดแด : LINK WON'T EXPIRE TILL I DELETE</b>"""
        
        await m.reply_text(
            text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(m)), stream_link, short_link),
            quote=True,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(
                    text=f"๐ฅ Download Now ๐ฅ", url=short_link)],
                 [InlineKeyboardButton("๐จ๐ปโ๐ป Developer ๐จ๐ปโ๐ป", url='https://t.me/mrmalik_offl'),
                  InlineKeyboardButton("๐ Bot Updates ๐", url='https://t.me/+rN9QCFgIihgyZWM1')]]
            ),
        )
    except errors.ButtonUrlInvalid:
        await m.reply_text(
            text="<code>{}</code>\n\nshortened: {})".format(
                stream_link, short_link
            ),
            quote=True,
            parse_mode=ParseMode.HTML,
        )
