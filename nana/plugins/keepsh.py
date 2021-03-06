# This module created by @legenhand 10/3/2020
# any error / bugs please report to https://t.me/nanabotsupport
# this module only support to Nana-Bot userbot
import datetime
import os

import pycurl
from pyrogram import filters

from nana import app, COMMAND_PREFIXES, log, AdminSettings, edit_or_reply
from .downloads import download_file_from_tg, name_file, humanbytes

__MODULE__ = "Keep.sh"
__HELP__ = """
Mirror any telegram file to keep.sh

──「 **Transfer telegram file** 」──
-> `keepsh`
Reply to telegram file for mirroring to keep.sh

"""


@app.on_message(
    filters.user(AdminSettings) & filters.command("keepsh", COMMAND_PREFIXES)
)
async def tfsh(client, message):
    if not message.reply_to_message:
        await edit_or_reply(
            message,
            text="`Reply to any file telegram message!`"
        )
        return
    await edit_or_reply(message, text="`Processing...`")
    name = await name_file(client, message)
    await download_file_from_tg(client, message)
    name_file_upload = name[-10:] if len(name) > 10 else name
    name_file_upload.encode("ascii", "ignore")
    os.rename(
        r"nana/downloads/{}".format(name),
        r"nana/downloads/{}".format(name_file_upload)
    )
    await edit_or_reply(
        message,
        text=await send_to_keepsh(
            "nana/downloads/{}".format(name_file_upload),
            message, name_file_upload
        ),
        disable_web_page_preview=True,
    )
    os.remove("nana/downloads/{}".format(name_file_upload))
    return


async def send_to_keepsh(file, message, name):
    """send file to keepsh, retrieve download link"""
    size_of_file = get_size(file)
    final_date = get_date_in_two_weeks()
    file_name = os.path.basename(file)

    await edit_or_reply(
        message,
        text="\nSending file: {} (size of the file: {})".format(
            file_name, size_of_file
        ),
    )
    url = "https://free.keep.sh/{}".format(name)
    c = pycurl.Curl()
    c.setopt(c.URL, url)

    c.setopt(c.UPLOAD, 1)
    with open(file, "rb") as f:
        c.setopt(c.READDATA, f)
        try:
            download_link = c.perform_rs()
        except pycurl.error as e:
            log.error(e)
            return "Unsupported file format!"
        c.close()
    f.close()
    return "`Success!\nwill be saved till {}`\n{}".format(
        final_date,
        download_link
    )


def get_size(file):
    """
    get file size, in megabytes
    :param file:
    :return: size of file
    """
    size_in_bytes = os.path.getsize(file)
    return humanbytes(size_in_bytes)


def get_date_in_two_weeks():
    """
    get maximum date of storage for file
    :return: date in two weeks
    """
    today = datetime.datetime.today()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()
