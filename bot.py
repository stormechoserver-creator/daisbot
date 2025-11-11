import discord
from discord.ext import commands
import sqlite3

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('rpg_profiles.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            user_id TEXT PRIMARY KEY,
            xp INTEGER DEFAULT 0,
            gold INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def get_profile(user_id):
    conn = sqlite3.connect('rpg_profiles.db')
    c = conn.cursor()
    c.execute('SELECT xp, gold FROM profiles WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result or (0, 0)

def update_stat(user_id, stat, amount):
    conn = sqlite3.connect('rpg_profiles.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO profiles (user_id) VALUES (?)', (user_id,))
    c.execute(f'UPDATE profiles SET {stat} = {stat} + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    init_db()

# --- Public Commands ---
@bot.command(name='get')
async def get(ctx, member: discord.Member = None):
    member = member or ctx.author
    xp, gold = get_profile(str(member.id))
    await ctx.send(f"{member.mention} | XP: {xp} | Gold: {gold}")

@bot.command(name='commands')
async def commands(ctx):
    help_text = (
        "**Available Commands:**\n"
        "`!get [@user]` – View your profile or another user's profile.\n"
        "`!add @user [xp/gold] [amount]` – Add XP or Gold (Mage Wright & Storm Lords only).\n"
        "`!re @user [xp/gold] [amount]` – Remove XP or Gold (Mage Wright & Storm Lords only).\n"
        "`!commands` – Display this help message."
    )
    await ctx.send(help_text)

# --- Role-Restricted Commands ---
def has_role(ctx):
    allowed_roles = ['Mage Wright', 'Storm Lords']
    return any(role.name in allowed_roles for role in ctx.author.roles)

@bot.command(name='add')
async def add(ctx, member: discord.Member, stat: str, amount: int):
    if not has_role(ctx):
        await ctx.send("Only Mage Wrights or Storm Lords may invoke this rite.")
        return
    if stat not in ['xp', 'gold']:
        await ctx.send("Stat must be 'xp' or 'gold'.")
        return
    update_stat(str(member.id), stat, amount)
    await ctx.send(f"{member.mention} gains {amount} {stat.upper()}!")

@bot.command(name='re')
async def remove(ctx, member: discord.Member, stat: str, amount: int):
    if not has_role(ctx):
        await ctx.send("Only Mage Wrights or Storm Lords may invoke this rite.")
        return
    if stat not in ['xp', 'gold']:
        await ctx.send("Stat must be 'xp' or 'gold'.")
        return
    update_stat(str(member.id), stat, -amount)
    await ctx.send(f"{member.mention} loses {amount} {stat.upper()}.")

from dotenv import load_dotenv
load_dotenv()

import os
bot.run(os.getenv("MTQzNjY3MjIzNTgyMDY4MzM0Ng.GqxaR7.pTHZRtYktuKV7Zu991mueaMYXA_uTo1T0271cg")

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Dais is stormbound and watching the skies."

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()