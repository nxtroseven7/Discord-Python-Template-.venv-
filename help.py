import discord
from discord.ext import commands

BOT_NAME = "My Discord Bot"
GREEN = 0x2ECC71
RED   = 0xE74C3C

def av(user):
    return user.avatar.url if user.avatar else user.default_avatar.url

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["commands"], help="Shows the help menu or info about a command.")
    async def help_command(self, ctx, *, command_name: str = None):
        prefix = ctx.prefix

        if command_name is None:
            em = discord.Embed(
                title=f"📜 {BOT_NAME} — Help Menu",
                description=f"Use **`{prefix}help <command>`** for details on a specific command.",
                color=GREEN,
            )
            em.add_field(
                name="🤖 Bot Account",
                value=f"`{self.bot.user.name}` (`{self.bot.user.id}`)",
                inline=True,
            )
            em.add_field(
                name="🟢 Status",
                value=f"Online • `{round(self.bot.latency * 1000)}ms`",
                inline=True,
            )

            # Dynamically list commands grouped by Cog
            for cog_name, cog in self.bot.cogs.items():
                cmds = [c for c in cog.get_commands() if not c.hidden]
                if cmds:
                    cmd_list = ", ".join(f"`{c.name}`" for c in cmds)
                    em.add_field(name=f"📂 {cog_name}", value=cmd_list, inline=False)

            em.set_thumbnail(url=av(self.bot.user))
            em.set_footer(text=f"Requested by {ctx.author.name} • {prefix}help", icon_url=av(ctx.author))
            await ctx.send(embed=em)
        else:
            cmd = self.bot.get_command(command_name)
            if not cmd or cmd.hidden:
                em = discord.Embed(
                    title="🚫 Command Not Found",
                    description=f"No command named **`{command_name}`** was found.",
                    color=RED,
                )
                em.set_footer(text=f"{BOT_NAME} • {prefix}help", icon_url=av(ctx.author))
                await ctx.send(embed=em, delete_after=5)
                return

            em = discord.Embed(
                title=f"📖 Command: {prefix}{cmd.name}",
                description=cmd.help or "No description provided.",
                color=GREEN,
            )
            usage = f"`{prefix}{cmd.name} {cmd.signature}`".strip()
            em.add_field(name="Usage", value=usage, inline=False)
            em.add_field(
                name="Aliases",
                value=", ".join(f"`{a}`" for a in cmd.aliases) if cmd.aliases else "None",
                inline=False,
            )
            em.set_footer(text=f"{BOT_NAME} • {prefix}help", icon_url=av(self.bot.user))
            await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(Help(bot))