import os

import discord
import random
import json
from discord.ext import commands, tasks
from itertools import cycle
import sqlite3
import asyncio
import math


async def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


async def get_shop_channel(client, message):
    with open('shopchan.json', 'r') as f:
        shop_channel = json.load(f)

    return shop_channel[str(message.guild.id)]


async def get_character_channel(client, message):
    with open('charchan.json', 'r') as f:
        character_channel = json.load(f)

    return character_channel[str(message.guild.id)]


async def get_hp_name(client, message):
    with open('hp.json', 'r') as f:
        hp_name = json.load(f)

    return hp_name[str(message.guild.id)]


async def get_mp_name(client, message):
    with open('mp.json', 'r') as f:
        mp_name = json.load(f)

    return mp_name[str(message.guild.id)]


async def get_ep_name(client, message):
    with open('ep.json', 'r') as f:
        ep_name = json.load(f)

    return ep_name[str(message.guild.id)]


async def get_gold_name(client, message):
    with open('goldname.json', 'r') as f:
        gold_name = json.load(f)

    return gold_name[str(message.guild.id)]


async def get_level_list_string(client, message):
    with open('lvllist.json', 'r') as f:
        level_list = json.load(f)

    return level_list[str(message.guild.id)]


async def can_be_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


async def roll(dice : str):
    if dice.find('d') != -1:
        val = dice.split('d')
        try:
            count = int(val[0])
        except ValueError:
            diceRoll = -999999999999
            return diceRoll

        try:
            diceMax = int(val[1])
        except ValueError:
            diceRoll = -999999999999
            return diceRoll

        if diceMax < 0:
            diceRoll = -999999999999
            return diceRoll

        if count == 0:
            return diceMax
        else:
            dice = 0
            for i in range(count):
                dice += random.randint(1, diceMax)

            return dice


async def can_list_be_int(string_list):
    correct = True
    for i in string_list:
        if can_be_int(i):
            correct = True
        else:
            return False
        return correct

client = commands.Bot(command_prefix=get_prefix)


