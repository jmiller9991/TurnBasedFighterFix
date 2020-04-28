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
            class_ac_roll_stat TEXT,
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
            weapon_plus_damage TEXT,
            weapon_damage_type TEXT,
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
    # TODO tell people how to make a character
    print(f'{member} has joined the server!!!!!!! WELCOME!!!!')


@client.event
async def on_member_remove(member):
    # TODO remove user items where server
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
        await ctx.send('Since you selected to allow more than one character, select at what level the player\'s most recent character')
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
                    This would mean the string 1,2,3,5,7,9,10,12 would be equal to:
                    
                    Level 1 >> Level 2 requires 1 exp point
                    Level 2 >> Level 3 requires 2 exp points
                    Level 3 >> Level 4 requires 3 exp points
                    Level 5 >> Level 6 requires 5 exp points
                    Level 6 >> Level 7 requires 7 exp points
                    Level 7 >> Level 8 requires 9 exp points
                    Level 8 >> Level 9 requires 10 exp points
                    Level 9 >> Level 10 requires 12 exp points
                    
                    where exp points are added every win/loss
                    ''')

    # lvllist set to lvllist.json

    def can_list_be_int(string_list):
        correct = True
        for i in string_list:
            if can_be_int(i):
                correct = True
            else:
                return False
        return correct

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

    #                                      0              1            2            3              4           5               6                 7
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

client.run('NjY5MDI4MTYwNzc5ODQ1NjUy.XqEYjQ.p_wYV-9h6vIEb5XR-j0l7W64sSY')