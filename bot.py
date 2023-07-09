import discord
from discord.ext import commands
import random

# Bot token from Discord Developer Portal
TOKEN = 'MTEyNzI0NjEyMDQ2NTIwMzI5NA.G62g-P.pxsF2UnHlvAfgoPFWTvEZ5-NfEskB0qseZXZ-k'

# K-pop groups and their members as cards
KPOP_GROUPS = {
    "BTS": ["Jin", "Suga", "J-Hope", "RM", "Jimin", "V", "Jungkook"],
    "Blackpink": ["Jisoo", "Jennie", "Rosé", "Lisa"],
    # Add more groups and members here...
}

# Card tiers and their probabilities
CARD_TIERS = {
    "Eevee": (KPOP_GROUPS, 50),
    "Jolteon, Flareon, & Vaporeon": (KPOP_GROUPS, 30),
    "Espeon & Umbreon": (KPOP_GROUPS, 15),
    "Leafeon & Glaceon": (KPOP_GROUPS, 4),
    "Sylveon": (KPOP_GROUPS, 1),
}

# User inventory
user_inventory = {}

intents = discord.Intents.all()
intents.members = True
intents.messages = True 
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_random_card():
    tier_names = list(CARD_TIERS.keys())
    probabilities = [tier[1] for tier in CARD_TIERS.values()]
    tier = random.choices(tier_names, weights=probabilities, k=1)[0]

    groups = list(CARD_TIERS[tier][0].keys())
    group = random.choice(groups)
    idol = random.choice(CARD_TIERS[tier][0][group])

    return tier, group, idol

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(
    name="drop",
    help="Get a random K-pop card!"
)
async def drop(ctx: commands.Context):
    tier, group, idol = get_random_card()
    
    # Update user inventory
    if idol not in user_inventory:
        user_inventory[idol] = 1
    else:
        user_inventory[idol] += 1
    
    await ctx.send(f"You got a {tier} card! It's {idol} from {group}!")

@bot.command(
    name="gift",
    help="Gift a specific K-pop card to a user!"
)
async def gift(ctx: commands.Context, user: discord.User, card_name: str):
    
    # Check if specified card is valid
    if card_name not in CARD_TIERS:
        await ctx.send(f"{card_name} is not a valid card!")
        return
    
    # Check if user has specified card in their inventory
    if card_name not in user_inventory or user_inventory[card_name] == 0:
        await ctx.send(f"You don't have any {card_name} cards to gift!")
        return
    
    # Update user inventory
    user_inventory[card_name] -= 1
    
    await ctx.send(f"You gifted a {card_name} card to {user.name}!")

@bot.command(
    name="inv",
    help="Check your inventory!"
)
async def inv(ctx: commands.Context):
    
    # Create inventory message
    inv_msg = ""
    
    for card_name in user_inventory:
        inv_msg += f"{card_name}: {user_inventory[card_name]}\n"
    
    await ctx.send(inv_msg)

bot.run(TOKEN)

