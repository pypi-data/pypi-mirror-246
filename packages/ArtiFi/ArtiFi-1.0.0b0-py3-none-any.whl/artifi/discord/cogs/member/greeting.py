from datetime import datetime

from discord import Embed
from discord.ext.commands import Cog

from artifi.discord import Discord, send_message


class Greeting(Cog):

    def __init__(self, bot):
        self._bot: Discord = bot

    @Cog.listener()
    async def on_member_join(self, member):
        embed = Embed(
            timestamp=datetime.now(),
            title="**Welcome To Our Server!**",
            description="We're Excited To Have You Here!",
            url="https://discord.com/invite/G8aRBSAR2J"
        )
        embed.set_author(
            name="Humanpredator",
            icon_url="https://cdn.discordapp.com/attachments/1151412194794278972/1151418378339237899/borg-7424633.jpg"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/1151412194794278972/1151412357222903859/1284962.png"
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/1151412194794278972/1151412356618919986/1321259.png"
        )
        await send_message(member, embed=embed)


async def setup(bot):
    await bot.add_cog(Greeting(bot))
