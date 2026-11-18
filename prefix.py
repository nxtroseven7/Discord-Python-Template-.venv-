import discord
import json
import os
from discord.ext import commands

BOT_NAME = "My Discord Bot"
GREEN = 0x2ECC71
RED   = 0xE74C3C

def av(user):
    return user.avatar.url if user.avatar else user.default_avatar.url

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _make_embed(self, title: str, description: str, color: int = GREEN):
        em = discord.Embed(title=title, description=description, color=color)
        em.timestamp = discord.utils.utcnow()
        return em

    @commands.command(name="prefix", aliases=["setprefix"], help="Change the server command prefix.")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix: str = None):
        if not new_prefix:
            em = self._make_embed(
                "⚠️ Missing Prefix",
                f"Please specify a new prefix.\nUsage: `{ctx.prefix}prefix <new_prefix>`",
                color=RED,
            )
            em.set_footer(text=f"{BOT_NAME} • Requested by {ctx.author.name}", icon_url=av(ctx.author))
            await ctx.send(embed=em, delete_after=5)
            return

        if len(new_prefix) > 5:
            em = self._make_embed(
                "🚫 Prefix Too Long",
                "The server prefix cannot be longer than 5 characters.",
                color=RED,
            )
            em.set_footer(text=f"{BOT_NAME} • Requested by {ctx.author.name}", icon_url=av(ctx.author))
            await ctx.send(embed=em, delete_after=5)
            return

        try:
            prefixes = {}
            if os.path.exists("prefixes.json"):
                with open("prefixes.json", "r") as f:
                    prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = new_prefix

            with open("prefixes.json", "w") as f:
                json.dump(prefixes, f, indent=4)

            em = self._make_embed(
                "✅ Prefix Updated",
                f"Server prefix updated to **`{new_prefix}`**\nTry running: `{new_prefix}help`",
                color=GREEN,
            )
            em.set_footer(text=f"{BOT_NAME} • Updated by {ctx.author.name}", icon_url=av(ctx.author))
            await ctx.send(embed=em)

        except Exception as e:
            em = self._make_embed(
                "❌ Error",
                f"Failed to save the prefix: `{e}`",
                color=RED,
            )
            em.set_footer(text=f"{BOT_NAME} • {ctx.prefix}prefix", icon_url=av(ctx.author))
            await ctx.send(embed=em, delete_after=5)

async def setup(bot):
    await bot.add_cog(Prefix(bot))