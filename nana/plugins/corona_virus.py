import asyncio

from pyrogram import filters

from nana import COMMAND_PREFIXES, app, AdminSettings, edit_or_reply
from nana.utils.aiohttp_helper import AioHttp

__MODULE__ = "Covid"
__HELP__ = """
Check info of cases corona virus disease 2019

──「 **Info Covid** 」──
-> `covid - for Global Stats`
-> `covid (country) - for a Country Stats`
"""


@app.on_message(
    filters.user(AdminSettings) & filters.command("covid", COMMAND_PREFIXES)
)
async def corona(_, message):
    args = message.text.split(None, 1)
    if len(args) == 1:
        try:
            r = await AioHttp().get_json("https://corona.lmao.ninja/v2/all")
            reply_text = f"""**Global Cases 🦠:**
 - **Cases:** `{r['cases']:,}`
 - **Cases Today:** `{r['todayCases']:,}`
 - **Deaths:** `{r['deaths']:,}`
 - **Deaths Today:** `{r['todayDeaths']:,}`
 - **Recovered:** `{r['recovered']:,}`
 - **Active:** `{r['active']:,}`
 - **Critical:** `{r['critical']:,}`
 - **Cases/Mil:** `{r['casesPerOneMillion']}`
 - **Deaths/Mil:** `{r['deathsPerOneMillion']}``
"""
            await edit_or_reply(message, text=f"{reply_text}")
            return
        except Exception as e:
            await edit_or_reply(
                message,
                text="`The corona API could not be reached`"
            )
            print(e)
            await asyncio.sleep(3)
            await message.delete()
            return
    country = args[1]
    r = await AioHttp().get_json(
        f"https://corona.lmao.ninja/v2/countries/{country}"
    )
    if "cases" not in r:
        await edit_or_reply(
            message,
            text="```The country could not be found!```"
        )
        await asyncio.sleep(3)
        await message.delete()
    else:
        try:
            reply_text = f"""**Cases for {r['country']} 🦠:**
 - **Cases:** `{r['cases']:,}`
 - **Cases Today:** `{r['todayCases']:,}`
 - **Deaths:** `{r['deaths']:,}`
 - **Deaths Today:** `{r['todayDeaths']:,}`
 - **Recovered:** `{r['recovered']:,}`
 - **Active:** `{r['active']:,}`
 - **Critical:** `{r['critical']:,}`
 - **Cases/Mil:** `{r['casesPerOneMillion']}`
 - **Deaths/Mil:** `{r['deathsPerOneMillion']}`
"""
            await edit_or_reply(message, text=reply_text)
        except Exception as e:
            await edit_or_reply(
                message,
                text="`The corona API could not be reached`"
            )
            print(e)
            await asyncio.sleep(3)
            await message.delete()