########################################################################################################################
#   EVENTS                                                                                                             #
########################################################################################################################
@client.event
async def on_ready():
    #Starting and creating database
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    #Creates spell list table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spells(
            guild_id TEXT,
            spell_name TEXT,
            attack_buff TEXT,
            spell_uses TEXT,
            spell_type TEXT,
            spell_range TEXT,
            spell_damage TEXT,
            spell_save TEXT,
            buff_debuff_condition TEXT,
            spell_desc TEXT
        )
    ''')

    print('spells Table built!')

    #Creates ability table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS abilities(
            guild_id TEXT,
            ability_name TEXT,
            ability_type TEXT,
            buff_range TEXT,
            buff_condition TEXT,
            ability_desc TEXT
        )
    ''')

    print('abilities Table built!')

    #Effects/Condition table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS effectcond(
            guild_id TEXT,
            condition_name TEXT,
            condition_type TEXT,
            condition_turns TEXT,
            condition_damage TEXT,
            condition_effect_roll TEXT,
            condition_gain_loss TEXT,
            condition_effect_stat TEXT,
            val_removed TEXT,
            cause_lose_turn TEXT,
            condition_desc TEXT
        )
    ''')

    print('condition Table built!')

    #Race Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS races(
            guild_id TEXT,
            race_name TEXT,
            val_hp TEXT,
            val_mp TEXT,
            val_ep TEXT,
            stats_plus_min TEXT,
            condtion_immune TEXT,
            condtition_strength TEXT,
            condition_vulnerable TEXT,
            ability_list TEXT,
            race_description TEXT
        )
    ''')

    print('race Table built!')

    #Class Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes(
            guild_id TEXT,
            class_name TEXT,
            add_sub_hp TEXT,
            add_sub_mp TEXT,
            add_sub_ep TEXT,
            stats_plus_min TEXT,
            stat_spell_save TEXT,
            unarmed_attack_damage TEXT,
            spell_array TEXT,
            start_weapon TEXT,
            start_armor TEXT,
            start_items TEXT,
            class_desc TEXT
        )
    ''')

    #Item Tables
    #Weapon Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weapons(
            guild_id TEXT,
            weapon_name TEXT,
            weapon_type TEXT,
            weapon_cost TEXT,
            weapon_desc TEXT
        )
    ''')

    print('weapons Table built!')

    # Armor Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS armors(
            guild_id TEXT,
            armor_name TEXT,
            armor_type TEXT,
            armor_plus_ac TEXT,
            armor_plus_roll TEXT,
            armor_cost TEXT,
            armor_desc TEXT
        )
    ''')

    print('armors Table built!')

    # Potion Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS potions(
            guild_id TEXT,
            potion_name TEXT,
            potion_condition TEXT,
            potion_cost TEXT,
            potion_desc TEXT
        )
    ''')

    print('potions Table built!')

    #Character Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters(
            guild_id TEXT,
            user_id TEXT,
            character_number TEXT,
            character_name TEXT,
            class_id TEXT,
            race_id TEXT,
            stat_list TEXT,
            weapon_id TEXT,
            armor_id TEXT,
            item_id_list TEXT,
            level TEXT,
            exp TEXT,
            character_desc TEXT
        )
    ''')

    #Rules Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules(
            guild_id TEXT,
            num_char_allowed TEXT,
            level_char TEXT,
            exp_for_win TEXT,
            exp_for_loss TEXT,
            ac_comp_roll TEXT,
            comp_roll_add TEXT,
            forfeit_loss TEXT,
            stat_for_init_role TEXT
        )
    ''')

    print('Rules Table Built!')

    # Stats Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats(
            guild_id TEXT,
            stat1 TEXT,
            stat2 TEXT,
            stat3 TEXT,
            stat4 TEXT,
            stat5 TEXT,
            stat6 TEXT,
            stat_dice TEXT,
            stat_reroll TEXT
        )
    ''')

    print('stats Table Built!')

    #player weapons table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_weapon(
            guild_id TEXT,
            user_id TEXT,
            weapon_name TEXT,
        )
    ''')

    print('player weapons Table Built!')

    # player armor table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_armor(
            guild_id TEXT,
            user_id TEXT,
            armor_name TEXT,
        )
    ''')

    print('player armor Table Built!')

    # player potion table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_potion(
            guild_id TEXT,
            user_id TEXT,
            potion_name TEXT,
        )
    ''')

    print('player potion Table Built!')

    # player gold table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_gold(
            guild_id TEXT,
            user_id TEXT,
            gold TEXT
        )
    ''')

    print('player gold Table Built!')



    await client.change_presence(activity=discord.Game('Turn Based Duels'))

    print('Bot is ready!')


@client.event
async def on_guild_join(guild):
    #Set prefixes for bot
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    #Set shop_channel for bot to general for the time being
    channels = ["general"]

    with open('shopchan.json', 'r') as f:
        shop_channel = json.load(f)

    shop_channel[str(guild.id)] = channels

    with open('shopchan.json', 'w') as f:
        json.dump(shop_channel, f, indent=4)


    #Set character_channel for bot to general for the time being
    channels = ["general"]

    with open('charchan.json', 'r') as f:
        character_channel = json.load(f)

    character_channel[str(guild.id)] = channels

    with open('charchan.json', 'w') as f:
        json.dump(character_channel, f, indent=4)

    #Set hp
    with open('hp.json', 'r') as f:
        hp_name = json.load(f)

    hp_name[str(guild.id)] = "TEMP"

    with open('hp.json', 'w') as f:
        json.dump(hp_name, f, indent=4)

    #Set mp
    with open('mp.json', 'r') as f:
        mp_name = json.load(f)

    mp_name[str(guild.id)] = "TEMP"

    with open('mp.json', 'w') as f:
        json.dump(mp_name, f, indent=4)
    #Set ep
    with open('ep.json', 'r') as f:
        ep_name = json.load(f)

    ep_name[str(guild.id)] = "TEMP"

    with open('ep.json', 'w') as f:
        json.dump(ep_name, f, indent=4)

    #Set gold name
    with open('goldname.json', 'r') as f:
        gold_name = json.load(f)

    gold_name[str(guild.id)] = "TEMP"

    with open('goldname.json', 'w') as f:
        json.dump(gold_name, f, indent=4)

    #Set lvl_list
    with open('lvllist.json', 'r') as f:
        lvl_list = json.load(f)

    lvl_list[str(guild.id)] = "TEMP"

    with open('lvllist.json', 'w') as f:
        json.dump(lvl_list, f, indent=4)


    #Send the start message to general channel
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(f'''
            ```Hello there! Thank you for adding the Turn Based RPG Bot to your Discord server!
            This bot was written in API version {discord.__version__}.\n\nThis bot can do several things. It can:
            -Manage one-on-one duel
            -Allow for the creation and storage of player character(s)
            -Manage shopping
            -And more
            
            
            To start the bot, first make channels for character creation and shopping.
            After this, use the commands !csc [channel] to set the shop channel and !ccc [channel] 
            to set the character creation channel. After this, use the !setup command to do the rest of the setup.
            
            When doing work for characters, please make spells, abilities, and conditions before creating races and classes.```''')
        break

@client.event
async def on_guild_remove(guild):
    #Remove prefixes for bot
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    #Remove shop_channel for bot
    with open('shopchan.json', 'r') as f:
        shop_channel = json.load(f)

    shop_channel.pop(str(guild.id))

    with open('shopchan.json', 'w') as f:
        json.dump(shop_channel, f, indent=4)

    #Remove character channel for bot
    with open('charchan.json', 'r') as f:
        character_channel = json.load(f)

    character_channel.pop(str(guild.id))

    with open('charchan.json', 'w') as f:
        json.dump(character_channel, f, indent=4)

    #Remove energy name for bot
    with open('ep.json', 'r') as f:
        nrg_name = json.load(f)

    nrg_name.pop(str(guild.id))

    with open('ep.json', 'w') as f:
        json.dump(nrg_name, f, indent=4)

    #Remove gold name for bot
    with open('goldname.json', 'r') as f:
        gld_name = json.load(f)

    gld_name.pop(str(guild.id))

    with open('goldname.json', 'w') as f:
        json.dump(gld_name, f, indent=4)

    #Remove hp name for bot
    with open('hp.json', 'r') as f:
        hp_name = json.load(f)

    hp_name.pop(str(guild.id))

    with open('hp.json', 'w') as f:
        json.dump(hp_name, f, indent=4)

    #Remove lvl list for bot
    with open('lvllist.json', 'r') as f:
        lvl_list = json.load(f)

    lvl_list.pop(str(guild.id))

    with open('lvllist.json', 'w') as f:
        json.dump(lvl_list, f, indent=4)

    # Remove mp name for bot
    with open('mp.json', 'r') as f:
        mp_name = json.load(f)

    mp_name.pop(str(guild.id))

    with open('mp.json', 'w') as f:
        json.dump(mp_name, f, indent=4)

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    # Delete from level
    cursor.execute(f'DELETE FROM level WHERE guild_id = {guild.id}')
    # Delete from spells
    cursor.execute(f'DELETE FROM spells WHERE guild_id = {guild.id}')
    # Delete from abilities
    cursor.execute(f'DELETE FROM abilities WHERE guild_id = {guild.id}')
    # Delete from effectcond
    cursor.execute(f'DELETE FROM effectcond WHERE guild_id = {guild.id}')
    # Delete from races
    cursor.execute(f'DELETE FROM races WHERE guild_id = {guild.id}')
    # Delete from classes
    cursor.execute(f'DELETE FROM classes WHERE guild_id = {guild.id}')
    # Delete from weapons
    cursor.execute(f'DELETE FROM weapons WHERE guild_id = {guild.id}')
    # Delete from armors
    cursor.execute(f'DELETE FROM armors WHERE guild_id = {guild.id}')
    # Delete from potions
    cursor.execute(f'DELETE FROM potions WHERE guild_id = {guild.id}')
    # Delete from characters
    cursor.execute(f'DELETE FROM characters WHERE guild_id = {guild.id}')
    # Delete from rules
    cursor.execute(f'DELETE FROM rules WHERE guild_id = {guild.id}')
    # Delete from stats
    cursor.execute(f'DELETE FROM stats WHERE guild_id = {guild.id}')
    # Delete from player_weapon
    cursor.execute(f'DELETE FROM player_weapon WHERE guild_id = {guild.id}')
    # Delete from player_armor
    cursor.execute(f'DELETE FROM player_armor WHERE guild_id = {guild.id}')
    # Delete from player_potion
    cursor.execute(f'DELETE FROM player_potion WHERE guild_id = {guild.id}')
    # Delete from player_gold
    cursor.execute(f'DELETE FROM player_gold WHERE guild_id = {guild.id}')
    db.commit()
    cursor.close()
    db.close()

@client.event
async def on_member_join(member):
    ment = member.mention
    for channel in member.guild.text_channels:
        if channel.permissions_for(member.guild.me).send_messages:
           channel.send(f'''Hello {ment}! Welcome to a server running the Turn Based Dueling Bot! 
           Please read the rules by calling view_all_rules, then create a character using character_creator!''')
    print(f'{member} has joined the server!!!!!!! WELCOME!!!!')


@client.event
async def on_member_remove(member):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    # Delete from characters
    cursor.execute(f'DELETE FROM characters WHERE guild_id = {member.guild.id} AND user_id = {member.id}')
    # Delete from player_weapon
    cursor.execute(f'DELETE FROM player_weapon WHERE guild_id = {member.guild.id} AND user_id = {member.id}')
    # Delete from player_armor
    cursor.execute(f'DELETE FROM player_armor WHERE guild_id = {member.guild.id} AND user_id = {member.id}')
    # Delete from player_potion
    cursor.execute(f'DELETE FROM player_potion WHERE guild_id = {member.guild.id} AND user_id = {member.id}')
    # Delete from player_gold
    cursor.execute(f'DELETE FROM player_gold WHERE guild_id = {member.guild.id} AND user_id = {member.id}')
    db.commit()
    cursor.close()
    db.close()

    print(f'{member} left! WE WILL MISS YOU!!!!!')




########################################################################################################################
#   COMMANDS                                                                                                           #
########################################################################################################################

########################################################################################################################
#   Important Stuff                                                                                                    #
########################################################################################################################

########################################################################################################################
#   Setup/Administrative Commands                                                                                      #
########################################################################################################################
#Changes the prefix for the bot
@client.command()
@commands.has_guild_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'```Prefix changed to {prefix}```')

#ERROR HANDLERS for prefix command
@changeprefix.error
async def prefixerror(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('The command is missing the correct arguments.\n```changeprefix [prefix]```')
    else:
        await ctx.send('An error has occurred!')

#Changes the channel that controls the shop
@client.command(aliases=['change-shop-channel', 'csc'])
@commands.has_guild_permissions(administrator=True)
async def changeshopchan(ctx, channel):
    ch = [channel]

    with open('shopchan.json', 'r') as f:
        shop_channel = json.load(f)

    shop_channel[str(ctx.guild.id)] = ch

    with open('shopchan.json', 'w') as f:
        json.dump(shop_channel, f, indent=4)

    await ctx.send(f'```The shop channel is now {ch}```')

#ERROR HANDLERS for changing shop channel command
@changeshopchan.error
async def shopchannelchangeerror(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('The command is missing the correct arguments.\n```change-shop-channel [channel]\ncsc [channel]```')
    else:
        await ctx.send('An error has occurred!')

# Changes the channel that controls the character creation
@client.command(aliases=['change-character-channel', 'ccc'])
@commands.has_guild_permissions(administrator=True)
async def changecharacterchan(ctx, channel):
    ch = [channel]

    with open('charchan.json', 'r') as f:
        character_channel = json.load(f)

    character_channel[str(ctx.guild.id)] = ch

    with open('charchan.json', 'w') as f:
        json.dump(character_channel, f, indent=4)

    await ctx.send(f'```The character building channel is now {ch}```')


@changecharacterchan.error
async def changecharacterchanerror(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('The command is missing the correct arguments.\n```change-character-channel [channel]\nccc [channel]```')
    else:
        await ctx.send('An error has occurred!')

#setup command
@client.command()
@commands.has_guild_permissions(administrator=True)
async def setup(ctx):

    # DB check if command was run
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT stat_for_init_role FROM rules WHERE guild_id = {ctx.guild.id}')
    result = cursor.fetchone()
    if result is None or "NO":
        # Rules DB setup
        sql = ("INSERT INTO rules(guild_id, num_char_allowed, level_char, exp_for_win, exp_for_loss, ac_comp_roll, comp_roll_add, forfeit_loss, stat_for_init_role) VALUES(?,?,?,?,?,?,?,?,?)")
        val = (ctx.guild.id, "0", "0", "0", "0", "0", "0", "0", "0")
        cursor.execute(sql, val)
        db.commit()

        # Stat DB setup
        sql = ("INSERT INTO stats(guild_id, stat1, stat2, stat3, stat4, stat5, stat6, stat_dice, stat_reroll) VALUES(?,?,?,?,?,?,?,?,?)")
        val = (ctx.guild.id, "NO", "NO", "NO", "NO", "NO", "NO", "NO", "-1")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    elif result is not None:
        await ctx.send('''```You have already run this command!```''')
        return


    await ctx.send('''Lets start by picking the name for your health, mana, and energy values.
        These values act as follows:
        -Health: Refers to the value to track damage taken, and the first person to reach 0 health loses
        -Mana: Refers to the value that determines if you can use magic spells
        -Energy: Refers to the value that determines if you can use physical spells (you can choose not to use this but 
        please still give it a name)\n\n
        
        Lets start with health first.''')

    #Check if author of message is the author of the command sender
    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel

    #HP name
    hp = await client.wait_for("message", check=check)
    hp = hp.content

    with open('hp.json', 'r') as f:
        hp_dict = json.load(f)

    hp_dict[str(ctx.guild.id)] = hp

    with open('hp.json', 'w') as f:
        json.dump(hp_dict, f, indent=4)

    #Mana Name
    await ctx.send('Thank you! Now lets get a name for mana.')

    mp = await client.wait_for("message", check=check)
    mp = mp.content

    with open('mp.json', 'r') as f:
        mp_dict = json.load(f)

    mp_dict[str(ctx.guild.id)] = mp

    with open('mp.json', 'w') as f:
        json.dump(mp_dict, f, indent=4)

    #energy name
    await ctx.send('Thank you! Now lets get a name for energy.')

    ep = await client.wait_for("message", check=check)
    ep = ep.content

    with open('ep.json', 'r') as f:
        ep_dict = json.load(f)

    ep_dict[str(ctx.guild.id)] = ep

    with open('ep.json', 'w') as f:
        json.dump(ep_dict, f, indent=4)

    #Gold Name
    await ctx.send('''Thank you! Now lets get a name for your gold. Gold is used to purchase items at the shop.''')

    gold = await client.wait_for("message", check=check)
    gold = gold.content

    with open('goldname.json', 'r') as f:
        gold_dict = json.load(f)

    gold_dict[str(ctx.guild.id)] = gold

    with open('goldname.json', 'w') as f:
        json.dump(gold_dict, f, indent=4)


    #Stats list
    await ctx.send('''Alright, now that the names are sorted, lets give your stats a name. Stats are used to determine your characters abilities. You have six stats and must give names to all six.
                    However, if you desire, you can leave some with the name of NOTHING if you don't want it to do anything. Please format the stats name in the following manner. stat1,stat2,stat3,stat4,stat5,stat6. 
                   ''')

    # remove commas from stats
    test = True
    while(test):
        statstring = await client.wait_for("message", check=check)
        statstring = statstring.content

        if len(statstring.split(',')) != 6:
            await ctx.send('The format is incorrect please retry')
            test = True
        else:
            #DB work set stat1 - stat6 to listed values then print stat1 - stat6
            x = statstring.split(',')

            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            sql = ('UPDATE stats SET stat1 = ?, stat2 = ?, stat3 = ?, stat4 = ?, stat5 = ?, stat6 = ? WHERE guild_id = ?')
            val = (x[0], x[1], x[2], x[3], x[4], x[5], ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            stat1 = x[0].rstrip(',')
            stat2 = x[1].rstrip(',')
            stat3 = x[2].rstrip(',')
            stat4 = x[3].rstrip(',')
            stat5 = x[4].rstrip(',')
            stat6 = x[5].rstrip(',')

            await ctx.send(f'Stat values are stat1: {stat1}, stat2: {stat2}, stat3: {stat3}, stat4: {stat4}, stat5: {stat5}, stat6: {stat6}. Don\'t worry, this can be changed later if they are incorrect.')

            test = False

    #Stat point buy or dice
    await ctx.send('''Next, lets determine if you are using point buy or dice. 
                   The point buy system is where each stat is at a base of 0 and they have 10 points to distribute between each stat.
                   Dice rolls allows for a dice or multiple's of one dice to become your stats.
                   
                   If you are using point buy, type POINTBUY and if you are using dice, type XdY where X is the number of dice and Y is the dice type.
                   ''')

    reroll = False
    test1 = True
    while(test1):
        dice = await client.wait_for("message", check=check)
        dice = dice.content

        if dice == 'POINTBUY':
            # Stat DB dice type to dice
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE stats SET stat_dice = ? WHERE guild_id = ?")
            val = (dice, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send(f'The value is now {dice}.')

            test1 = False

        else:
            if dice.find('d') != -1:
                x = dice.split('d')

                if can_be_int(x[0]) and can_be_int(x[1]):
                    if (int(x[0]) > 0) and (int(x[1]) > 0):
                        # Stat DB dice type to dice
                        db = sqlite3.connect('main.sqlite')
                        cursor = db.cursor()

                        sql = ("UPDATE stats SET stat_dice = ? WHERE guild_id = ?")
                        val = (dice, ctx.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()


                        await ctx.send(f'The value is now {dice}.')
                        test1 = False
                        reroll = True

                    else:
                        test1 = True
                        await ctx.send('One of your dice values was negative! Please try again!')
                else:
                    test1 = True
                    await ctx.send('That value is not in XdY form! Please try again!')

            else:
                test1 = True
                await ctx.send('The value does not fit the required formats! Please try again!')

    if reroll:
        await ctx.send('''Since you picked the dice rolling system, do you want to have a minimum stat value. If any dice roll is less than or equal to this value, it will be re-rolled till a better value is present.'
                       If you do not want any value, set the value to -1''')

        reroll_val = await client.wait_for("message", check=check)
        reroll_val = reroll_val.content

        # Stat DB set re-roll value
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        sql = ('UPDATE stats SET stat_reroll = ? WHERE guild_id = ?')
        val = (reroll_val, ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

        await ctx.send(f'Re-roll value set to {reroll_val}')

    #Rules set
    await ctx.send('''Now lets focus on rules. First, how many characters are people allowed to have? The value must be greater than or equal to 1!''')

    character_at_level = False
    test2 = True
    while(test2):
        charNum = await client.wait_for("message", check=check)
        charNum = charNum.content
        if can_be_int(charNum):
            if int(charNum) > 1:
                # set num characters to charNum
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET num_char_allowed = ? WHERE guild_id = ?")
                val = (charNum, ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                character_at_level = True
                test2 = False
                await ctx.send(f'The number of characters has been set to {charNum}')
            elif int(charNum) == 1:
                # set num characters to charNum
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET num_char_allowed = ? WHERE guild_id = ?")
                val = (charNum, ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test2 = False
                await ctx.send(f'The number of characters has been set to {charNum}')
            else:
                await ctx.send('The value you entered is less than 0! Please try again!')
                test2 = True
        else:
            await ctx.send('The value you entered is not a number! Please try again!')
            test2 = True

    if character_at_level:
        await ctx.send('Since you selected to allow more than one character, select at what level the player\'s most recent character. This will be implemented in the future.')
        test3 = True
        while(test3):
            charlvl = await client.wait_for("message", check=check)
            charlvl = charlvl.content
            if can_be_int(charlvl):
                if int(charlvl) >= 0:
                    # DB work set level to charlvl
                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ("UPDATE rules SET level_char = ? WHERE guild_id = ?")
                    val = (charlvl, ctx.guild.id)
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

                    await ctx.send(f'The level has been set to {charlvl}')
                    test3 = False
                else:
                    await ctx.send('The level you set is to low! Please try again!')
                    test3 = True
            else:
                await ctx.send('The level you set is not a number! Please try again!')
                test3 = True
    else:
        # set level to 0
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        sql = ("UPDATE rules SET level_char = ? WHERE guild_id = ?")
        val = ("0", ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        pass

    await ctx.send('''Now lets set up the level list. To set this up, list the experience to level the next level in an additive fashion.
                    This would mean the string 1,2,3,5,7,9,10,12,15 would be equal to:
                    
                    Level 1 >> Level 2 requires 1 exp point
                    Level 2 >> Level 3 requires 2 exp points
                    Level 3 >> Level 4 requires 3 exp points
                    Level 4 >> Level 5 requires 5 exp points
                    Level 5 >> Level 6 requires 7 exp points
                    Level 6 >> Level 7 requires 9 exp points
                    Level 7 >> Level 8 requires 10 exp points
                    Level 8 >> Level 9 requires 12 exp points
                    Level 9 >> Level 10 requires 15 exp points
                    
                    where exp points are added every win/loss
                    ''')

    # lvllist set to lvllist.json

    test4 = True
    while(test4):
        lvl_list = await client.wait_for("message", check=check)
        lvl_list = lvl_list.content

        if can_be_int(lvl_list):
            with open('lvllist.json', 'r') as f:
                lvl_list_dict = json.load(f)

            lvl_list_dict[str(ctx.guild.id)] = lvl_list

            with open('lvllist.json', 'w') as f:
                json.dump(lvl_list_dict, f, indent=4)

            test4 = False
        elif lvl_list.find(',') != -1:
            y = lvl_list.split(',')

            if can_list_be_int(y):
                with open('lvllist.json', 'r') as f:
                    lvl_list_dict = json.load(f)

                lvl_list_dict[str(ctx.guild.id)] = lvl_list

                with open('lvllist.json', 'w') as f:
                    json.dump(lvl_list_dict, f, indent=4)

                test4 = False
            else:
                await ctx.send("Whole set does not contain integers please try again!")
                test4 = True
        else:
            await ctx.send("Set does not contain integers please try again!")
            test4 = True


    await ctx.send('''Now lets set the experience for a win or a loss. 
                      Please write this in terms of X,Y where X is the experience for a win and Y is the experience for a loss.''')

    # exp read in
    win_loss = await client.wait_for("message", check=check)
    win_loss = win_loss.content

    # check formatting
    test5 = True
    while(test5):
        if win_loss.find(',') != -1:
            y = win_loss.split(',')

            if (can_be_int(y[0])) and (can_be_int(y[1])):
                # add to database
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET exp_for_win = ?, exp_for_loss = ? WHERE guild_id = ?")
                val = (y[0], y[1], ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The exp for a win is now {y[0]} and the exp for a loss is now {y[1]}.')

                test5 = False
            else:
                await ctx.send('The values are incorrect please try again!')
                test5 = True



    await ctx.send('''Now lets chose if you are using AC or competitive roll rules. If you are using AC rules please type AC and if you are using competitive roll rules please type COMPROLL!
    
                    The AC rules takes an AC value for the dice roll to beat. If the attack roll is better than the AC value, the attack occurs. If not, the attack fails.
                    The competitive roll rules cause a roll for the other player and compares the two values. If the attack roll is better than the dodge roll, the attack succeeds. If the dodge roll is better, the attack fails.
                    ''')

    comp_rolls = False
    test6 = True
    while(test6):
        # read in string
        ac_comp = await client.wait_for("message", check=check)
        ac_comp = ac_comp.content


        #check if correct
        if ac_comp == "AC":
            # add to rules db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET ac_comp_roll = ? WHERE guild_id = ?")
            val = (ac_comp, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test6 = False
            await ctx.send(f'The value is now {ac_comp}')

        elif ac_comp == "COMPROLL":
            # add to rules db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET ac_comp_roll = ? WHERE guild_id = ?")
            val = (ac_comp, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            comp_rolls = True
            test6 = False
            await ctx.send(f'The value is now {ac_comp}')
        else:
            await ctx.send('The string was not AC or COMPROLL. Please try again!')
            test6 = True


    # if the player chooses COMPROLL, ask about stat to add to roll
    if comp_rolls:
        await ctx.send('Since you selected to use a competitive roll system, select what stat you want the roll to be based off of.')

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()

        test7 = True
        while(test7):
            stat = await client.wait_for("message", check=check)
            stat = stat.content

            if stat == result[0]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat1", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[1]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat2", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[2]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat3", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[3]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat4", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[4]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat5", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[5]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat6", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            else:
                await ctx.send('The value is not acceptable. Please try again!')
                test7 = True


    await ctx.send('''Now that the attack roll is set. Lets set if the player can forfeit a fight as a loss. Type YES if they can and NO if they can't.''')

    test8 = True
    while (test8):
        # read in string
        forfeit_rule = await client.wait_for("message", check=check)
        forfeit_rule = forfeit_rule.content

        # check if correct
        if forfeit_rule == "YES" or forfeit_rule == "NO":
            # add to rules db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET forfeit_loss = ? WHERE guild_id = ?")
            val = (forfeit_rule, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test8 = False
            await ctx.send(f'The value is now {forfeit_rule}')
        else:
            await ctx.send("The input is incorrect! Please try again!")
            test8 = True


    await ctx.send('''Now lets set the stat that a player can add to initiative. Just type in the stats name as you typed it in while setting it.''')
    test9 = True

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
    result1 = cursor.fetchone()

    while(test9):
        # read in string
        stat_init = await client.wait_for("message", check=check)
        stat_init = stat_init.content

        # check if it matches values
        if stat_init == result1[0]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat1", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[1]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat2", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[2]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat3", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[3]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat4", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[4]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat5", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[5]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat6", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        else:
            await ctx.send("The stat does not match your stat names! Please try again!")
            test9 = True


    await ctx.send('Everything should be now set up and working!')

########################################################################################################################
#   Create/Read/Update/Delete Commands                                                                                 #
########################################################################################################################

########################################################################################################################
#  Stat table info, needs only read and update                                                                         #
########################################################################################################################

#READ
# A summary for the character stats
@client.command()
async def full_statistics_info(ctx):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT stat1, stat2, stat3, stat4, stat5, stat6, stat_dice, stat_reroll FROM stats WHERE guild_id = {ctx.guild.id}')
    result = cursor.fetchone()

    await ctx.send(f'The stats that were created are {result[0]}, {result[1]}, {result[2]}, {result[3]}, {result[4]}, {result[5]}. When the stats are rolled for a character, the dice is a {result[6]} and are re-rolled when the value is below {result[7]}.')

#fetch one thing from the table
@client.command()
async def stat_info(ctx, statInfo):
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    accepted_strings = {'stat1', 'stat2', 'stat3', 'stat4', 'stat5', 'stat6', 'stat_dice', 'stat_reroll', 'stat_list'}

    if statInfo in accepted_strings:
        if stat_info == 'stat_list':
            cursor.execute(f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()

            await ctx.send(f'The stats are {result[0]}, {result[1]}, {result[2]}, {result[3]}, {result[4]}, {result[5]},')
        else:
            cursor.execute(f'SELECT {statInfo} FROM stats WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()

            await ctx.send(f'{statInfo}: {result[0]}')
    else:
        await ctx.send('The command has the incorrect arguments.\n```stat_info [stat_list]\nThe acceptable strings are stat1, stat2, stat3, stat4, stat5, stat6 (which shows a stat name), stat_dice (which shows the dice to use), stat_reroll (which shows the value of which a stat is re-rolled during character creation), and stat_list (which shows the list of all stats).```')

@stat_info.error
async def stat_info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('The command is missing the correct arguments.\n```stat_info [stat_list]\nThe acceptable strings are stat1, stat2, stat3, stat4, stat5, stat6 (which shows a stat name), stat_dice (which shows the dice to use), stat_reroll (which shows the value of which a stat is re-rolled during character creation), and stat_list (which shows the list of all stats).  ```')
    else:
        await ctx.send('An error has occurred!')

#UPDATE
@client.command()
@commands.has_guild_permissions(administrator=True)
async def update_all_stats(ctx):
    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel

    # Stats list
    await ctx.send('''Lets give your stats a name. Stats are used to determine your characters abilities. You have six stats and must give names to all six.
                    However, if you desire, you can leave some with the name of NOTHING if you don't want it to do anything. Please format the stats name in the following manner. stat1,stat2,stat3,stat4,stat5,stat6. 
                   ''')

    # remove commas from stats
    test = True
    while (test):
        statstring = await client.wait_for("message", check=check)
        statstring = statstring.content

        if len(statstring.split(',')) != 6:
            await ctx.send('The format is incorrect please retry')
            test = True
        else:
            # DB work set stat1 - stat6 to listed values then print stat1 - stat6
            x = statstring.split(',')

            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            sql = (
                'UPDATE stats SET stat1 = ?, stat2 = ?, stat3 = ?, stat4 = ?, stat5 = ?, stat6 = ? WHERE guild_id = ?')
            val = (x[0], x[1], x[2], x[3], x[4], x[5], ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            stat1 = x[0].rstrip(',')
            stat2 = x[1].rstrip(',')
            stat3 = x[2].rstrip(',')
            stat4 = x[3].rstrip(',')
            stat5 = x[4].rstrip(',')
            stat6 = x[5].rstrip(',')

            await ctx.send(
                f'Stat values are stat1: {stat1}, stat2: {stat2}, stat3: {stat3}, stat4: {stat4}, stat5: {stat5}, stat6: {stat6}. Don\'t worry, this can be changed later if they are incorrect.')

            test = False

    # Stat point buy or dice
    await ctx.send('''Next, lets determine if you are using point buy or dice. 
                   The point buy system is where each stat is at a base of 0 and they have 10 points to distribute between each stat.
                   Dice rolls allows for a dice or multiple's of one dice to become your stats.

                   If you are using point buy, type POINTBUY and if you are using dice, type XdY where X is the number of dice and Y is the dice type.
                   ''')

    reroll = False
    test1 = True
    while (test1):
        dice = await client.wait_for("message", check=check)
        dice = dice.content

        if dice == 'POINTBUY':
            # Stat DB dice type to dice
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE stats SET stat_dice = ? WHERE guild_id = ?")
            val = (dice, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send(f'The value is now {dice}.')

            test1 = False

        else:
            if dice.find('d') != -1:
                x = dice.split('d')

                if can_be_int(x[0]) and can_be_int(x[1]):
                    if (int(x[0]) > 0) and (int(x[1]) > 0):
                        # Stat DB dice type to dice
                        db = sqlite3.connect('main.sqlite')
                        cursor = db.cursor()

                        sql = ("UPDATE stats SET stat_dice = ? WHERE guild_id = ?")
                        val = (dice, ctx.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()

                        await ctx.send(f'The value is now {dice}.')
                        test1 = False
                        reroll = True

                    else:
                        test1 = True
                        await ctx.send('One of your dice values was negative! Please try again!')
                else:
                    test1 = True
                    await ctx.send('That value is not in XdY form! Please try again!')

            else:
                test1 = True
                await ctx.send('The value does not fit the required formats! Please try again!')

    if reroll:
        await ctx.send('''Since you picked the dice rolling system, do you want to have a minimum stat value. If any dice roll is less than or equal to this value, it will be re-rolled till a better value is present.'
                       If you do not want any value, set the value to -1''')

        reroll_val = await client.wait_for("message", check=check)
        reroll_val = reroll_val.content

        # Stat DB set re-roll value
        if (can_be_int(reroll_val)):
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ('UPDATE stats SET stat_reroll = ? WHERE guild_id = ?')
            val = (reroll_val, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send(f'Re-roll value set to {reroll_val}')
        await ctx.send('All done!')


@client.command()
@commands.has_guild_permissions(administrator=True)
async def update_stat_info(ctx, statInfo, value):
    acceptable_strings = {'stat1', 'stat2', 'stat3', 'stat4', 'stat5', 'stat6', 'stat_dice', 'stat_reroll'}
    if statInfo in acceptable_strings:
        if(statInfo == 'stat1') or (statInfo == 'stat2') or (statInfo == 'stat3') or (statInfo == 'stat4') or (statInfo == 'stat5') or (statInfo == 'stat6'):
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            sql = (
                f'UPDATE stats SET {statInfo} = ? WHERE guild_id = ?')
            val = (value, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send(f'{statInfo} is now {value}')

        elif statInfo == 'stat_dice':
            if statInfo == 'POINTBUY':
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE stats SET stat_dice = ? WHERE guild_id = ?")
                val = (value, ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value for {statInfo} is now {value}')

            else:
                if value.find('d') != -1:
                    x = value.split('d')

                    if can_be_int(x[0]) and can_be_int(x[1]):
                        if (int(x[0]) > 0) and (int(x[1]) > 0):
                            db = sqlite3.connect('main.sqlite')
                            cursor = db.cursor()

                            sql = ("UPDATE stats SET stat_dice = ? WHERE guild_id = ?")
                            val = (value, ctx.guild.id)
                            cursor.execute(sql, val)
                            db.commit()
                            cursor.close()
                            db.close()

                            await ctx.send(f'The value for {statInfo} is now {value}')

                        else:
                            await ctx.send('The value for either the number of dice or the dice range is not positive')

                    else:
                        await ctx.send('The value for either the number of dice or the dice range is not an integer')

                else:
                    await ctx.send('The value is not in XdY for where X is the number of dice and Y is the range of the dice')

        elif statInfo == 'stat_reroll':
            if (can_be_int(value)):
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ('UPDATE stats SET stat_reroll = ? WHERE guild_id = ?')
                val = (value, ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'Re-roll value set to {value}')
            else:
                await ctx.send('The value is not an integer!')

        else:
            await ctx.send('''```update_stat_info [stat rule] [stat value]
            The acceptable values for stat rule are stat1, stat2, stat3, stat4, stat5, stat6 (which shows a stat name), stat_dice (which shows the dice to use), and stat_reroll (which shows the value of which a stat is re-rolled during character creation).```''')

@update_stat_info.error
async def stat_info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('''```update_stat_info [stat rule] [stat value]
            The acceptable values for stat rule are stat1, stat2, stat3, stat4, stat5, stat6 (which shows a stat name), stat_dice (which shows the dice to use), and stat_reroll (which shows the value of which a stat is re-rolled during character creation).```''')
    else:
        await ctx.send('An error has occurred!')

########################################################################################################################
#   Rules only needs read and update                                                                                   #
########################################################################################################################
#READ
@client.command()
async def view_all_rules(ctx):
    #Setting strings
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    #                             0              1            2            3              4           5               6                 7
    cursor.execute(f'SELECT num_char_allowed, level_char, exp_for_win, exp_for_loss, ac_comp_roll, comp_roll_add, forfeit_loss, stat_for_init_role FROM rules WHERE guild_id = {ctx.guild.id}')
    result = cursor.fetchone()

    cursor.execute(f'SELECT {result[5]} FROM stats WHERE guild_id = {ctx.guild.id}')
    stat_5 = cursor.fetchone()

    cursor.execute(f'SELECT {result[7]} FROM stats WHERE guild_id = {ctx.guild.id}')
    stat_7 = cursor.fetchone()

    start_rules = f'''Welcome to a server running the Turn Based Dueling Bot. This bot allows players to duel against each other to earn gold and experience. 
    To start, you would make a character. Players are allowed {result[0]} character(s). '''

    if_result_0_bigger_1 = f'''Since you are allowed more than one character, you can make a new character when the last character reaches level {result[1]}.\n'''

    rules_second = f'''This then leads into fights. Players start by having initiative rolled. This is where a d20 is rolled for you and your {stat_7[0]} stat is then added. 
    The person who rolled highest gets to go first. From there, the player who goes first can either attack with their weapon by calling ATTACK, use a spell by calling SPELL [the spell to use], 
    or use a potion by calling POTION [the potion to use]. '''

    forfeit_rules = f'''A player can type forfeit if they want to end the battle as a loss. '''

    ac_third = f'''In response to an attack, there must be a roll to attack. The system rolls a d20 to try to beat your AC, which is set by your class and any armor is added to it. '''

    comp_roll_third = f'''In response to an attack, there must be a roll to attack. The system rolls a d20 for both players where your {stat_5[0]} stat is added. If the attacking player has a higher roll, 
    then the attack works. If the defending player has a higher roll, then the attack fails. On a tie, the attack succeeds. '''

    rules_fourth = f'''A spell must be saved against. A d20 is rolled by the defending player and if they fail the save, they take the spell damage. If they succeed, they take no damage. 
    A spell save is determined by the character level added to the spells specific save stat. Some spells do not have a save, but these are for buffing a character. The player whose health hits zero loses. 
    The loser receives{result[3]} exp and the winner receives {result[2]}. '''

    main_string = start_rules + (if_result_0_bigger_1 if int(result[0]) == 1 else '') + rules_second + (forfeit_rules if result[6] == 'YES' else '') + (ac_third if result[4] == 'AC' else comp_roll_third) + rules_fourth

    await ctx.send(main_string)

@client.command()
async def read_rule_set(ctx, value):
    accepted_strings = ['characters', 'battle']

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    #                            0              1            2            3              4           5               6                 7
    cursor.execute(f'SELECT num_char_allowed, level_char, exp_for_win, exp_for_loss, ac_comp_roll, comp_roll_add, forfeit_loss, stat_for_init_role FROM rules WHERE guild_id = {ctx.guild.id}')
    result = cursor.fetchone()

    cursor.execute(f'SELECT {result[5]} FROM stats WHERE guild_id = {ctx.guild.id}')
    stat_5 = cursor.fetchone()

    cursor.execute(f'SELECT {result[7]} FROM stats WHERE guild_id = {ctx.guild.id}')
    stat_7 = cursor.fetchone()

    if value in accepted_strings:
        if value == accepted_strings[0]:
            start_rules = f'''Welcome to a server running the Turn Based Dueling Bot. This bot allows players to duel against each other to earn gold and experience. 
            To start, you would make a character. Players are allowed {result[0]} character(s). '''

            if_result_0_bigger_1 = f'''Since you are allowed more than one character, you can make a new character when the last character reaches level {result[1]}.\n'''
            main_string = start_rules + (if_result_0_bigger_1 if int(result[0]) == 1 else '')

            await ctx.send(main_string)

        elif value == accepted_strings[1]:
            rules_second = f'''Players start by having initiative rolled. This is where a d20 is rolled for you and your {stat_7[0]} stat is then added. 
            The person who rolled highest gets to go first. From there, the player who goes first can either attack with their weapon by calling ATTACK, use a spell by calling SPELL [the spell to use], 
            or use a potion by calling POTION [the potion to use]. '''

            forfeit_rules = f'''A player can type forfeit if they want to end the battle as a loss. '''

            ac_third = f'''In response to an attack, there must be a roll to attack. The system rolls a d20 to try to beat your AC, which is set by your class and any armor is added to it. '''

            comp_roll_third = f'''In response to an attack, there must be a roll to attack. The system rolls a d20 for both players where your {stat_5[0]} stat is added. If the attacking player has a higher roll, 
            then the attack works. If the defending player has a higher roll, then the attack fails. On a tie, the attack succeeds. '''

            rules_fourth = f'''A spell must be saved against. A d20 is rolled by the defending player and if they fail the save, they take the spell damage. If they succeed, they take no damage. 
            A spell save is determined by the character level added to the spells specific save stat. Some spells do not have a save, but these are for buffing a character. The player whose health hits zero loses. 
            The loser receives{result[3]} exp and the winner receives {result[2]}. '''

            main_string = rules_second + (forfeit_rules if result[6] == 'YES' else '') + (ac_third if result[4] == 'AC' else comp_roll_third) + rules_fourth

            await ctx.send(main_string)
        else:
            await ctx.send('An error has occurred.')
    else:
        await ctx.send('''The value inserted was incorrect. The command format: 
        ```read_rule_set [rule_set] where rule_set can be either characters for miscellaneous character rules or battle for battle rules```''')

@read_rule_set.error
async def read_rule_stat(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('''The value inserted was missing. The command format: 
        ```read_rule_set [rule_set] where rule_set can be either characters for miscellaneous character rules or battle for battle rules```''')
    else:
        await ctx.send('An error has occurred!')

@client.command()
async def read_specific_rule(ctx, value):
    accepted_strings = ['num_char_allowed', 'level_char', 'exp_for_win', 'exp_for_loss', 'ac_comp_roll', 'comp_roll_add', 'forfeit_loss', 'stat_for_init_role']

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    #                           0              1            2            3              4           5               6                 7
    cursor.execute(f'SELECT num_char_allowed, level_char, exp_for_win, exp_for_loss, ac_comp_roll, comp_roll_add, forfeit_loss, stat_for_init_role FROM rules WHERE guild_id = {ctx.guild.id}')
    result = cursor.fetchone()

    cursor.execute(f'SELECT {result[5]} FROM stats WHERE guild_id = {ctx.guild.id}')
    stat_5 = cursor.fetchone()

    cursor.execute(f'SELECT {result[7]} FROM stats WHERE guild_id = {ctx.guild.id}')
    stat_7 = cursor.fetchone()

    if value in accepted_strings:
        if value == accepted_strings[0]:
            await ctx.send(f'The number of characters allowed are {result[0]}')
        elif value == accepted_strings[1]:
            await ctx.send(f'The level at which your last made character must be to make a new character is {result[1]}')
        elif value == accepted_strings[2]:
            await ctx.send(f'The experienced gained per win is {result[2]}')
        elif value == accepted_strings[3]:
            await ctx.send(f'The experienced gained per loss is {result[3]}')
        elif value == accepted_strings[4]:
            await ctx.send(f'The system for deflecting a hit is {result[4]}')
        elif value == accepted_strings[5]:
            if result[4] == "AC":
                await ctx.send(f'The AC system is being used and therefore there is not stat to add to a competing roll.')
            else:
                await ctx.send(f'The stat to add to a competing defense roll is {stat_5[0]}')
        elif value == accepted_strings[6]:
            if result[6] == "YES":
                await ctx.send(f'This server uses the forfeit ruleset. This is where typing in FORFEIT will lead to a loss during a battle.')
        elif value == accepted_strings[7]:
           await ctx.send(f'The stat used during initiative is {stat_7[0]}')
        else:
            await ctx.send('An error has occurred!')
    else:
        await ctx.send('''```The value is incorrect! read_specific_rule [rule]
            The acceptable values for rule are num_char_allowed (which shows the number of characters a player can have), level_char (which shows the level the last character made must be), exp_for_win (which is the experience gained for win), exp_for_loss (which is the experience gained for a loss), ac_comp_roll (which shows if it AC rules or competitive roll rules), comp_roll_add (which shows the stat for roll if competitive role rules were set), forfeit_loss (which shows the rules for forfeit loss, if active), stat_for_init_role (which shows the stat used for initiative role).```''')

@read_specific_rule.error
async def rule_specfific_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('''```The value is missing! read_specific_rule [rule]
            The acceptable values for rule are num_char_allowed (which shows the number of characters a player can have), level_char (which shows the level the last character made must be), exp_for_win (which is the experience gained for win), exp_for_loss (which is the experience gained for a loss), ac_comp_roll (which shows if it AC rules or competitive roll rules), comp_roll_add (which shows the stat for roll if competitive role rules were set), forfeit_loss (which shows the rules for forfeit loss, if active), stat_for_init_role (which shows the stat used for initiative role).```''')
    else:
        await ctx.send('An error has occurred!')


@client.command()
@commands.has_guild_permissions(administrator=True)
async def update_all_rules(ctx):
    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel

    await ctx.send(
        '''Now lets focus on rules. First, how many characters are people allowed to have? The value must be greater than or equal to 1!''')

    character_at_level = False
    test2 = True
    while (test2):
        charNum = await client.wait_for("message", check=check)
        charNum = charNum.content
        if can_be_int(charNum):
            if int(charNum) > 1:
                # set num characters to charNum
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET num_char_allowed = ? WHERE guild_id = ?")
                val = (charNum, ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                character_at_level = True
                test2 = False
                await ctx.send(f'The number of characters has been set to {charNum}')
            elif int(charNum) == 1:
                # set num characters to charNum
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET num_char_allowed = ? WHERE guild_id = ?")
                val = (charNum, ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test2 = False
                await ctx.send(f'The number of characters has been set to {charNum}')
            else:
                await ctx.send('The value you entered is less than 0! Please try again!')
                test2 = True
        else:
            await ctx.send('The value you entered is not a number! Please try again!')
            test2 = True

    if character_at_level:
        await ctx.send(
            'Since you selected to allow more than one character, select at what level the player\'s most recent character')
        test3 = True
        while (test3):
            charlvl = await client.wait_for("message", check=check)
            charlvl = charlvl.content
            if can_be_int(charlvl):
                if int(charlvl) >= 0:
                    # DB work set level to charlvl
                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ("UPDATE rules SET level_char = ? WHERE guild_id = ?")
                    val = (charlvl, ctx.guild.id)
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

                    await ctx.send(f'The level has been set to {charlvl}')
                    test3 = False
                else:
                    await ctx.send('The level you set is to low! Please try again!')
                    test3 = True
            else:
                await ctx.send('The level you set is not a number! Please try again!')
                test3 = True
    else:
        # set level to 0
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        sql = ("UPDATE rules SET level_char = ? WHERE guild_id = ?")
        val = ("0", ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    await ctx.send('''Now lets set the experience for a win or a loss. 
                         Please write this in terms of X,Y where X is the experience for a win and Y is the experience for a loss.''')

    # exp read in
    win_loss = await client.wait_for("message", check=check)
    win_loss = win_loss.content

    # check formatting
    test5 = True
    while (test5):
        if win_loss.find(',') != -1:
            y = win_loss.split(',')

            if (can_be_int(y[0])) and (can_be_int(y[1])):
                # add to database
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET exp_for_win = ?, exp_for_loss = ? WHERE guild_id = ?")
                val = (y[0], y[1], ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The exp for a win is now {y[0]} and the exp for a loss is now {y[1]}.')

                test5 = False
            else:
                await ctx.send('The values are incorrect please try again!')
                test5 = True

    await ctx.send('''Now lets chose if you are using AC or competitive roll rules. If you are using AC rules please type AC and if you are using competitive roll rules please type COMPROLL!

                       The AC rules takes an AC value for the dice roll to beat. If the attack roll is better than the AC value, the attack occurs. If not, the attack fails.
                       The competitive roll rules cause a roll for the other player and compares the two values. If the attack roll is better than the dodge roll, the attack succeeds. If the dodge roll is better, the attack fails.
                       ''')

    comp_rolls = False
    test6 = True
    while (test6):
        # read in string
        ac_comp = await client.wait_for("message", check=check)
        ac_comp = ac_comp.content

        # check if correct
        if ac_comp == "AC":
            # add to rules db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET ac_comp_roll = ? WHERE guild_id = ?")
            val = (ac_comp, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test6 = False
            await ctx.send(f'The value is now {ac_comp}')

        elif ac_comp == "COMPROLL":
            # add to rules db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET ac_comp_roll = ? WHERE guild_id = ?")
            val = (ac_comp, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            comp_rolls = True
            test6 = False
            await ctx.send(f'The value is now {ac_comp}')
        else:
            await ctx.send('The string was not AC or COMPROLL. Please try again!')
            test6 = True

    # if the player chooses COMPROLL, ask about stat to add to roll
    if comp_rolls:
        await ctx.send(
            'Since you selected to use a competitive roll system, select what stat you want the roll to be based off of.')

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()

        test7 = True
        while (test7):
            stat = await client.wait_for("message", check=check)
            stat = stat.content

            if stat == result[0]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat1", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[1]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat2", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[2]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat3", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[3]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat4", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[4]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat5", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            elif stat == result[5]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat6", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                test7 = False
                await ctx.send(f'The value is now {stat}')
            else:
                await ctx.send('The value is not acceptable. Please try again!')
                test7 = True

    await ctx.send(
        '''Now that the attack roll is set. Lets set if the player can forfeit a fight as a loss. Type YES if they can and NO if they can't.''')

    test8 = True
    while (test8):
        # read in string
        forfeit_rule = await client.wait_for("message", check=check)
        forfeit_rule = forfeit_rule.content

        # check if correct
        if forfeit_rule == "YES" or forfeit_rule == "NO":
            # add to rules db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET forfeit_loss = ? WHERE guild_id = ?")
            val = (forfeit_rule, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test8 = False
            await ctx.send(f'The value is now {forfeit_rule}')
        else:
            await ctx.send("The input is incorrect! Please try again!")
            test8 = True

    await ctx.send(
        '''Now lets set the stat that a player can add to initiative. Just type in the stats name as you typed it in while setting it.''')
    test9 = True

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
    result1 = cursor.fetchone()

    while (test9):
        # read in string
        stat_init = await client.wait_for("message", check=check)
        stat_init = stat_init.content

        # check if it matches values
        if stat_init == result1[0]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat1", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[1]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat2", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[2]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat3", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[3]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat4", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[4]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat5", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        elif stat_init == result1[5]:
            # add to db
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            sql = ("UPDATE rules SET stat_for_init_role = ? WHERE guild_id = ?")
            val = ("stat6", ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            test9 = False
            await ctx.send(f'The value is now {stat_init}')

        else:
            await ctx.send("The stat does not match your stat names! Please try again!")
            test9 = True

    await ctx.send('Everything should be now set up and working!')

@client.command()
@commands.has_guild_permissions(administrator=True)
async def update_single_rule(ctx, rule, value):
    accepted_strings = ['num_char_allowed', 'level_char', 'exp_for_win', 'exp_for_loss', 'ac_comp_roll', 'comp_roll_add', 'forfeit_loss', 'stat_for_init_role']

    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT num_char_allowed, level_char, exp_for_win, exp_for_loss, ac_comp_roll, comp_roll_add, forfeit_loss, stat_for_init_role FROM rules WHERE guild_id = {ctx.guild.id}')
    old_data = cursor.fetchone()

    if rule in accepted_strings:
        if rule == accepted_strings[0]:
            if can_be_int(value):
                if int(value) > 0:
                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ('UPDATE rules SET num_char_allowed = ? WHERE guild_id = ?')
                    val = (value, ctx.guild.id)
                    cursor.execute(sql, val)
                    db.commit()

                    await ctx.send(f'The value is now {value}.')

                    if old_data[0] == "1" and int(value) > 1:
                        await ctx.send('Since you allowed people to use more characters, lets set the level of the last character at which they can make a new character! Set the value to zero if they are allowed to make a new character right at the beginning.')

                        level = await client.wait_for("message", check=check)
                        level = level.content

                        if can_be_int(level):
                            if level > 0:
                                sql = ('UPDATE rules SET level_char = ? WHERE guild_id = ?')
                                val = (level, ctx.guild.id)

                                cursor.execute(sql, val)
                                db.commit()
                                cursor.close()
                                db.close()

                            else:
                                await ctx.send('The level cannot be negative! The value is set to the previous value!')

                                sql = ('UPDATE rules SET level_char = ? WHERE guild_id = ?')
                                val = (old_data[1], ctx.guild.id)

                                cursor.execute(sql, val)
                                db.commit()
                                cursor.close()
                                db.close()
                        else:
                            await ctx.send('The level must be an integer! The value is set to the previous value!')

                            sql = ('UPDATE rules SET level_char = ? WHERE guild_id = ?')
                            val = (old_data[1], ctx.guild.id)

                            cursor.execute(sql, val)
                            db.commit()
                            cursor.close()
                            db.close()

                else:
                    await ctx.send('The value cannot be negative! The value is set to the previous value!')

                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ('UPDATE rules SET level_char = ? WHERE guild_id = ?')
                    val = (old_data[0], ctx.guild.id)

                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.send('The value must be an integer! The value is set to the previous value!')

                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ('UPDATE rules SET level_char = ? WHERE guild_id = ?')
                val = (old_data[0], ctx.guild.id)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

        elif rule == accepted_strings[1]:
            if can_be_int(value):
                if int(value) > 0:
                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ('UPDATE rules SET level_char = ? WHERE guild_id = ?')
                    val = (value, ctx.guild.id)

                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

                    await ctx.send(f'The value is now {value}.')

                else:
                    await ctx.send('The level cannot be negative! The value is set to the previous value!')

                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ('UPDATE rules SET level_char = ? WHERE guild_id = ?')
                    val = (old_data[1], ctx.guild.id)

                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
            else:
                await ctx.send('The value must be an integer! The value is set to the previous value!')

                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ('UPDATE rules SET level_char = ? WHERE guild_id = ?')
                val = (old_data[1], ctx.guild.id)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()


        elif rule == accepted_strings[2]:
            if can_be_int(value):
                if int(value) > 0:
                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ('UPDATE rules SET exp_for_win = ? WHERE guild_id = ?')
                    val = (value, ctx.guild.id)

                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

                    await ctx.send(f'The value is now {value}.')

                else:
                    await ctx.send('The value must greater than 1! The value is set to the previous value!')

                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ('UPDATE rules SET exp_for_win = ? WHERE guild_id = ?')
                    val = (old_data[2], ctx.guild.id)

                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
            else:
                await ctx.send('The value must be an integer! The value is set to the previous value!')

                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ('UPDATE rules SET exp_for_win = ? WHERE guild_id = ?')
                val = (old_data[2], ctx.guild.id)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

        elif rule == accepted_strings[3]:
            if can_be_int(value):
                if int(value) > 0:
                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ('UPDATE rules SET exp_for_loss = ? WHERE guild_id = ?')
                    val = (value, ctx.guild.id)

                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()

                    await ctx.send(f'The value is now {value}.')

                else:
                    await ctx.send('The value must greater than 1! The value is set to the previous value!')

                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()

                    sql = ('UPDATE rules SET exp_for_loss = ? WHERE guild_id = ?')
                    val = (old_data[3], ctx.guild.id)

                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
            else:
                await ctx.send('The value must be an integer! The value is set to the previous value!')

                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ('UPDATE rules SET exp_for_loss = ? WHERE guild_id = ?')
                val = (old_data[3], ctx.guild.id)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

        elif rule == accepted_strings[4]:
            if value == "AC" or value == "COMPROLL":
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ('UPDATE rules SET ac_comp_roll = ? WHERE guild_id = ?')
                val = (value, ctx.guild.id)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {value}.')

                if value == "COMPROLL":
                    await ctx.send(
                        'Since you selected to use a competitive roll system, select what stat you want the roll to be based off of.')

                    db = sqlite3.connect('main.sqlite')
                    cursor = db.cursor()
                    cursor.execute(
                        f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
                    result = cursor.fetchone()

                    stat = await client.wait_for("message", check=check)
                    stat = stat.content

                    if stat == result[0]:
                        db = sqlite3.connect('main.sqlite')
                        cursor = db.cursor()

                        sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                        val = ("stat1", ctx.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()


                        await ctx.send(f'The value is now {stat}')
                    elif stat == result[1]:
                        db = sqlite3.connect('main.sqlite')
                        cursor = db.cursor()

                        sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                        val = ("stat2", ctx.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()


                        await ctx.send(f'The value is now {stat}')
                    elif stat == result[2]:
                        db = sqlite3.connect('main.sqlite')
                        cursor = db.cursor()

                        sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                        val = ("stat3", ctx.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()

                        await ctx.send(f'The value is now {stat}')
                    elif stat == result[3]:
                        db = sqlite3.connect('main.sqlite')
                        cursor = db.cursor()

                        sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                        val = ("stat4", ctx.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()


                        await ctx.send(f'The value is now {stat}')
                    elif stat == result[4]:
                        db = sqlite3.connect('main.sqlite')
                        cursor = db.cursor()

                        sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                        val = ("stat5", ctx.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()


                        await ctx.send(f'The value is now {stat}')
                    elif stat == result[5]:
                        db = sqlite3.connect('main.sqlite')
                        cursor = db.cursor()

                        sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                        val = ("stat6", ctx.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()

                        await ctx.send(f'The value is now {stat}')
                    else:
                        await ctx.send('The value is not acceptable. The value will now be stat1')

                        db = sqlite3.connect('main.sqlite')
                        cursor = db.cursor()

                        sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                        val = ("stat1", ctx.guild.id)
                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()

        elif rule == accepted_strings[5]:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()

            stat = await client.wait_for("message", check=check)
            stat = stat.content

            if stat == result[0]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat1", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {stat}')
            elif stat == result[1]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat2", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {stat}')
            elif stat == result[2]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat3", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {stat}')
            elif stat == result[3]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat4", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {stat}')
            elif stat == result[4]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat5", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {stat}')
            elif stat == result[5]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat6", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {stat}')
            else:
                await ctx.send('The value is not acceptable. The value will now be stat1')

                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat1", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

        elif rule == accepted_strings[6]:
            if value == "YES" or value == "NO":
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET forfeit_loss = ? WHERE guild_id = ?")
                val = (value, ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {value}')
            else:
                await ctx.send("The input is incorrect! The value will be set to YES!")

                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET forfeit_loss = ? WHERE guild_id = ?")
                val = ('YES', ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

        elif rule == accepted_strings[7]:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(
                f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()

            if value == result[0]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat1", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {value}')
            elif value == result[1]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat2", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {value}')
            elif value == result[2]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat3", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {value}')
            elif value == result[3]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat4", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {value}')
            elif value == result[4]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat5", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {value}')
            elif value == result[5]:
                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat6", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

                await ctx.send(f'The value is now {value}')
            else:
                await ctx.send('The value is not acceptable. The value will now be stat1')

                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()

                sql = ("UPDATE rules SET comp_roll_add = ? WHERE guild_id = ?")
                val = ("stat1", ctx.guild.id)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
        else:
            await ctx.send('''```The value is incorrect! update_single_rule [rule] [value]
            The acceptable values for rule are num_char_allowed (which shows the number of characters a player can have), level_char (which shows the level the last character made must be), exp_for_win (which is the experience gained for win), exp_for_loss (which is the experience gained for a loss), ac_comp_roll (which shows if it AC rules or competitive roll rules), comp_roll_add (which shows the stat for roll if competitive role rules were set), forfeit_loss (which shows the rules for forfeit loss, if active), stat_for_init_role (which shows the stat used for initiative role).```''')

@update_single_rule.error
async def rule_single_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('''```The value is missing! update_single_rule [rule] [value]
            The acceptable values for rule are num_char_allowed (which shows the number of characters a player can have), level_char (which shows the level the last character made must be), exp_for_win (which is the experience gained for win), exp_for_loss (which is the experience gained for a loss), ac_comp_roll (which shows if it AC rules or competitive roll rules), comp_roll_add (which shows the stat for roll if competitive role rules were set), forfeit_loss (which shows the rules for forfeit loss, if active), stat_for_init_role (which shows the stat used for initiative role).```''')
    else:
        await ctx.send('An error has occurred!')


########################################################################################################################
#   Creators                                                                                                           #
########################################################################################################################
@client.command()
@commands.has_guild_permissions(administrator=True)
async def condition_creator(ctx):
    cond_name = ''
    cond_type = ''
    cond_turns = ''
    cond_damage = ''
    cond_effect_roll = ''
    cond_gain_loss = ''
    cond_effect_stat = ''
    val_changed = ''
    cond_lose_turn = ''
    desc = ''

    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel

    await ctx.send('''This command will take you through creating a command in a step-by-step manor. Lets start by giving it a name. 
    At any point, you can type EXIT to close the command. The name cannot be NONE or DONE.''')

    work1 = True
    while(work1):
        name = await client.wait_for("message", check=check)
        name = name.content

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        cursor.execute(
            f'SELECT condition_name FROM effectcond WHERE guild_id = {ctx.guild.id} AND condition_name = {name}')
        result = cursor.fetchone()

        if result is not None:
            await ctx.send('The name you picked already exists! Please select another!')
            work1 = True
        elif name == 'EXIT':
            await ctx.send('Closing...')
            return
        elif name == 'NONE':
            await ctx.send('The name cannot be NONE.')
        elif name == 'DONE':
            await ctx.send('The name cannot be DONE.')
        else:
            cond_name = name
            work1 = False

    await ctx.send('''Now, lets assign the value to the condition type. This can either be PHYSICAL or SPECIAL!''')

    work2 = True
    while(work2):
        type = await client.wait_for("message", check=check)
        type = type.content

        if type != 'PHYSICAL' or type != 'SPECIAL' or type != 'EXIT':
            await ctx.send('The value is not PHYSICAL, SPECIAL, or EXIT! Please try again!')
        else:
            if type == 'PHYSICAL' or type == 'SPECIAL':
                cond_type = type
                work2 = False
            elif type == 'EXIT':
                await ctx.send('Closing...')
                return

    await ctx.send('''The next step is to set the number of turns this effect last for. This must be in XdY form. This is where X is the number of dice and Y is the max range of dice.''')

    work3 = True
    while(work3):
        turns = await client.wait_for("message", check=check)
        turns = turns.content

        if turns == 'EXIT':
            await ctx.send('Closing...')
            return
        elif turns.find('d') == -1:
            await ctx.send('This value is not in XdY form.')
        else:
            x = turns.split('d')

            if not can_be_int(x[0]) or not can_be_int(x[1]):
                await ctx.send('The X or the Y values are not integers.')
            else:
                if int(x[0]) < 0 or int(x[1]) < 0:
                    await ctx.send('The X or Y value is negative.')
                else:
                    cond_turns = turns
                    work3 = False

    await ctx.send('''The next step is to set the damage of this effect. This must be in either NONE or XdY form. This is where X is the number of dice and Y is the max range of dice.''')

    work4 = True
    while(work4):
        damage = await client.wait_for("message", check=check)
        damage = damage.content

        if damage == 'EXIT':
            await ctx.send('Closing...')
            return
        elif damage.find('d') == -1 or damage != 'NONE':
            await ctx.send('The value is not in XdY form or NONE! Please try again!')
        elif damage.find('d') != -1:
            x = damage.split('d')

            if not can_be_int(x[0]) or not can_be_int(x[1]):
                await ctx.send('This values for X or Y are not integers! Please try again!')
            elif int(x[0]) < 0 or int(x[1]) < 0 :
                await ctx.send('The values for X or Y are negative! Please try again!')
        else:
            cond_damage = damage
            work4 = False

    await ctx.send('''The next thing to look at is the stat used to break from this condition. Please type the stat from the list of stats.''')

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()


    cursor.execute(
        f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
    res1 = cursor.fetchone()

    work5 = True
    while(work5):
        effected = await client.wait_for("message", check=check)
        effected = effected.content

        if effected == 'EXIT':
            await ctx.send('Closing...')
            return
        elif effected == res1[0]:
            cond_effect_roll = 'stat1'
            work5 = False
        elif effected == res1[1]:
            cond_effect_roll = 'stat2'
            work5 = False
        elif effected == res1[2]:
            cond_effect_roll = 'stat3'
            work5 = False
        elif effected == res1[3]:
            cond_effect_roll = 'stat4'
            work5 = False
        elif effected == res1[4]:
            cond_effect_roll = 'stat5'
            work5 = False
        elif effected == res1[5]:
            cond_effect_roll = 'stat6'
            work5 = False
        else:
            await ctx.send('The value must be a stat from the stat list!')

    await ctx.send('''This leads into the next step where you need to set if we are going to add or remove from this value on a roll. If you want to add, type GAIN or if you want to remove type LOSS.''')

    work6 = True
    while(work6):
        gain_loss = await client.wait_for("message", check=check)
        gain_loss = gain_loss.content

        if gain_loss == 'GAIN' or gain_loss == 'LOSS':
            cond_gain_loss = gain_loss
            work6 = False
        elif gain_loss == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            await ctx.send('The value was not either GAIN or LOSS! Please try again!')

    await ctx.send('''Now lets determine the stat that will be effected. This would either be HP, MP, or EP if it effects those stats or a stat from the stat list.''')

    work7 = True
    while(work7):
        stat_effected = await client.wait_for("message", check=check)
        stat_effected = stat_effected.content

        if stat_effected == 'EXIT':
            await ctx.send('Closing...')
            return
        elif stat_effected == 'HP' or stat_effected == 'MP' or stat_effected == 'EP':
            cond_effect_stat = stat_effected
            work7 = False
        elif stat_effected == res1[0]:
            cond_effect_stat = 'stat1'
            work7 = False
        elif stat_effected == res1[1]:
            cond_effect_stat = 'stat2'
            work7 = False
        elif stat_effected == res1[2]:
            cond_effect_stat = 'stat3'
            work7 = False
        elif stat_effected == res1[3]:
            cond_effect_stat = 'stat4'
            work7 = False
        elif stat_effected == res1[4]:
            cond_effect_stat = 'stat5'
            work7 = False
        elif stat_effected == res1[5]:
            cond_effect_stat = 'stat6'
            work7 = False
        else:
            await ctx.send('The value must be a stat from the stat list or HP, MP, or EP!')

    await ctx.send('Now how much will this value change by? Please type it in here and make sure it is an integer!')

    work8 = True
    while(work8):
        val_diff = await client.wait_for("message", check=check)
        val_diff = val_diff.content

        if can_be_int(val_diff):
            val_changed = val_diff
            work8 = False
        elif val_diff == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            await ctx.send('This value must be an integer! Please try again!')

    await ctx.send('Now lets gets a description written for the condition.')

    cond_lose_turn = 'NO'

    work9 = True
    while(work9):
        desc_written = await client.wait_for("message", check=check)
        desc_written = desc_written.content

        if desc_written == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            desc = desc_written
            work9 = False

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    sql = (
        'INSERT INTO effectcond(guild_id, condition_name, condition_type, condition_turns, condition_damage, condition_effect_roll, condition_gain_loss, condition_effect_stat, val_removed, cause_lose_turn, condition_desc) VALUES(?,?,?,?,?,?,?,?,?,?,?)')
    val = (ctx.guild.id, cond_name, cond_type, cond_turns, cond_damage, cond_effect_roll, cond_gain_loss, cond_effect_stat, val_changed, cond_lose_turn, desc)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()



@client.command()
@commands.has_guild_permissions(administrator=True)
async def ability_creator(ctx):
    abil_name = ''
    abil_type = ''
    buff_range = ''
    buff_cond = ''
    abil_desc = ''

    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel


    await ctx.send('''Let's create an ability. To start, let's get the name. Make sure the name is not the same as an already existing name. If you want to quit at any point, type EXIT''')

    pass1 = True
    while(pass1):
        name = await client.wait_for("message", check=check)
        name = name.content

        if name == 'EXIT':
            await ctx.send('Closing...')
            return

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        cursor.execute(
            f'SELECT ability_name FROM abilities WHERE guild_id = {ctx.guild.id} AND ability_name = {name}')
        result = cursor.fetchone()

        if result is not None:
            await ctx.send('This is an already existing ability! Please pick a new name!')
        elif name == 'NONE':
            await ctx.send('The name cannot be NONE.')
        elif name == 'DONE':
            await ctx.send('The name cannot be DONE.')
        else:
            abil_name = name
            pass1 = False

    await ctx.send('''Now let's set the type of the ability! The acceptable values are PHYSICAL or SPECIAL.''')

    pass2 = True
    while(pass2):
        type = await client.wait_for("message", check=check)
        type = type.content

        if type == 'EXIT':
            await ctx.send('Closing...')
            return
        elif type == 'PHYSICAL' or type == 'SPECIAL':
            abil_type = type
            pass2 = False
        else:
            await ctx.send('The value is not accepted. Please use either PHYSICAL or SPECIAL!')

    await ctx.send('''Next, let's determine the range of the ability. Type SELF if it effects the person or type ENEMY if it effects the enemy.''')

    pass3 = True
    while(pass3):
        range = await client.wait_for("message", check=check)
        range = range.content

        if range == 'EXIT':
            await ctx.send('Closing...')
            return
        elif range == 'SELF' or range == 'ENEMY':
            buff_range = range
            pass3 = False
        else:
            await ctx.send('The value does not match either SELF or ENEMY! Please try again!')

    await ctx.send(''''Now let's set the condition associated with the ability. The condition you type in must match a condition in your conditions list.''')

    pass4 = True
    while(pass4):
        cond = await client.wait_for("message", check=check)
        cond = cond.content

        if cond == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT condition_name FROM effectcond WHERE guild_id = {ctx.guild.id} AND condition_name = {cond}')
            res = cursor.fetchone()

            if res is not None:
                buff_cond = cond
                pass4 = False
            else:
                await ctx.send('This condition does not exist! Please type one that does.')

    await ctx.send('''Finally, let's add a description.''')

    pass5 = True
    while(pass5):
        desc = await client.wait_for("message", check=check)
        desc = desc.content

        if desc == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            abil_desc = desc
            pass5 = False

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    sql = (
        'INSERT INTO abilities(guild_id, ability_name, ability_type, buff_range, buff_condition, ability_desc) VALUES(?,?,?,?,?,?)')
    val = (ctx.guild.id, abil_name, abil_type, buff_range, buff_cond, abil_desc)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


@client.command()
@commands.has_guild_permissions(administrator=True)
async def spell_creator(ctx):
    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel

    spell_name = ''
    spell_buff_attack = ''
    spell_used_stat = ''
    spell_type = ''
    spell_range = ''
    spell_damage = ''
    spell_save = ''
    buff_deb_cond = ''
    spell_desc = ''

    attack_buff = True

    await ctx.send('''This is the spell creator. Lets start with the name of the spell. This name must not match any previously created spells. Spell names cannot be NONE or DONE. At any point, type EXIT to quit.''')

    work1 = True
    while(work1):
        name = await client.wait_for("message", check=check)
        name = name.content

        if name == 'EXIT':
            await ctx.send('Closing...')
            return

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        cursor.execute(
            f'SELECT spell_name FROM spells WHERE guild_id = {ctx.guild.id} AND spell_name = {name}')
        res = cursor.fetchone()

        if res is not None:
            await ctx.send('This spell already exists. Please try a different name.')
        elif name == 'NONE':
            await ctx.send('The name cannot be NONE.')
        elif name == 'DONE':
            await ctx.send('The name cannot be DONE.')
        else:
            spell_name = name
            work1 = False

    await ctx.send('''Now let's set if this is an attack or buff. The values to use are ATTACK or BUFF.''')

    work2 = True
    while(work2):
        att_buff = await client.wait_for("message", check=check)
        att_buff = att_buff.content

        if att_buff == 'EXIT':
            await ctx.send('Closing...')
            return
        elif att_buff == 'ATTACK':
            spell_buff_attack = att_buff
            attack_buff = True
            work2 = False
        elif att_buff == 'BUFF':
            spell_buff_attack = att_buff
            attack_buff = False
            work2 = False
        else:
            await ctx.send('This is not a valid string. Please type ATTACK or BUFF!')


    await ctx.send('''From here, let's work on setting what stat the spell adds to better the cast. This value must be one from your stat list.''')

    work4 = True
    while(work4):
        stat = await client.wait_for("message", check=check)
        stat = stat.content

        if stat == 'EXIT':
            await ctx.send('Closing...')
            return

        cursor.execute(
            f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
        stats = cursor.fetchone()

        if stat == stats[0]:
            spell_used_stat = 'stat1'
            work4 = False
        elif stat == stats[1]:
            spell_used_stat = 'stat2'
            work4 = False
        elif stat == stats[2]:
            spell_used_stat = 'stat3'
            work4 = False
        elif stat == stats[3]:
            spell_used_stat = 'stat4'
            work4 = False
        elif stat == stats[4]:
            spell_used_stat = 'stat5'
            work4 = False
        elif stat == stats[5]:
            spell_used_stat = 'stat6'
            work4 = False
        else:
            await ctx.send('The value is not a stat. Please try again!')

    await ctx.send('''Next, let's set the type of spell. The value must be PHYSICAL or SPECIAL.''')

    work3 = True
    while(work3):
        type = await client.wait_for("message", check=check)
        type = type.content

        if type == 'EXIT':
            await ctx.send('Closing...')
            return
        elif type == 'PHYSICAL' or type == 'SPECIAL':
            spell_type = type
            work3 = False

    await ctx.send('''Now, let's work on the spell range. The range can either be SELF to foucs the ability on the caster or ENEMY to focus the other player.''')

    work5 = True
    while(work5):
        range = await client.wait_for("message", check=check)
        range = range.content

        if range == 'EXIT':
            await ctx.send('Closing...')
            return
        elif range == 'SELF' or range == 'ENEMY':
            spell_range = range
            work5 = False

    await ctx.send('''Next, to set the spell you use to save. This value must be one from your stat list.''')

    work6 = True
    while(work6):
        stat = await client.wait_for("message", check=check)
        stat = stat.content

        if stat == 'EXIT':
            await ctx.send('Closing...')
            return

        cursor.execute(
            f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
        stats = cursor.fetchone()

        if stat == stats[0]:
            spell_save = 'stat1'
            work6 = False
        elif stat == stats[1]:
            spell_save = 'stat2'
            work6 = False
        elif stat == stats[2]:
            spell_save = 'stat3'
            work6 = False
        elif stat == stats[3]:
            spell_save = 'stat4'
            work6 = False
        elif stat == stats[4]:
            spell_save = 'stat5'
            work6 = False
        elif stat == stats[5]:
            spell_save = 'stat6'
            work6 = False
        else:
            await ctx.send('The value is not a stat. Please try again!')

    if (attack_buff):
        await ctx.send('''Now, since the spell is an attack, let's set the damage. This must be in a dice form of XdY where X is the count of dice and Y is the max value of the dice.''')
        buff_deb_cond = 'NONE'

        work7 = True
        while(work7):
            damage = await client.wait_for("message", check=check)
            damage = damage.content

            if damage == 'EXIT':
                await ctx.send('Closing...')
                return
            elif damage.find('d') == -1:
                await ctx.send('The value must be in XdY form! Please change the value.')
            elif damage.find('d') != -1:
                x = damage.split('d')

                if can_be_int(x[0]) and can_be_int(x[1]):
                    if int(x[0]) > 0 or int(x[1]) > 0:
                        spell_damage = damage
                        work7 = False
                    else:
                        await ctx.send('This value for X or Y are not positive! Please change the value.')
                else:
                    await ctx.send('This value for X or Y are not integers! Please change the value.')
            else:
                await ctx.send('The value must be in XdY form! Please change the value.')

    else:
        await ctx.send('''Now, since the spell is a buff or debuff, let's set the condition that effects the spell would have. This effect much match a name from the conditions database.''')
        spell_damage = 'NONE'

        work7 = True
        while(work7):
            cond = await client.wait_for("message", check=check)
            cond = cond.content

            if cond == 'EXIT':
                await ctx.send('Closing...')
                return

            cursor.execute(
                f'SELECT condition_name FROM effectcond WHERE guild_id = {ctx.guild.id} AND condition_name = {cond}')
            val_cond = cursor.fetchone()

            if val_cond is not None:
                buff_deb_cond = cond
                work7 = False
            else:
                await ctx.send('''This value is not in the conditions database.''')

    work8 = True
    while(work8):
        desc = await client.wait_for("message", check=check)
        desc = desc.content

        if desc == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            spell_desc = desc
            work8 = False

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    sql = (
        'INSERT INTO spells(guild_id, spell_name, attack_buff, spell_uses, spell_type, spell_range, spell_damage, spell_save, buff_debuff_condition, spell_desc) VALUES(?,?,?,?,?,?,?,?,?,?)')
    val = (ctx.guild.id, spell_name, spell_buff_attack, spell_used_stat, spell_type, spell_range, spell_damage, spell_save, buff_deb_cond, spell_desc)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


@client.command()
@commands.has_guild_permissions(administrator=True)
async def race_creator(ctx):
    race_name = ''
    race_hp = ''
    race_mp = ''
    race_ep = ''
    race_stat_plus_min = ''
    race_cond_immune_list = ''
    race_cond_resist_list = ''
    race_cond_vuln_list = ''
    race_abil_list = ''
    race_desc = ''

    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel

    await ctx.send('''This creates a race for characters to be. Let's start with the race name. Please make sure that the race is not the same name as other races. The value cannot be NONE or DONE. At any point, you can type EXIT to stop working.''')

    work1 = True
    while(work1):
        name = await client.wait_for("message", check=check)
        name = name.content

        if name == 'EXIT':
            await ctx.send('Closing...')
            return

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        cursor.execute(
            f'SELECT race_name FROM races WHERE guild_id = {ctx.guild.id} AND race_name = {name}')
        res1 = cursor.fetchone()

        if res1 is not None:
            await ctx.send('This name already exists. Please choose a different name!')
        elif name == 'NONE':
            await ctx.send('The name cannot be NONE.')
        elif name == 'DONE':
            await ctx.send('The name cannot be DONE.')
        else:
            race_name = name
            work1 = False

    await ctx.send('''Now let's get the race health stat. This stat must be a positive integer number.''')

    work2 = True
    while(work2):
        hp = await client.wait_for("message", check=check)
        hp = hp.content

        if hp == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(hp):
            if int(hp) > 0:
                race_hp = hp
                work2 = False
            else:
                await ctx.send('The value is not positive.')
        else:
            await ctx.send('The value is not an integer.')

    await ctx.send('''Next, let's set the mana stat. This stat must be a positive integer number.''')

    work3 = True
    while(work3):
        mp = await client.wait_for("message", check=check)
        mp = mp.content

        if mp == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(mp):
            if int(mp) > 0:
                race_mp = mp
                work3 = False
            else:
                await ctx.send('The value is not positive.')
        else:
            await ctx.send('The value is not an integer.')

    await ctx.send('''Now, let's set the energy stat. This stat must be a positive integer number.''')

    work4 = True
    while(work4):
        ep = await client.wait_for("message", check=check)
        ep = ep.content

        if ep == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(ep):
            if int(ep) > 0:
                race_ep = ep
                work3 = False
            else:
                await ctx.send('The value is not positive.')
        else:
            await ctx.send('The value is not an integer.')

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(
        f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
    stats = cursor.fetchone()

    await ctx.send(f'''Now let's work on creating the stat array. This array will contain a list of the six stats with what will be added and subtracted. 
    These values must be integers. Let's start with the value of {stats[0]}. If you are adding to the value, make the integer positive, zero if it is not changing, or negative if you are removing from it.''')

    work5 = True
    while(work5):
        stat1 = await client.wait_for("message", check=check)
        stat1 = stat1.content

        if stat1 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat1):
            race_stat_plus_min += f'{stat1},'
            work5 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[1]}.''')

    work6 = True
    while (work6):
        stat2 = await client.wait_for("message", check=check)
        stat2 = stat2.content

        if stat2 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat2):
            race_stat_plus_min += f'{stat2},'
            work6 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[2]}.''')

    work7 = True
    while (work7):
        stat3 = await client.wait_for("message", check=check)
        stat3 = stat3.content

        if stat3 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat3):
            race_stat_plus_min += f'{stat3},'
            work7 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[3]}.''')

    work8 = True
    while (work8):
        stat4 = await client.wait_for("message", check=check)
        stat4 = stat4.content

        if stat4 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat4):
            race_stat_plus_min += f'{stat4},'
            work8 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[4]}.''')

    work9 = True
    while (work9):
        stat5 = await client.wait_for("message", check=check)
        stat5 = stat5.content

        if stat5 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat5):
            race_stat_plus_min += f'{stat5},'
            work9 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[5]}.''')

    work10 = True
    while (work10):
        stat6 = await client.wait_for("message", check=check)
        stat6 = stat6.content

        if stat6 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat6):
            race_stat_plus_min += f'{stat6},'
            work10 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    race_stat_plus_min.rstrip(',')

    await ctx.send('''Now let's set the list of conditions the race is immune to. Please type in names of the condition or NONE if there is none. If there are multiple conditions, DONE when you are done.''')

    work11 = True
    while(work11):
        condition = await client.wait_for("message", check=check)
        condition = condition.content

        if condition == 'EXIT':
            await ctx.send('Closing...')
            return
        elif condition == 'NONE':
            if race_cond_immune_list == '':
                race_cond_immune_list = condition
                work11 = False
            else:
                await ctx.send('There are other values. Please type DONE instead.')
        elif condition == 'DONE':
            if not race_cond_immune_list == '':
                race_cond_immune_list.rstrip(',')
                work11 = False
            else:
                await ctx.send('There are no values. Please type NONE instead.')
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT condition_name FROM effectcond WHERE guild_id = {ctx.guild.id} AND condition_name = {condition}')
            res = cursor.fetchone()

            if res is not None:
                race_cond_immune_list += f'{condition},'


    await ctx.send('''Now let's set the list of conditions the race is resistant to. Please type in names of the condition or NONE if there is none. If there are multiple conditions, DONE when you are done.''')

    work11 = True
    while(work11):
        condition = await client.wait_for("message", check=check)
        condition = condition.content

        if condition == 'EXIT':
            await ctx.send('Closing...')
            return
        elif condition == 'NONE':
            if race_cond_resist_list == '':
                race_cond_resist_list = condition
                work11 = False
            else:
                await ctx.send('There are other values. Please type DONE instead.')
        elif condition == 'DONE':
            if not race_cond_resist_list == '':
                race_cond_resist_list.rstrip(',')
                work11 = False
            else:
                await ctx.send('There are no values. Please type NONE instead.')
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT condition_name FROM effectcond WHERE guild_id = {ctx.guild.id} AND condition_name = {condition}')
            res = cursor.fetchone()

            if res is not None:
                race_cond_resist_list += f'{condition},'

    await ctx.send('''Now let's set the list of conditions the race is vulnerable to. Vulnerable to a condition causes two times the turns effected. Please type in names of the condition or NONE if there is none. If there are multiple conditions, DONE when you are done.''')

    work11 = True
    while(work11):
        condition = await client.wait_for("message", check=check)
        condition = condition.content

        if condition == 'EXIT':
            await ctx.send('Closing...')
            return
        elif condition == 'NONE':
            if race_cond_vuln_list == '':
                race_cond_vuln_list = condition
                work11 = False
            else:
                await ctx.send('There are other values. Please type DONE instead.')
        elif condition == 'DONE':
            if not race_cond_vuln_list == '':
                race_cond_vuln_list.rstrip(',')
                work11 = False
            else:
                await ctx.send('There are no values. Please type NONE instead.')
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT condition_name FROM effectcond WHERE guild_id = {ctx.guild.id} AND condition_name = {condition}')
            res = cursor.fetchone()

            if res is not None:
                race_cond_vuln_list += f'{condition},'

    await ctx.send('''Now let's set the list of abilities the race has. Please type in names of the abilites or NONE if there is none. If there are multiple abilities, DONE when you are done.''')

    work11 = True
    while(work11):
        ability = await client.wait_for("message", check=check)
        ability = ability.content

        if ability == 'EXIT':
            await ctx.send('Closing...')
            return
        elif ability == 'NONE':
            if race_abil_list == '':
                race_abil_list = condition
                work11 = False
            else:
                await ctx.send('There are other values. Please type DONE instead.')
        elif ability == 'DONE':
            if not race_abil_list == '':
                race_abil_list.rstrip(',')
                work11 = False
            else:
                await ctx.send('There are no values. Please type NONE instead.')
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT ability_name, ability_type, buff_range, buff_condition, ability_desc FROM abilities WHERE guild_id = {ctx.guild.id} AND ability_name = {ability}')
            res = cursor.fetchone()

            if res is not None:
                race_abil_list += f'{condition},'

    await ctx.send('''Finally, let's set a description for the race. This will describe how the race looks, area, etc. This is just for role-playing aspects.''')

    work12 = True
    while(work12):
        desc = await client.wait_for("message", check=check)
        desc = desc.content

        if desc == 'EXIT':
            await ctx.send('Closing...')
            return

        race_desc = desc
        work12 = False

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    sql = (
        'INSERT INTO spells(guild_id, race_name, val_hp, val_mp, val_ep, stats_plus_min, condtion_immune, condtition_strength, condition_vulnerable, ability_list, race_description) VALUES(?,?,?,?,?,?,?,?,?,?,?)')
    val = (ctx.guild.id, race_name, race_hp, race_mp, race_ep, race_stat_plus_min, race_cond_immune_list, race_cond_resist_list, race_cond_vuln_list, race_abil_list, race_desc)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@client.command()
@commands.has_guild_permissions(administrator=True)
async def class_creator(ctx):
    class_name = ''
    class_add_sub_hp = ''
    class_add_sub_mp = ''
    class_add_sub_ep = ''
    class_add_sub_stat_list = ''
    class_spell_save = ''
    class_unarmed_attack = ''
    class_spell_list = ''
    class_start_weapon = ''
    class_start_armor = ''
    class_start_potion = ''
    class_desc = ''

    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel

    await ctx.send('''Thank you for starting to use the class creator. At any point, you can enter EXIT to close the command. Let's start by entering a name. This name must not be DONE, NONE, or match other class names.''')

    work1 = True
    while(work1):
        name = await client.wait_for("message", check=check)
        name = name.content

        if name == 'EXIT':
            await ctx.send('Closing...')
            return
        elif name == 'DONE':
            await ctx.send('The name cannot be DONE.')
        elif name == 'NONE':
            await ctx.send('The name cannot be NONE.')
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT class_name, add_sub_hp, add_sub_mp, add_sub_ep, stats_plus_min, stat_spell_save, unarmed_attack_damage, spell_array, class_ac_roll_stat, start_weapon, start_armor, start_items, class_desc FROM classes WHERE guild_id = {ctx.guild.id} AND class_name = {name}')
            res = cursor.fetchone()

            if res is not None:
                await ctx.send('This name already exits.')
            else:
                class_name = name
                work1 = False

    await ctx.send('''Now let's set the value to be added or removed from the health value. This value must be an integer.''')

    work2 = True
    while(work2):
        add_sub_hp = await client.wait_for("message", check=check)
        add_sub_hp = add_sub_hp.content

        if can_be_int(add_sub_hp):
            class_add_sub_hp = add_sub_hp
            work2 = False

    await ctx.send('''Now let's do the same for the mana value. This value must be an integer.''')

    work3 = True
    while (work3):
        add_sub_mp = await client.wait_for("message", check=check)
        add_sub_mp = add_sub_mp.content

        if can_be_int(add_sub_mp):
            class_add_sub_mp = add_sub_mp
            work3 = False

    await ctx.send('''Now let's do the same for the energy value. This value must be an integer.''')

    work3 = True
    while (work3):
        add_sub_ep = await client.wait_for("message", check=check)
        add_sub_ep = add_sub_ep.content

        if can_be_int(add_sub_ep):
            class_add_sub_ep = add_sub_ep
            work3 = False

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute(
        f'SELECT stat1, stat2, stat3, stat4, stat5, stat6 FROM stats WHERE guild_id = {ctx.guild.id}')
    stats = cursor.fetchone()

    await ctx.send(
        f'''Now let's work on creating the stat array. This array will contain a list of the six stats with what will be added and subtracted. 
        These values must be integers. Let's start with the value of {stats[0]}. If you are adding to the value, make the integer positive, zero if it is not changing, or negative if you are removing from it.''')

    work5 = True
    while (work5):
        stat1 = await client.wait_for("message", check=check)
        stat1 = stat1.content

        if stat1 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat1):
            class_add_sub_stat_list += f'{stat1},'
            work5 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[1]}.''')

    work6 = True
    while (work6):
        stat2 = await client.wait_for("message", check=check)
        stat2 = stat2.content

        if stat2 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat2):
            class_add_sub_stat_list += f'{stat2},'
            work6 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[2]}.''')

    work7 = True
    while (work7):
        stat3 = await client.wait_for("message", check=check)
        stat3 = stat3.content

        if stat3 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat3):
            class_add_sub_stat_list += f'{stat3},'
            work7 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[3]}.''')

    work8 = True
    while (work8):
        stat4 = await client.wait_for("message", check=check)
        stat4 = stat4.content

        if stat4 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat4):
            class_add_sub_stat_list += f'{stat4},'
            work8 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[4]}.''')

    work9 = True
    while (work9):
        stat5 = await client.wait_for("message", check=check)
        stat5 = stat5.content

        if stat5 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat5):
            class_add_sub_stat_list += f'{stat5},'
            work9 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    await ctx.send(f'''Now, let's set {stats[5]}.''')

    work10 = True
    while (work10):
        stat6 = await client.wait_for("message", check=check)
        stat6 = stat6.content

        if stat6 == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(stat6):
            class_add_sub_stat_list += f'{stat6},'
            work10 = False
        else:
            await ctx.send('The value is incorrect. Please try again!')

    class_add_sub_stat_list.rstrip(',')

    await ctx.send('''Let's focus on the spell save. This value is what the enemy player needs to roll against when a spell is cast. This value must be a positive integer.''')

    work11 = True
    while(work11):
        save =  await client.wait_for("message", check=check)
        save = save.content

        if save == 'EXIT':
            await ctx.send('Closing...')
            return
        elif can_be_int(save):
            if int(save) > 0:
                class_spell_save = save
                work11 = False
            else:
                await ctx.send('The value must be positive! Please try again!')
        else:
            await ctx.send('The value must be an integer! Please try again!')

    await ctx.send('''Now, let's set the classes unarmed attack dice. This value must written as XdY where X is the number of dice and Y is the max value of the dice.''')

    work12 = True
    while(work12):
        unarmed = await client.wait_for("message", check=check)
        unarmed = unarmed.context

        if unarmed == 'EXIT':
            await ctx.send('Closing...')
            return
        elif unarmed.find('d') != -1:
            x = unarmed.split('d')

            if can_be_int(x[0]) or can_be_int(x[1]):
                if int(x[0]) > 0and int(x[1]) > 0:
                    class_unarmed_attack = unarmed
                    work12 = False
                else:
                    await ctx.send('The X or Y values are not positive! Please try again!')
            else:
                await ctx.send('The X or Y values are not integers! Please try again!')
        else:
            await ctx.send('The value is not in XdY form. Please try again!')

    await ctx.send('''Now let's set what spells are associated with the class.''')

    work13 = True
    while (work13):
        spell = await client.wait_for("message", check=check)
        spell = spell.content

        if spell == 'EXIT':
            await ctx.send('Closing...')
            return
        elif spell == 'NONE':
            if class_spell_list == '':
                class_spell_list = spell
                work13 = False
            else:
                await ctx.send('There are other values. Please type DONE instead.')
        elif spell == 'DONE':
            if class_spell_list != '':
                class_spell_list.rstrip(',')
                work13 = False
            else:
                await ctx.send('There are no values. Please type NONE instead.')
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT spell_name FROM spells WHERE guild_id = {ctx.guild.id} AND spell_name = {spell}')
            res = cursor.fetchone()

            if res is not None:
                class_spell_list += f'{spell},'

    await ctx.send('''Now let's set the weapon you start with. Make sure this name matches a name from the weapons list.''')

    work14 = True
    while(work14):
        weap_name = await client.wait_for("message", check=check)
        weap_name = weap_name.content

        if weap_name == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT weapon_name FROM weapons WHERE guild_id = {ctx.guild.id} AND weapon_name = {weap_name}')
            sweap = cursor.fetchone()

            if sweap is not None:
                class_start_weapon = weap_name
                work14 = False
            else:
                await ctx.send('This name is not a weapon.')

    await ctx.send('''Now let's set the armor you start with. Make sure this name matches a name from the armor list.''')

    work15 = True
    while(work15):
        armor_name = await client.wait_for("message", check=check)
        armor_name = armor_name.content

        if armor_name == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT armor_name FROM armors WHERE guild_id = {ctx.guild.id} AND armor_name = {armor_name}')
            start_arm = cursor.fetchone()

            if start_arm is not None:
                class_start_armor = armor_name
                work15 = False
            else:
                await ctx.send('This name is not an armor.')

    await ctx.send('''Now let's set the potion you start with. Make sure this name matches a name from the potion list.''')

    work16 = True
    while(work16):
        potion_name = await client.wait_for("message", check=check)
        potion_name = potion_name.content

        if potion_name == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            cursor.execute(
                f'SELECT potion_name FROM potions WHERE guild_id = {ctx.guild.id} AND potion_name = {potion_name}')
            start_pot = cursor.fetchone()

            if start_pot is not None:
                class_start_potion = potion_name
                work16 = False
            else:
                await ctx.send('This is not a potion name. Please try again!')

    work17 = True
    while(work17):
        desc = await client.wait_for("message", check=check)
        desc = desc.content

        if desc == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            class_desc = desc
            work17 = False

    sql = (
        'INSERT INTO spells(guild_id, class_name, add_sub_hp, add_sub_mp, add_sub_ep, stats_plus_min, stat_spell_save, unarmed_attack_damage, spell_array, class_ac_roll_stat, start_weapon, start_armor, start_items, class_desc) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
    val = (ctx.guild.id, class_name, class_add_sub_hp, class_add_sub_mp, class_add_sub_ep, class_add_sub_stat_list, class_spell_save, class_unarmed_attack, class_spell_list, class_start_weapon, class_start_armor, class_start_potion, class_desc)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

@commands.command()
async def create_character(ctx):
    userid = ctx.message.author.id
    char_name = ''
    char_class = ''
    char_race = ''
    char_stat_list = ''
    char_desc = ''

    def check(amsg):
        return amsg.author == ctx.author and amsg.channel == ctx.channel

    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()

    cursor.execute(f'SELECT COUNT(character_name) FROM characters WHERE guild_id = {ctx.guild.id} AND user_id = {userid}')
    res1 = cursor.fetchone()

    cursor.execute(f'SELECT num_char_allowed FROM rules WHERE guild_id = {ctx.guild.id}')
    res2 = cursor.fetchone()

    if res1[0] >= res2[0]:
        await ctx.send('You already have hit the max number of characters! Closing...')
        return

    await ctx.send('''This command is a custom build character generator. This will act as a step-by-step guide to building a character. At any point, you can type EXIT to quit the command. Additionally, there is a two minute timeout for each prompt.
    Let's start with a name for the character. The name cannot be EXIT, DONE, or NONE.''')

    work1 = True
    while(work1):
        try:
            name = await client.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to type a name! Closing...')
            return
        name = name.content

        if name == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            cursor.execute(
                f'SELECT character_name FROM characters WHERE guild_id = {ctx.guild.id} AND user_id = {userid} AND character_name = {name}')
            res = cursor.fetchone()

            if res is not None:
                await ctx.send('This name is the same as another of your characters. Please try again!')
            else:
                char_name = name
                work1 = False

    await ctx.send('''Now that a name is selected, let's pick a race. Make sure the race exists in the game.''')

    work2 = True
    while(work2):
        try:
            race = await client.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to type a race! Closing...')
            return
        race = race.content

        if race == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            cursor.execute(
                f'SELECT race_name FROM races WHERE guild_id = {ctx.guild.id} AND race_name = {race}')
            res = cursor.fetchone()

            if res is not None:
                char_race = race
                work2 = False
            else:
                await ctx.send('This race does not exist! Please try again!')

    await ctx.send('''Now let's pick a class. Make sure the class exists in the game.''')

    work3 = True
    while(work3):
        try:
            class_val = await client.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to type a race! Closing...')
            return
        class_val = class_val.content

        if class_val == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            cursor.execute(
                f'SELECT class_name FROM classes WHERE guild_id = {ctx.guild.id} AND class_name = {class_val}')
            res = cursor.fetchone()

            if res is not None:
                char_class = class_val
                work3 = False
            else:
                await ctx.send('This class does not exist! Please try agian!')

    cursor.execute(
        f'SELECT stat1, stat2, stat3, stat4, stat5, stat6, stat_dice, stat_reroll FROM stats WHERE guild_id = {ctx.guild.id}')
    stat_rules = cursor.fetchone()

    cursor.execute(
        f'SELECT stats_plus_min FROM characters WHERE guild_id = {ctx.guild.id} AND user_id = {userid} AND character_name = {char_class}')
    class_add_sub = cursor.fetchone()

    cursor.execute(
        f'SELECT stats_plus_min FROM races WHERE guild_id = {ctx.guild.id} AND race_name = {char_race}')
    race_add_sub = cursor.fetchone()

    statl = stat_rules[0]
    stat2 = stat_rules[1]
    stat3 = stat_rules[2]
    stat4 = stat_rules[3]
    stat5 = stat_rules[4]
    stat6 = stat_rules[5]

    class_stat = class_add_sub[0].split(',')
    race_stat = race_add_sub[0].split(',')

    stat1_add = int(class_stat[0]) + int(race_stat[0])
    stat2_add = int(class_stat[1]) + int(race_stat[1])
    stat3_add = int(class_stat[2]) + int(race_stat[2])
    stat4_add = int(class_stat[3]) + int(race_stat[3])
    stat5_add = int(class_stat[4]) + int(race_stat[4])
    stat6_add = int(class_stat[5]) + int(race_stat[5])

    if stat_rules[6] == 'POINTBUY':
        current_points = 10
        await ctx.send(f'''The server uses a point buy system. You are given ten points to distribute amongst the six stats. To start, lets work on {statl} Remember, you will have {stat1_add} added to the value.''')

        work4 = True
        while(work4):
            try:
                stat1_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat1_val = stat1_val.content

            if stat1_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat1_val):
                if int(stat1_val) > 0:
                    if current_points >= stat1_val:
                        stat1_val_int = int(stat1_val)
                        current_points -= stat1_val_int
                        stat1_val_int += stat1_add
                        char_stat_list += f'{str(stat1_val_int)},'
                    else:
                        await ctx.send('The value you entered is greater than the current number of points! Please try again!')
                else:
                    await ctx.send('The value you entered is not positive! Please try again!')
            else:
                await ctx.send('The value you entered is not an integer! Please try again!')

        await ctx.send(f'''Now, lets set the stat {stat2}. Remember, you will have {stat2_add}.''')

        work4 = True
        while(work4):
            try:
                stat2_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat2_val = stat2_val.content

            if stat2_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat2_val):
                if int(stat2_val) > 0:
                    if current_points >= int(stat2_val):
                        stat2_val_int = int(stat2_val)
                        current_points -= stat2_val_int
                        stat2_val_int += stat2_add
                        char_stat_list += f'{str(stat2_val_int)},'
                    else:
                        await ctx.send('The value you entered is greater than the current number of points! Please try again!')
                else:
                    await ctx.send('The value you entered is not positive! Please try again!')
            else:
                await ctx.send('The value you entered is not an integer! Please try again!')

        await ctx.send(f'''Now, lets set the stat {stat3}. Remember, you will have {stat3_add}.''')

        work4 = True
        while(work4):
            try:
                stat3_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat3_val = stat3_val.content

            if stat3_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat3_val):
                if int(stat3_val) > 0:
                    if current_points >= int(stat3_val):
                        stat3_val_int = int(stat3_val)
                        current_points -= stat3_val_int
                        stat3_val_int += stat3_add
                        char_stat_list += f'{str(stat3_val_int)},'
                    else:
                        await ctx.send('The value you entered is greater than the current number of points! Please try again!')
                else:
                    await ctx.send('The value you entered is not positive! Please try again!')
            else:
                await ctx.send('The value you entered is not an integer! Please try again!')

        await ctx.send(f'''Now, lets set the stat {stat4}. Remember, you will have {stat4_add}.''')

        work4 = True
        while(work4):
            try:
                stat4_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat4_val = stat4_val.content

            if stat4_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat4_val):
                if int(stat4_val) > 0:
                    if current_points >= int(stat4_val):
                        stat4_val_int = int(stat4_val)
                        current_points -= stat4_val_int
                        stat4_val_int += stat4_add
                        char_stat_list += f'{str(stat4_val_int)},'
                    else:
                        await ctx.send('The value you entered is greater than the current number of points! Please try again!')
                else:
                    await ctx.send('The value you entered is not positive! Please try again!')
            else:
                await ctx.send('The value you entered is not an integer! Please try again!')

        await ctx.send(f'''Now, lets set the stat {stat5}. Remember, you will have {stat5_add}.''')

        work4 = True
        while (work4):
            try:
                stat5_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat5_val = stat5_val.content

            if stat5_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat5_val):
                if int(stat5_val) > 0:
                    if current_points >= int(stat5_val):
                        stat5_val_int = int(stat5_val)
                        current_points -= stat5_val_int
                        stat5_val_int += stat5_add
                        char_stat_list += f'{str(stat5_val_int)},'
                    else:
                        await ctx.send(
                            'The value you entered is greater than the current number of points! Please try again!')
                else:
                    await ctx.send('The value you entered is not positive! Please try again!')
            else:
                await ctx.send('The value you entered is not an integer! Please try again!')

        await ctx.send(f'''Now, lets set the stat {stat6}. Remember, you will have {stat6_add}.''')

        work4 = True
        while (work4):
            try:
                stat6_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat6_val = stat6_val.content

            if stat6_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat6_val):
                if int(stat6_val) > 0:
                    if current_points >= int(stat6_val):
                        stat6_val_int = int(stat6_val)
                        current_points -= stat6_val_int
                        stat6_val_int += stat6_add
                        char_stat_list += f'{str(stat6_val_int)}'
                    else:
                        await ctx.send(
                            'The value you entered is greater than the current number of points! Please try again!')
                else:
                    await ctx.send('The value you entered is not positive! Please try again!')
            else:
                await ctx.send('The value you entered is not an integer! Please try again!')

        await ctx.send(f'The stats list is now {char_stat_list}.')

    elif stat_rules[6].find('d') != -1:
        await ctx.send(f'''This server uses a dice roll system. This is where a dice is rolled for each stat and then the class values are applied to each stat. Let's start with rolling the stats.''')

        def roll_stat(x):
            reroll = True
            while(reroll):
                x = roll(stat_rules[6])
                if x > int(stat_rules[7]):
                    reroll = False
                else:
                    reroll = True

        stat1_roll = 0
        stat2_roll = 0
        stat3_roll = 0
        stat4_roll = 0
        stat5_roll = 0
        stat6_roll = 0

        roll_stat(stat1_roll)
        roll_stat(stat2_roll)
        roll_stat(stat3_roll)
        roll_stat(stat4_roll)
        roll_stat(stat5_roll)
        roll_stat(stat6_roll)

        stat_rolls = [stat1_roll, stat2_roll, stat3_roll, stat4_roll, stat5_roll, stat6_roll]

        await ctx.send(f'''The dice roll values you got are {stat_rolls[0]}, {stat_rolls[1]}, {stat_rolls[2]}, {stat_rolls[3]}, {stat_rolls[4]}, {stat_rolls[5]}. Let's now assign those values starting with {statl}. 
        Remember, {stat1_add} will be added to the roll.''')

        work4 = True
        while(work4):
            try:
                stat1_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat1_val = stat1_val.content

            if stat1_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat1_val):
                if int(stat1_val) in stat_rolls:
                    stat1_val_int = int(stat1_val)
                    stat1_val_int += stat1_add
                    char_stat_list += f'{str(stat1_val_int)},'
                else:
                    await ctx.send('The value you entered is not in the list! Please type a different value!')
            else:
                await ctx.send('The value must be an integer! Please type a different value!')

        await ctx.send(f'''Now, lets set the stat {stat2}. Remember, you will have {stat2_add}.''')

        work4 = True
        while (work4):
            try:
                stat2_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat2_val = stat2_val.content

            if stat2_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat2_val):
                if int(stat2_val) in stat_rolls:
                    stat2_val_int = int(stat2_val)
                    stat2_val_int += stat2_add
                    char_stat_list += f'{str(stat2_val_int)},'
                else:
                    await ctx.send('The value you entered is not in the list! Please type a different value!')
            else:
                await ctx.send('The value must be an integer! Please type a different value!')

        await ctx.send(f'''Now, lets set the stat {stat3}. Remember, you will have {stat3_add}.''')

        work4 = True
        while (work4):
            try:
                stat3_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat3_val = stat3_val.content

            if stat3_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat3_val):
                if int(stat3_val) in stat_rolls:
                    stat3_val_int = int(stat3_val)
                    stat3_val_int += stat3_add
                    char_stat_list += f'{str(stat3_val_int)},'
                else:
                    await ctx.send('The value you entered is not in the list! Please type a different value!')
            else:
                await ctx.send('The value must be an integer! Please type a different value!')

        await ctx.send(f'''Now, lets set the stat {stat4}. Remember, you will have {stat4_add}.''')

        work4 = True
        while (work4):
            try:
                stat4_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat4_val = stat4_val.content

            if stat4_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat4_val):
                if int(stat4_val) in stat_rolls:
                    stat4_val_int = int(stat4_val)
                    stat4_val_int += stat4_add
                    char_stat_list += f'{str(stat4_val_int)},'
                else:
                    await ctx.send('The value you entered is not in the list! Please type a different value!')
            else:
                await ctx.send('The value must be an integer! Please type a different value!')

        await ctx.send(f'''Now, lets set the stat {stat5}. Remember, you will have {stat5_add}.''')

        work4 = True
        while (work4):
            try:
                stat5_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat5_val = stat5_val.content

            if stat5_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat5_val):
                if int(stat5_val) in stat_rolls:
                    stat5_val_int = int(stat5_val)
                    stat5_val_int += stat5_add
                    char_stat_list += f'{str(stat5_val_int)},'
                else:
                    await ctx.send('The value you entered is not in the list! Please type a different value!')
            else:
                await ctx.send('The value must be an integer! Please type a different value!')

        await ctx.send(f'''Now, lets set the stat {stat6}. Remember, you will have {stat6_add}.''')

        work4 = True
        while (work4):
            try:
                stat6_val = await client.wait_for("message", timeout=120, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You took too long to type a value! Closing...')
                return
            stat6_val = stat6_val.content

            if stat6_val == 'EXIT':
                await ctx.send('Closing...')
                return
            elif can_be_int(stat6_val):
                if int(stat6_val) in stat_rolls:
                    stat6_val_int = int(stat6_val)
                    stat6_val_int += stat6_add
                    char_stat_list += f'{str(stat6_val_int)}'
                else:
                    await ctx.send('The value you entered is not in the list! Please type a different value!')
            else:
                await ctx.send('The value must be an integer! Please type a different value!')

    else:
        await ctx.send('An error has occurred, please message the server admin and ask them to change the dice roll.')
        return


    await ctx.send('''Now let's set the character description. Here, you can share the looks and personality of the character. This only has barring on roleplay.''')

    work5 = True
    while(work5):
        try:
            desc = await client.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to type a value! Closing...')
            return
        desc = desc.content

        if desc == 'EXIT':
            await ctx.send('Closing...')
            return
        else:
            char_desc = desc

    cursor.execute(f'SELECT COUNT(character_name) FROM characters WHERE guild_id = {ctx.guild.id} AND user_id = {user}')
    res1 = cursor.fetchone()

    num_char = int(res1[0])+1

    cursor.execute(
        f'SELECT start_weapon, start_armor, start_items, FROM classes WHERE guild_id = {ctx.guild.id} AND class_name = {char_class}')
    items = cursor.fetchone()

    sql = (
        'INSERT INTO characters(guild_id, user_id, character_number, character_name, class_id, race_id, stat_list, weapon_id, armor_id, item_id_list, level, exp, character_desc) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)')
    val = (
    ctx.guild.id, userid, num_char, char_name, char_class, char_race, char_stat_list, items[0], items[1], items[2], '1', '0',
    char_desc)

    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()


########################################################################################################################
#   Cog Data                                                                                                           #
########################################################################################################################
@client.command()
@commands.has_guild_permissions(administrator=True)
async def load_cog(ctx, extention):
    client.load_extension(f'cogs.{extention}')

@load_cog.error
async def load_cog_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing the cog to load!')
    else:
        await ctx.send('An error has occurred!')


@client.command()
@commands.has_guild_permissions(administrator=True)
async def unload_cog(ctx, extention):
    client.unload_extension(f'cogs.{extention}')

@unload_cog.error
async def unload_cog_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing the cog to unload!')
    else:
        await ctx.send('An error has occurred!')

@client.command()
@commands.has_guild_permissions(administrator=True)
async def reload_cog(ctx, extention):
    client.unload_extension(f'cogs.{extention}')
    client.load_extension(f'cogs.{extention}')

@reload_cog.error
async def reload_cog_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You are missing the cog to reload!')
    else:
        await ctx.send('An error has occurred!')

########################################################################################################################
#   OTHER IMPORTANT CODE                                                                                               #
########################################################################################################################

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)