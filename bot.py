import discord
import json
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

BOT_NAME = "My Discord Bot"
DEFAULT_PREFIX = "!"

GREEN = 0x2ECC71
RED   = 0xE74C3C

def get_prefix(bot, message):
    try:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)
        guild_id = str(message.guild.id) if message.guild else "0"
        return prefixes.get(guild_id, DEFAULT_PREFIX)
    except FileNotFoundError:
        return DEFAULT_PREFIX

class CaseInsensitiveBot(commands.Bot):
    def get_command(self, name: str):
        cmd = super().get_command(name)
        if cmd:
            return cmd
        lower = name.lower()
        for command in self.commands:
            if command.name.lower() == lower:
                return command
            if any(a.lower() == lower for a in command.aliases):
                return command
        return None

intents = discord.Intents.all()
bot = CaseInsensitiveBot(command_prefix=get_prefix, intents=intents, help_command=None)

def av(user):
    return user.avatar.url if user.avatar else user.default_avatar.url

# ── Block all commands in DMs ─────────────────────────────────
@bot.check
async def guild_only(ctx):
    if ctx.guild is None:
        try:
            em = discord.Embed(
                title="🚫 Server Only",
                description="Commands only work inside a server, not in DMs!",
                color=RED,
            )
            await ctx.send(embed=em)
        except Exception:
            pass
        return False
    return True

# ── Dynamic config check (channels + blacklists) ──────────────
@bot.check
async def config_check(ctx):
    from shared import get_config
    cfg = get_config()

    if ctx.command and ctx.command.name in ("setup",):
        return True

    if ctx.author.id in cfg.get("blacklisted_users", []):
        try:
            em = discord.Embed(
                title="🚫 Blacklisted",
                description="You are not allowed to use bot commands.",
                color=RED,
            )
            await ctx.send(embed=em, delete_after=5)
        except Exception:
            pass
        return False

    if ctx.channel.id in cfg.get("blacklisted_channels", []):
        return False

    allowed = cfg.get("allowed_channels", [])
    if allowed and ctx.channel.id not in allowed:
        try:
            mentions = " ".join(f"<#{c}>" for c in allowed[:3])
            em = discord.Embed(
                title="🚫 Wrong Channel",
                description=f"Commands only work in: {mentions}",
                color=RED,
            )
            await ctx.send(embed=em, delete_after=5)
        except Exception:
            pass
        return False

    return True

@bot.event
async def setup_hook():
    # Add your future cogs/extensions to this list
    extensions = [
        "help",
        "prefix",
    ]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is ONLINE — serving {len(bot.guilds)} server(s)")
    from shared import get_config
    get_config()

@bot.event
async def on_guild_join(guild):
    from shared import get_config
    get_config()
    print(f"✅ Joined: {guild.name} ({guild.id})")
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            em = discord.Embed(
                title=f"👋 Thanks for adding {BOT_NAME}!",
                description=(
                    f"Run **`{DEFAULT_PREFIX}help`** for the full command list.\n"
                    f"Admins can change the prefix anytime with **`{DEFAULT_PREFIX}prefix <new_prefix>`**."
                ),
                color=GREEN,
            )
            em.set_footer(text=f"{BOT_NAME} • {DEFAULT_PREFIX}help to get started")
            try:
                await channel.send(embed=em)
            except Exception:
                pass
            break

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        em = discord.Embed(
            title="🚫 Missing Permissions",
            description="You don't have permission to use this.",
            color=RED,
        )
        em.timestamp = discord.utils.utcnow()
        await ctx.send(embed=em)
    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(
            title="⚠️ Missing Argument",
            description=f"Missing: `{error.param.name}`",
            color=RED,
        )
        em.timestamp = discord.utils.utcnow()
        await ctx.send(embed=em)
    else:
        print(f"❌ {ctx.command}: {error}")

bot.run(TOKEN)