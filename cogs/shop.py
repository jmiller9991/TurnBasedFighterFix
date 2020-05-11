import discord
import random
import json
from discord.ext import commands, tasks
from itertools import cycle
import sqlite3
import asyncio
import math

########################################################################################################################
#   Shop Class                                                                                                         #
#                                                                                                                      #
#   This class is to manage all commands related to shops and item creation.                                           #
#   This class will do the create/read/update/delete (CRUD) of items and player inventory.                             #
########################################################################################################################

########################################################################################################################
#   Other Codes                                                                                                        #
########################################################################################################################
async def can_be_int(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

async def can_list_be_int(string_list):
    correct = True
    for i in string_list:
        if can_be_int(i):
            correct = True
        else:
            return False
    return correct

async def get_val_from_json(ctx, file):
    with open(file, 'r') as f:
        val = json.load(f)

    return val[str(ctx.guild.id)]

class Shop(commands.Cog):
    ####################################################################################################################
    #   Necessary Code                                                                                                 #
    ####################################################################################################################
    def __init__(self, client):
        self.client = client

    ####################################################################################################################
    #   Gold                                                                                                           #
    ####################################################################################################################
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def give_gold(self, ctx, user:discord.Member, amount):
        userid = user.id
        guildid = ctx.guild.id
        gold_value = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(f'SELECT gold FROM guild_id = ? AND user_id = ?')
        gold = cursor.fetchone()

        if gold is not None:
            if can_be_int(gold[0]):
                gold_val = int(gold[0])

                if can_be_int(amount):
                    if int(amount) > 0:
                        gold_val += amount
                        gold_value = str(gold_value)
                    else:
                        await ctx.send('The amount you entered in gold is not positive.')
                else:
                    await ctx.send('The amount you entered is not an integer.')
            else:
                await ctx.send('The current gold value has an error in it.')
        else:
            await ctx.send('There is no gold value set up for this player!')

        sql = ('UPDATE player_gold SET gold = ? WHERE guild_id = ? AND user_id = ?')
        val = (gold_value, guildid, userid)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @give_gold.error
    async def give_gold_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''The required arguments are missing!
            ```give_gold [user] [amount]
            where user is a mention to the user
            where amount is the amount to add```''')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def remove_gold(self, ctx, user: discord.Member, amount):
        userid = user.id
        guildid = ctx.guild.id
        gold_value = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(f'SELECT gold FROM guild_id = ? AND user_id = ?', vals)
        gold = cursor.fetchone()

        if gold is not None:
            if can_be_int(gold[0]):
                gold_val = int(gold[0])

                if can_be_int(amount):
                    if int(amount) > 0:
                        gold_val -= amount
                        gold_value = str(gold_value)
                    else:
                        await ctx.send('The amount you entered in gold is not positive.')
                else:
                    await ctx.send('The amount you entered is not an integer.')
            else:
                await ctx.send('The current gold value has an error in it.')
        else:
            await ctx.send('There is no gold value set up for this player!')

        if int(gold_value) < 0:
            await ctx.send('Gold has been set to a negative number. Please try a different value!')
            return
        else:
            sql = ('UPDATE player_gold SET gold = ? WHERE guild_id = ? AND user_id = ?')
            val = (gold_value, guildid, userid)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @remove_gold.error
    async def remove_gold_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''The required arguments are missing!
            ```remove_gold [user] [amount]
            where user is a mention to the user
            where amount is the amount to remove```''')
        else:
            await ctx.send('''An error has occurred!
            ```remove_gold [user] [amount]
            where user is a mention to the user
            where amount is the amount to remove```''')

    @commands.command()
    async def show_gold_amount(self, ctx):
        userid = ctx.author.id
        guildid = ctx.guild.id

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(f'SELECT gold FROM guild_id = ? AND user_id = ?', vals)
        gold = cursor.fetchone()

        gold_name = get_val_from_json(ctx, 'goldname.json')

        await ctx.send(f'''You have {gold[0]} {gold_name}.''')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def show_player_gold(self, ctx, user:discord.Member):
        userid = user.id
        guildid = ctx.guild.id
        ment = user.mention

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(f'SELECT gold FROM guild_id = ? AND user_id = ?', vals)
        gold = cursor.fetchone()

        gold_name = get_val_from_json(ctx, 'goldname.json')

        await ctx.send(f'''{ment} has {gold[0]} {gold_name}.''')

    @show_player_gold.error
    async def show_player_gold_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('''The command is missing the required arguments!
            ```show_player_gold [user]
            where user is a mention of a user```''')
        else:
            await ctx.send('''An error has occurred!
            ```show_player_gold [user]
            where user is a mention of a user```''')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def set_player_gold_to_zero(self, ctx, user:discord.Member):
        userid = user.id
        guildid = ctx.guild.id
        ment = user.mention
        gold_name = get_val_from_json(ctx, 'goldname.json')

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(f'SELECT gold FROM guild_id = ? AND user_id = ?', vals)
        gold = cursor.fetchone()

        if gold is not None:
            sql = ('UPDATE player_gold SET gold = ? WHERE guild_id = ? AND user_id = ?')
            val = ('0', guildid, userid)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send(f'{ment} now has 0 {gold_name}')
        else:
            await ctx.send(f'{ment} does not have database set up.')

    ####################################################################################################################
    #   PLAYER INVENTORY                                                                                               #
    ####################################################################################################################
    ####################################################################################################################
    #   Player Weapons                                                                                                 #
    ####################################################################################################################
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def add_weapon(self, ctx, user:discord.Member, *, weapon):
        guildid = ctx.guild.id
        userid = user.id
        ment = user.mention

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, weapon)
        cursor.execute(
            f'SELECT weapon_name FROM weapons WHERE guild_id = ? AND weapon_name = ?', vals)
        weap = cursor.fetchone()

        if weap is not None:
            vals = (guildid, userid, weapon)
            cursor.execute(
                f'SELECT weapon_name FROM player_weapon WHERE guild_id = ? AND user_id = ? AND weapon_name = ?', vals)
            weapon = cursor.fetchone()

            if weapon is None:
                sql = ('INSERT INTO player_weapon(guild_id, user_id, weapon_name) VALUES(?, ?, ?)')
                val = (guildid, userid, weapon)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
            else:
                await ctx.send(f'{ment} already has {weapon}')
        else:
            await ctx.send(f'{weapon} does not exist.')

    @add_weapon.error
    async def add_weapon_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''An argument is missing!
            ```add_weapon [user] [weapon]
            where user is a mention to a user
            where weapon is a weapon from the weapons list```''')


    @commands.command()
    async def show_weapon_inv_list(self, ctx):
        userid = ctx.author.id
        guildid = ctx.guild.id
        weapons = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(
            f'SELECT weapon_name FROM player_weapon WHERE guild_id = ? AND user_id = ?', vals)
        weapon = cursor.fetchall()

        if weapon is not None:
            for i in weapon:
                weapons += f'{i}\n'
        else:
            await ctx.send('You own no weapons.')
            return

        ctx.send(weapons)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def show_player_weapon_list(self, ctx, user: discord.Member):
        userid = user.id
        guildid = ctx.guild.id
        ment = user.mention
        weapons = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(
            f'SELECT weapon_name FROM player_weapon WHERE guild_id = ? AND user_id = ?', vals)
        weapon = cursor.fetchall()

        if weapon is not None:
            for i in weapon:
                weapons += f'{i}\n'
        else:
            await ctx.send(f'{ment} owns no weapons.')
            return

        await ctx.send(weapons)

    @show_player_weapon_list.error
    async def show_player_inv_weapon_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''You are missing an argument!
            ```show_player_weapon_list [user]
            where user is the mention of a user```''')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def remove_weapon(self, ctx, user: discord.Member, *, weapon):
        userid = user.id
        guildid = ctx.guild.id
        ment = user.mention

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid, weapon)
        cursor.execute(
            f'SELECT weapon_name FROM player_weapon WHERE guild_id = ? AND user_id = ? AND weapon_name = ?', vals)
        weap = cursor.fetchone()

        if weap is not None:
            sql = ('DELETE FROM player_weapon WHERE guild_id = ? AND user_id = ? AND weapon_name = ?')
            val = (guildid, userid, weapon)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send(f'{ment} had weapon {weapon} removed.')
        else:
            await ctx.send(f'{ment} does not have {weapon}.')

    @remove_weapon.error
    async def remove_weapon_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('''You are missing an argument!
            ```remove_weapon [user] [weapon]
            where user is the user you want to remove from
            where weapon is the weapon to remove```''')

    ####################################################################################################################
    #   PLayer Armor                                                                                                   #
    ####################################################################################################################
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def add_armor(self, ctx, user: discord.Member, *, armor):
        guildid = ctx.guild.id
        userid = user.id
        ment = user.mention

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, armor)
        cursor.execute(
            f'SELECT armor_name FROM armors WHERE guild_id = ? AND armor_name = ?', vals)
        arm = cursor.fetchone()

        if arm is not None:
            vals = (guildid, userid, armor)
            cursor.execute(
                f'SELECT armor_name FROM player_armor WHERE guild_id = ? AND user_id = ? AND armor_name=?', vals)
            armors = cursor.fetchone()

            if armors is None:
                sql = ('INSERT INTO player_armor(guild_id, user_id, armor_name) VALUES(?, ?, ?)')
                val = (guildid, userid, armor)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
            else:
                await ctx.send(f'{ment} already has {armor}')
        else:
            await ctx.send(f'{armor} does not exist.')

    @add_armor.error
    async def add_armor_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''An argument is missing!
            ```add_armor [user] [armor]
            where user is a mention to a user
            where armor is an armor from the armors list```''')


    @commands.command()
    async def show_armor_inv_list(self, ctx):
        userid = ctx.author.id
        guildid = ctx.guild.id
        armors = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(
            f'SELECT armor_name FROM player_armor WHERE guild_id = ? AND user_id = ?', vals)
        armor = cursor.fetchall()

        if armor is not None:
            for i in armor:
                armors += f'{i}\n'
        else:
            await ctx.send('You own no armor.')
            return

        await ctx.send(armors)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def show_player_armor_list(self, ctx, user: discord.Member):
        userid = user.id
        guildid = ctx.guild.id
        ment = user.mention
        armors = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(
            f'SELECT armor_name FROM player_armor WHERE guild_id = / AND user_id = ?', vals)
        armor = cursor.fetchall()

        if armor is not None:
            for i in armor:
                armors += f'{i}\n'
        else:
            await ctx.send(f'{ment} owns no armor.')
            return

        await ctx.send(armors)

    @show_player_armor_list.error
    async def show_player_inv_armor_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''You are missing an argument!
            ```show_player_armor_list [user]
            where user is the mention of a user```''')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def remove_armor(self, ctx, user: discord.Member, *, armor):
        userid = user.id
        guildid = ctx.guild.id
        ment = user.mention

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid, armor)
        cursor.execute(
            f'SELECT armor_name FROM player_armor WHERE guild_id = ? AND user_id = ? AND armor_name = ?', vals)
        armors = cursor.fetchone()

        if armors is not None:
            sql = ('DELETE FROM player_armor WHERE guild_id = ? AND user_id = ? AND armor_name = ?')
            val = (guildid, userid, armor)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send(f'{ment} had armor {armor} removed.')
        else:
            await ctx.send(f'{ment} does not have {armor}.')

    @remove_armor.error
    async def remove_armor_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('''You are missing an argument!
            ```remove_armor [user] [armor]
            where user is the user you want to remove from
            where armor is the armor to remove```''')

    ####################################################################################################################
    #   Player Potion                                                                                                  #
    ####################################################################################################################
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def add_potion(self, ctx, user: discord.Member, *, potion):
        guildid = ctx.guild.id
        userid = user.id
        ment = user.mention

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, potion)
        cursor.execute(
            f'SELECT potion_name FROM potions WHERE guild_id = ? AND potion_name = ?', vals)
        pot = cursor.fetchone()

        if pot is not None:
            vals = (guildid, userid, potion)
            cursor.execute(
                f'SELECT potion_name FROM player_potion WHERE guild_id = ? AND user_id = ? AND potion_name = ?', vals)
            potions = cursor.fetchone()

            if potions is None:
                sql = ('INSERT INTO player_potion(guild_id, user_id, potion_name) VALUES(?, ?, ?)')
                val = (guildid, userid, potion)

                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
            else:
                await ctx.send(f'{ment} already has {potion}')
        else:
            await ctx.send(f'{potion} does not exist.')

    @add_armor.error
    async def add_potion_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''An argument is missing!
            ```add_potion [user] [potion]
            where user is a mention to a user
            where potion is an potion from the potions list```''')


    @commands.command()
    async def show_potion_inv_list(self, ctx):
        userid = ctx.author.id
        guildid = ctx.guild.id
        potions = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(
            f'SELECT potion_name FROM player_potion WHERE guild_id = ? AND user_id = ?', vals)
        potion = cursor.fetchall()

        if potion is not None:
            for i in potion:
                potions += f'{i}\n'
        else:
            await ctx.send('You own no potions.')
            return

        await ctx.send(potions)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def show_player_potion_list(self, ctx, user: discord.Member):
        userid = user.id
        guildid = ctx.guild.id
        ment = user.mention
        potions = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid)
        cursor.execute(
            f'SELECT potion_name FROM player_potion WHERE guild_id = ? AND user_id = ?')
        potion = cursor.fetchall()

        if potion is not None:
            for i in potion:
                potions += f'{i}\n'
        else:
            await ctx.send(f'{ment} owns no potion.')
            return

        await ctx.send(potions)

    @show_player_potion_list.error
    async def show_player_inv_potion_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''You are missing an argument!
            ```show_player_potion_list [user]
            where user is the mention of a user```''')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def remove_potion(self, ctx, user: discord.Member, *, potion):
        userid = user.id
        guildid = ctx.guild.id
        ment = user.mention

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (guildid, userid, potion)
        cursor.execute(
            f'SELECT potion_name FROM player_potion WHERE guild_id = ? AND user_id = ? AND potion_name = ?', vals)
        armors = cursor.fetchone()

        if armors is not None:
            sql = ('DELETE FROM player_potion WHERE guild_id = ? AND user_id = ? AND potion_name = ?')
            val = (guildid, userid, potion)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

            await ctx.send(f'{ment} had armor {potion} removed.')
        else:
            await ctx.send(f'{ment} does not have {potion}.')

    @remove_potion.error
    async def remove_potion_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('''You are missing an argument!
            ```remove_potion [user] [potion]
            where user is the user you want to remove from
            where potion is the potion to remove```''')

    ####################################################################################################################
    #   Weapons                                                                                                        #
    ####################################################################################################################
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def create_weapon_by_db(self, ctx, name, type, cost, add_to_attack, *, desc):
        weap_guild = ctx.guild.id
        weap_name = ''
        weap_type = ''
        weap_cost = ''
        weap_add_to_attack = ''
        weap_desc = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, name)
        cursor.execute(f'SELECT weapon_name FROM weapons WHERE guild_id = ? AND weapon_name = ?', vals)
        res = cursor.fetchone()

        if res is not None:
            await ctx.send('The weapon_already exists! Please choose another name!')
            return
        else:
            weap_name = name

        if type != 'MELEE' or type != 'RANGE':
            await ctx.send('The value of type is not MELEE and RANGE! Please change this value!')
            return
        else:
            weap_type = type

        if not can_be_int(cost):
            await ctx.send('The weapon cost needs to be an integer! Please change this value!')
            return
        else:
            if int(cost) <= 0:
                await ctx.send('The cost value is not positive! Please change this value!')
                return
            else:
                weap_cost = cost

        if not can_be_int(add_to_attack):
            await ctx.send('The weapon value added to attack needs to be an integer! Please change this value!')
            return
        else:
            if int(add_to_attack) <= 0:
                await ctx.send('The attack value is not positive or zero! Please change this value!')
                return
            else:
                weap_add_to_attack = add_to_attack

        sql = ('INSERT INTO weapons(guild_id, weapon_name, weapon_type, weapon_cost, weapon_add_attack, weapon_desc) VALUES(?,?,?,?,?,?)')
        val = (weap_guild, weap_name, weap_type, weap_cost, weap_add_to_attack, weap_desc)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @create_weapon_by_db.error
    async def create_weapon_by_db_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''You are missing argument(s)!
            ```create_weapon_by_db [name] [type] [cost] [add_to_attack] [desc]
            where name is the name of the weapon
            where type is if the weapon is MELEE or RANGE
            where cost is an integer cost
            where add_to_attack is the integer value to add to an attack
            where desc is the weapon description
            
            If any of these values excluding the description has a space, please surround the value with double quotes ("")!''')
        else:
            await ctx.send('An error has occurred!')

    @commands.command()
    async def show_weapon_info(self, ctx, *, weapon):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, weapon)
        cursor.execute(f'SELECT weapon_name, weapon_type, weapon_cost, weapon_add_attack, weapon_desc FROM weapons WHERE guild_id = ? AND weapon_name = ?', vals)
        result = cursor.fetchone()

        gold_name = get_val_from_json(ctx, 'goldname.json')

        if result is not None:
            await ctx.send(f'''{result[0]} | {result[1]} weapon
            ```Costs: {result[2]} {gold_name}
        
            Adds {result[3]} to all attacks.
            Description:\n{result[4]}''')
        else:
            await ctx.send('This weapon does not exist.')

    @show_weapon_info.error
    async def show_weapon_info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''You are missing an argument!
            ```show_weapon_info [weapon]
            where weapon is a weapon from the weapon list```''')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def update_weapon(self, ctx, weapon, info, *, value):
        acceptable_strings = ['name', 'type', 'cost', 'add_to_attack', 'desc']
        insert_col = ''
        insert_val = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, weapon)
        cursor.execute(f'SELECT weapon_name FROM weapons WHERE guild_id = ? AND weapon_name = ?', vals)
        res = cursor.fetchone()

        if res is not None:
            if info in acceptable_strings:
                if info == acceptable_strings[0]:
                    vals = (ctx.guild.id, value)
                    cursor.execute(
                        f'SELECT weapon_name FROM weapons WHERE guild_id = ? AND weapon_name = ?', vals)
                    quest = cursor.fetchone()

                    if quest is not None:
                        await ctx.send(f'{value} already exits! Please select another name!')
                        return
                    else:
                        insert_col = 'weapon_name'
                        insert_val = value
                        await ctx.send(f'Setting the weapon name as {value}.')
                elif info == acceptable_strings[1]:
                    if value == 'MELEE' or value == 'RANGE':
                        insert_col = 'weapon_type'
                        insert_val = value
                        await ctx.send(f'Setting the weapon type to {value}.')
                    else:
                        await ctx.send(f'{value} is not MELEE or RANGE! Please change it to one of those two values!')
                        return
                elif info == acceptable_strings[2]:
                    if can_be_int(value):
                        if int(value) >= 0:
                            insert_col = 'weapon_cost'
                            insert_val = value
                            await ctx.send(f'Setting the weapon cost to {value}.')
                        else:
                            await ctx.send(f'{value} is a negative number! Please set it to a positive value!')
                            return
                    else:
                        await ctx.send(f'{value} is not an integer! Please try again!')
                        return
                elif info == acceptable_strings[3]:
                    if can_be_int(value):
                        if int(value) > 0:
                            insert_col = 'weapon_add_attack'
                            insert_val = value
                            await ctx.send(f'Setting the weapon add to attack value to {value}.')
                        else:
                            await ctx.send(f'{value} is not a positive value! Please change this value!')
                            return
                    else:
                        await ctx.send(f'{value} is not an integer! Please change this value!')
                        return
                elif info == acceptable_strings[4]:
                    insert_col = 'weapon_desc'
                    insert_val = value
                    await ctx.send(f'Setting description to {value}.')
                else:
                    await ctx.send(f'''The info string inputted does not fit the acceptable strings!
                    ```update_weapon [weapon] [info] [value]
                    where weapon is the name of the weapon list
                    where info is the information to be changed
                        The acceptable strings are
                            name which changes the name of the weapon
                            type which changes whether the weapon is MELEE or RANGE
                            cost which changes the cost of the weapon (This is an integer greater than or equal to zero)
                            add_to_attack which changes the value added to each classes attack (This is an integer greater than zero)
                            desc which changes the description of the weapon
                    where value is the value to change it to
                    
                    If the weapon contains a space, please surround it with double quotes ("")!''')
                    return
            else:
                await ctx.send(f'''The info string inputted does not fit the acceptable strings!
                ```update_weapon [weapon] [info] [value]
                where weapon is the name of the weapon list
                where info is the information to be changed
                    The acceptable strings are
                        name which changes the name of the weapon
                        type which changes whether the weapon is MELEE or RANGE
                        cost which changes the cost of the weapon (This is an integer greater than or equal to zero)
                        add_to_attack which changes the value added to each classes attack (This is an integer greater than zero)
                        desc which changes the description of the weapon
                    where value is the value to change it to
                    
                    If the weapon contains a space, please surround it with double quotes ("")!''')
                return
        else:
            await ctx.send(f'{weapon} does not exist')
            return

        sql = (f'UPDATE weapons SET {insert_col} = ? WHERE guild_id = ? AND weapon_name = ?')
        val = (insert_val, ctx.guild.id, weapon)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @update_weapon.error
    async def update_weapon_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''The value is missing argument(s)!
            ```update_weapon [weapon] [info] [value]
            where weapon is the name of the weapon list
            where info is the information to be changed
                The acceptable strings are
                    name which changes the name of the weapon
                    type which changes whether the weapon is MELEE or RANGE
                    cost which changes the cost of the weapon (This is an integer greater than or equal to zero)
                    add_to_attack which changes the value added to each classes attack (This is an integer greater than zero)
                    desc which changes the description of the weapon
                where value is the value to change it to
                    
                If the weapon contains a space, please surround it with double quotes ("")!''')
        else:
            await ctx.send('''An error has occurred!''')


    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def delete_weapon(self, ctx, *, weapon):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, weapon)
        cursor.execute(f'SELECT weapon_name FROM weapons WHERE guild_id = ? AND weapon_name = ?', vals)
        res = cursor.fetchone()

        if res is not None:
            sql = ('DELETE FROM weapons WHERE guild_id = ? AND weapon_name = ?')
            val = (ctx.guild.id, weapon)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send(f'''{weapon} does not exist!
            ```delete_weapon [weapon]
            where weapon is the weapon to remove```''')

    @delete_weapon.error
    async def delete_weapon_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('''You are missing the required argument!
            ```delete_weapon [weapon]
            where weapon is the weapon to remove```''')
        else:
            await ctx.send('''An error has occurred!''')

    ####################################################################################################################
    #   Armor                                                                                                          #
    ####################################################################################################################
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def create_armor_by_db(self, ctx, name, type, plus_ac_roll, cost, *, desc):
        armor_guild = ctx.guild.id
        armor_name = ''
        armor_type = ''
        armor_plus_ac_roll = ''
        armor_cost = ''
        armor_desc = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, name)
        cursor.execute(
            f'SELECT armor_name FROM armors WHERE guild_id = ? AND armor_name = ?', vals)
        res = cursor.fetchone()

        if res is not None:
            await ctx.send(f'The armor {name} already exist! Please pick a name that does not exist!')
            return
        else:
            armor_name = name

        if type != 'LIGHT' or type != 'MEDIUM' or type != 'HEAVY':
            await ctx.send('The type is incorrect! Please try again!')
            return
        else:
            armor_type = type

        if not can_be_int(plus_ac_roll):
            await ctx.send('The value of the ac or roll addition value is not an integer! Please try again!')
            return
        elif can_be_int(plus_ac_roll):
            if int(plus_ac_roll) <= 0:
                await ctx.send('The value must be a positive! Please try again!')
                return
            else:
                armor_plus_ac_roll = plus_ac_roll
        else:
            await ctx.send('An error has occurred! Please try again!')
            return

        if not can_be_int(cost):
            await ctx.send('The value of the cost is not an integer! Please try again!')
            return
        elif can_be_int(cost):
            if int(cost) < 0:
                await ctx.send('The value must be a positive! Please try again!')
                return
            else:
                armor_cost = cost

        armor_desc = desc

        sql = (
            'INSERT INTO armors(guild_id, armor_name, armor_type, armor_plus_ac_roll, armor_cost, armor_desc) VALUES(?,?,?,?,?,?)')
        val = (armor_guild, armor_name, armor_type, armor_plus_ac_roll, armor_cost, armor_desc)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()


    @create_armor_by_db.error
    async def create_armor_by_db_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('''An error has occurred! Please try again!
            ```create_armor_by_db [name] [type] [plus_ac_roll] [cost] [desc]
            where name is the name of the armor
            where type is the type of the armor (This can be LIGHT, MEDIUM, or HEAVY)
            where plus_ac_roll is what value is to be added to either the player ac or dodge roll depending on rule (This must be a positive integer)
            where cost is the cost of the item (This must be a positive integer)
            where desc is the description of the armor

            If any information besides the description contains a space, please surround it in double quotes ("")!```''')
        else:
            await ctx.send('An error has occurred!')


    @commands.command()
    async def show_armor_info(self, ctx, *, armor):
        ac_comp_rule = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id)
        cursor.execute(f'SELECT ac_comp_roll FROM rules WHERE guild_id = ?', vals)
        rule = cursor.fetchone()

        gold_name = get_val_from_json(ctx, 'goldname.json')

        if rule is not None:
            if rule[0] == 'AC':
                ac_comp_rule = rule[0]
            elif rule[0] == 'COMPROLL':
                ac_comp_rule = rule[0]
            else:
                await ctx.send('The rules are not set up correctly!')
                return
        else:
            await ctx.send('The rules are not set up correctly!')
            return

        vals = (ctx.guild.id, armor)
        cursor.execute(f'SELECT armor_name, armor_type, armor_plus_ac_roll, armor_cost, armor_desc FROM armors WHERE guild_id = ? AND armor_name = ?', vals)
        result = cursor.fetchone()

        if result is not None:
            await ctx.send(f'''{result[0]} | {result[1]}
            Cost: {result[3]} {gold_name}
            Adds {result[2]} to {ac_comp_rule}
            
            Description:\n{result[4]}''')
        else:
            await ctx.send(f'''The armor does not exist!
            ```show_armor_info [armor]
            where armor is armor to look up from the armor list```''')


    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def update_armor(self, ctx, armor, info, *, value):
        acceptable_strings = ['name', 'type', 'ac_plus_roll', 'cost', 'desc']
        insert_col = ''
        insert_val = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, armor)
        cursor.execute(
            f'SELECT armor_name FROM armors WHERE guild_id = ? AND armor_name = ?', vals)
        res = cursor.fetchone()

        if res is None:
            await ctx.send(f'{armor} does not exist!')
            return

        if info in acceptable_strings:
            if info == acceptable_strings[0]:

                vals = (ctx.guild.id, value)
                cursor.execute(
                    f'SELECT armor_name FROM armors WHERE guild_id = ? AND armor_name = ?', vals)
                quest = cursor.fetchone()

                if quest is not None:
                    await ctx.send(f'{value} already exists! Please select another name!')
                    return
                else:
                    insert_col = 'armor_name'
                    insert_val = value
                    await ctx.send(f'Setting name to {value}.')
            elif info == acceptable_strings[1]:
                if value == 'LIGHT' or value == 'MEDIUM' or value == 'HEAVY':
                    insert_col = 'armor_type'
                    insert_val = value
                    await ctx.send(f'Setting armor type to {value}.')
                else:
                    await ctx.send(f'{value} does not fit the current list! Please try again!')
                    return
            elif info == acceptable_strings[2]:
                if can_be_int(value):
                    if int(value) > 0:
                        insert_col = 'armor_plus_ac_roll'
                        insert_val = value
                        await ctx.send(f'Setting value added to ac or dodge roll to {value}.')
                    else:
                        await ctx.send(f'The value {value} must be positive! Please try again!')
                        return
                else:
                    await ctx.send(f'The value {value} must be an integer! Please try again!')
                    return
            elif info == acceptable_strings[3]:
                if can_be_int(value):
                    if int(value) >= 0:
                        insert_col = 'armor_cost'
                        insert_val = value
                        await ctx.send(f'Setting the cost to {value}.')
                    else:
                        await ctx.send(f'The value {value} must be positive! Please try again!')
                        return
                else:
                    await ctx.send(f'The value {value} must be an integer! Please try again!')
                    return
            elif info == acceptable_strings[4]:
                insert_col = 'armor_desc'
                insert_val = value
                await ctx.send(f'Setting description to {value}.')
            else:
                await ctx.send(f'''The info value does not fit the accepted strings!
                ```update_armor [armor] [info] [value]
                where armor is an armor from the armor list
                where info this the information to update
                    The accepted strings are
                        name which changes the name of the armor
                        type which changes if the armor is LIGHT armor, MEDIUM armor, or HEAVY armor (The acceptable values are LIGHT, MEDIUM, or HEAVY)
                        ac_plus_roll changes the value added to the ac or dodge roll (This value must be a positive integer)
                        cost which changes the cost of the armor (This value must be a positive integer)
                        desc which changes the description of the armor
                where value is the value to change the information to
                
                If anything excluding value contain spaces, please surround the value with double quotes ("")!```''')
                return
        else:
            await ctx.send(f'''The info value does not fit the accepted strings!
            ```update_armor [armor] [info] [value]
            where armor is an armor from the armor list
            where info this the information to update
                The accepted strings are
                    name which changes the name of the armor
                    type which changes if the armor is LIGHT armor, MEDIUM armor, or HEAVY armor (The acceptable values are LIGHT, MEDIUM, or HEAVY)
                    ac_plus_roll changes the value added to the ac or dodge roll (This value must be a positive integer)
                    cost which changes the cost of the armor (This value must be a positive integer)
                    desc which changes the description of the armor
                where value is the value to change the information to
                
                If anything excluding value contain spaces, please surround the value with double quotes ("")!```''')
            return

        sql = (f'UPDATE armors SET {insert_col} = ? WHERE guild_id = ? AND armor_name = ?')
        val = (insert_val, ctx.guild.id, armor)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @update_armor.error
    async def update_armor_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''You are missing arguments!
            ```update_armor [armor] [info] [value]
            where armor is an armor from the armor list
            where info this the information to update
                The accepted strings are
                    name which changes the name of the armor
                    type which changes if the armor is LIGHT armor, MEDIUM armor, or HEAVY armor (The acceptable values are LIGHT, MEDIUM, or HEAVY)
                    ac_plus_roll changes the value added to the ac or dodge roll (This value must be a positive integer)
                    cost which changes the cost of the armor (This value must be a positive integer)
                    desc which changes the description of the armor
                where value is the value to change the information to
                
                If anything excluding value contain spaces, please surround the value with double quotes ("")!```''')
        else:
            await ctx.send('An error has occurred!')


    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def delete_armor(self, ctx, armor):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, armor)
        cursor.execute(
            f'SELECT armor_name FROM armors WHERE guild_id = ? AND armor_name = ?', vals)
        armor = cursor.fetchone()

        if armor is not None:
            sql = ('DELETE FROM armors WHERE guild_id = ? AND armor_name = ?')
            val = (ctx.guild.id, armor)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send(f'''{armor} does not exist!
            ```delete_armor [armor]
            where weapon is the weapon to remove```''')

    @delete_armor.error
    async def delete_armor_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''An argument is missing!
            ```delete_armor [armor]
            where armor is the armor to remove```''')
        else:
            await ctx.send('An error has occurred!')

    ####################################################################################################################
    #   Potions                                                                                                        #
    ####################################################################################################################
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def create_potion_by_db(self, ctx, name, cond, cost, *, desc):
        potion_guild = ctx.guild.id
        potion_name = ''
        potion_cond = ''
        potion_cost = ''
        potion_desc = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, name)
        cursor.execute(
            f'SELECT potion_name FROM potions WHERE guild_id = ? AND potion_name = ?', vals)
        res = cursor.fetchone()

        if res is not None:
            await ctx.send(f'{name} already exists. Please try again!')
            return
        else:
            potion_name = name

        vals = (ctx.guild.id, cond)
        cursor.execute(
            f'SELECT condition_name FROM effectcond WHERE guild_id = ? AND condition_name = ?', vals)
        res1 = cursor.fetchone()

        if res1 is not None:
            potion_cond = cond
        else:
            await ctx.send(f'{cond} does not exist. Please try again!')
            return

        if not can_be_int(cost):
            await ctx.send('The value of the cost is not an integer! Please try again!')
            return
        elif can_be_int(cost):
            if int(cost) < 0:
                await ctx.send('The value must be a positive! Please try again!')
                return
            else:
                potion_cost = cost

        potion_desc = desc

        sql = (
            'INSERT INTO armors(guild_id, potion_name, potion_condition, potion_cost, potion_desc) VALUES(?,?,?,?,?)')
        val = (potion_guild, potion_name, potion_cond, potion_cost, potion_desc)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @create_potion_by_db.error
    async def create_potion_by_db_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''An argumment(s) is missing!
            ```create_potion_by_db [name] [cond] [cost] [desc]
            where name is the name of the potion
            where cond is the condition associated with the potion (the condition must be a pre-existing condition)
            where cost is the cost of the potion (this value must be a positive integer)
            where desc is the description of the potion
            
            If any values not including description contains spaces, please surround the value with double quotes ("")!''')


    @commands.command()
    async def show_potion_info(self, ctx, potion):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, potion)
        cursor.execute(
            f'SELECT potion_name, potion_condition, potion_cost, potion_desc FROM potions WHERE guild_id = ? AND potion_name = ?', vals)
        pot = cursor.fetchone()

        gold_name = get_val_from_json(ctx, 'goldname.json')

        if pot is None:
            await ctx.send(f'''Potion {potion} does not exist.''')
            return
        else:
            await ctx.send(f'''{pot[0]}
            Cost: {pot[1]} {gold_name}
            Condition given: {pot[2]}
            
            Description\n{pot[3]}''')

    @show_potion_info.error
    async def show_potion_info_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''This command is missing an argument!
            ```show_potion_info [potion]
            where potion is the potion to view```''')
        else:
            await ctx.send('An error has occurred!')


    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def update_potion(self, ctx, potion, info, *, value):
        accepted_strings = ['name', 'cond', 'cost', 'desc']
        insert_col = ''
        insert_val = ''

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, potion)
        cursor.execute(
            f'SELECT potion_name FROM potions WHERE guild_id = ? AND potion_name = ?', vals)
        res = cursor.fetchone()

        if res is None:
            await ctx.send('The potion does not exist! Please try again!')
            return

        if info in accepted_strings:
            if info == accepted_strings[0]:
                vals = (ctx.guild.id, value)
                cursor.execute(
                    f'SELECT potion_name FROM potions WHERE guild_id = ? AND potion_name = ?', vals)
                question = cursor.fetchone()

                if question is not None:
                    await ctx.send(f'{value} already exits! Please select another name!')
                    return
                else:
                    insert_col = 'potion_name'
                    insert_val = value
                    await ctx.send(f'Setting the name to {value}.')
            elif info == accepted_strings[1]:
                vals = (ctx.guild.id, value)
                cursor.execute(
                    f'SELECT condition_name FROM effectcond WHERE guild_id = ? AND condition_name = ?', vals)
                res1 = cursor.fetchone()

                if res1 is None:
                    await ctx.send(f'{value} is not a condition! Please try again!')
                    return
                else:
                    insert_col = 'potion_condition'
                    insert_val = value
                    await ctx.send(f'Setting condition to {value}.')
            elif info == accepted_strings[2]:
                if can_be_int(value):
                    if int(value) >= 0:
                        insert_col = 'potion_cost'
                        insert_val = value
                        await ctx.send(f'Setting cost value to {value}.')
                    else:
                        await ctx.send(f'The value {value} must be positive! Please try again!')
                        return
                else:
                    await ctx.send(f'The value {value} must be an integer! Please try again!')
                    return
            elif info == accepted_strings[3]:
                insert_col = 'potion_desc'
                insert_val = value
                await ctx.send(f'Setting description to {value}.')
            else:
                await ctx.send(f'''The info value is not acceptable!
                ```update_potion [potion] [info] [value]
                where potion is potion you are trying to change
                where info is the information you are trying to change
                    The acceptable values are
                        name which changes the name of the potion
                        cond which changes the condition associated with the spell (This must be an already existing condition)
                        cost which changes the cost of the potion (This must be an integer greater than or equal to zero
                        desc which changes the description of the potion
                where value is the value to change the information to
                
                If anything excluding value contain spaces, please surround the value with double quotes ("")!```''')
                return
        else:
            await ctx.send(f'''The info value is not acceptable!
            ```update_potion [potion] [info] [value]
            where potion is potion you are trying to change
            where info is the information you are trying to change
                The acceptable values are
                    name which changes the name of the potion
                    cond which changes the condition associated with the spell (This must be an already existing condition)
                    cost which changes the cost of the potion (This must be an integer greater than or equal to zero
                    desc which changes the description of the potion
            where value is the value to change the information to
                
            If anything excluding value contain spaces, please surround the value with double quotes ("")!```''')
            return

        sql = (f'UPDATE potions SET {insert_col} = ? WHERE guild_id = ? AND potion_name = ?')
        val = (insert_val, ctx.guild.id, potion)

        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @update_potion.error
    async def update_potion_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'''There was an argument(s) missing!
            ```update_potion [potion] [info] [value]
            where potion is potion you are trying to change
            where info is the information you are trying to change
                The acceptable values are
                    name which changes the name of the potion
                    cond which changes the condition associated with the spell (This must be an already existing condition)
                    cost which changes the cost of the potion (This must be an integer greater than or equal to zero
                    desc which changes the description of the potion
            where value is the value to change the information to
                
            If anything excluding value contain spaces, please surround the value with double quotes ("")!```''')

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    async def delete_potion(self, ctx, potion):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        vals = (ctx.guild.id, potion)
        cursor.execute(
            f'SELECT potion_name FROM potions WHERE guild_id = ? AND potion_name = ?')
        pot = cursor.fetchone()

        if pot is not None:
            sql = ('DELETE FROM potions WHERE guild_id = ? AND potion_name = ?')
            val = (ctx.guild.id, potion)

            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.send(f'''{potion} does not exist!
            ```delete_potion [potion]
            where potion is the potion to remove```''')

    @delete_potion.error
    async def delete_potion_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('''The command is missing argument(s)!
            ```delete_potion [potion]
            where potion is the potion to remove```''')


    ####################################################################################################################
    #   Other Methods                                                                                                  #
    ####################################################################################################################
    @commands.command()
    async def purchase(self, ctx, item_type, item_name):
        userid = ctx.author.id
        guildid = ctx.guild.id

        async def buy(user_gold, item_cost):
            if int(user_gold) < int(item_cost):
                await ctx.send('You cannot afford this item!')
                return 'failure'
            else:
                new_user_gold = int(user_gold) - int(item_cost)
                return str(new_user_gold)




        if item_type == 'weapon':
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            vals = (guildid, item_name)
            cursor.execute(
                f'SELECT weapon_name, weapon_cost FROM weapons WHERE guild_id =  AND weapon_name = ?', vals)
            item = cursor.fetchone()

            vals2 = (guildid, userid)
            cursor.execute(f'SELECT gold FROM player_gold WHERE guild_id = ? AND user_id = ?', vals2)
            gold = cursor.fetchone()

            if item is None:
                await ctx.send(f'{item_name} does not exist!')
                return
            else:
                vals = (guildid, userid, item_name)
                cursor.execute(
                    f'SELECT weapon_name FROM player_weapon WHERE guild_id = ? AND user_id = ? AND weapon_name = ?', vals)
                weapon = cursor.fetchone()

                if weapon is not None:
                    await ctx.send(f'{item_name} is already in your inventory!')
                    return
                else:
                    worked = buy(gold[0], item[1])

                    if worked == 'failure':
                        return
                    else:
                        sql = ('UPDATE player_gold SET gold = ? WHERE guild_id = ? AND user_id = ?')
                        val = (worked, guildid, userid)

                        cursor.execute(sql, val)

                        sql = ('INSERT INTO player_weapon(guild_id, user_id, weapon_name) VALUES(?,?,?)')
                        val = (guildid, userid, item_name)

                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()
        elif item_type == 'armor':
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            vals = (guildid, item_name)
            cursor.execute(
                f'SELECT armor_name, armor_cost FROM armors WHERE guild_id = ? AND armor_name = ?', vals)
            item = cursor.fetchone()

            vals2 = (guildid, userid)
            cursor.execute(f'SELECT gold FROM player_gold WHERE guild_id = ? AND user_id = ?', vals)
            gold = cursor.fetchone()

            if item is None:
                await ctx.send(f'{item_name} does not exist!')
                return
            else:
                vals = (guildid, userid, item_name)
                cursor.execute(
                    f'SELECT armor_name FROM player_armor WHERE guild_id = ? AND user_id = ? AND armor_name = ?', vals)
                weapon = cursor.fetchone()

                if weapon is not None:
                    await ctx.send(f'{item_name} is already in your inventory!')
                    return
                else:
                    worked = buy(gold[0], item[1])

                    if worked == 'failure':
                        return
                    else:
                        sql = ('UPDATE player_gold SET gold = ? WHERE guild_id = ? AND user_id = ?')
                        val = (worked, guildid, userid)

                        cursor.execute(sql, val)

                        sql = ('INSERT INTO player_armor(guild_id, user_id, armor_name) VALUES(?,?,?)')
                        val = (guildid, userid, item_name)

                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()
        elif item_type == 'potion':
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()

            vals = (guildid, item_name)
            cursor.execute(
                f'SELECT potion_name, potion_cost FROM potions WHERE guild_id = ? AND potion_name = ?', vals)
            item = cursor.fetchone()

            vals = (guildid, userid)
            cursor.execute(f'SELECT gold FROM player_gold WHERE guild_id = ? AND user_id = ?', vals)
            gold = cursor.fetchone()

            if item is None:
                await ctx.send(f'{item_name} does not exist!')
                return
            else:
                vals = (guildid, userid, item_name)
                cursor.execute(
                    f'SELECT potion_name FROM player_potion WHERE guild_id = ? AND user_id = ? AND potion_name = ?', vals)
                weapon = cursor.fetchone()

                if weapon is not None:
                    await ctx.send(f'{item_name} is already in your inventory!')
                    return
                else:
                    worked = buy(gold[0], item[1])

                    if worked == 'failure':
                        return
                    else:
                        sql = ('UPDATE player_gold SET gold = ? WHERE guild_id = ? AND user_id = ?')
                        val = (worked, guildid, userid)

                        cursor.execute(sql, val)

                        sql = ('INSERT INTO player_potion(guild_id, user_id, potion_name) VALUES(?,?,?)')
                        val = (guildid, userid, item_name)

                        cursor.execute(sql, val)
                        db.commit()
                        cursor.close()
                        db.close()
        else:
            await ctx.send('''This is not a valid item type
            ```purchase [item_type] [item_name]
            where item_type defines if the item is a weapon, armor, or potion (The acceptable values are weapon, armor, or potion)
            where item_name is the item to purchase```''')

    @purchase.error
    async def purchase_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('''This is not a valid item type
            ```purchase [item_type] [item_name]
            where item_type defines if the item is a weapon, armor, or potion (The acceptable values are weapon, armor, or potion)
            where item_name is the item to purchase```''')
        else:
            await ctx.send('An error has occurred!')

    @commands.command()
    async def view_shop_items(self, ctx):
        str = 'WEAPONS:\n'
        gold_name = get_val_from_json(ctx, 'goldname.json')

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        for row in cursor.execute(f'SELECT weapon_name, weapon_cost FROM weapons WHERE guild_id = {ctx.guild.id}'):
            str += f'{row[0]} | {row[1]} {gold_name}\n'

        str += '\nARMORS:\n'

        for row in cursor.execute(f'SELECT armor_name, armor_cost FROM armors WHERE guild_id = {ctx.guild.id}'):
            str += f'{row[0]} | {row[1]} {gold_name}\n'

        str += '\nPOTIONS:\n'

        for row in cursor.execute(f'SELECT potion_name, potion_cost FROM potions WHERE guild_id = {ctx.guild.id}'):
            str += f'{row[0]} | {row[1]} {gold_name}\n'

        await ctx.send(str)

    @commands.command()
    async def view_shop_weapons(self, ctx):
        str = 'WEAPONS:\n'
        gold_name = get_val_from_json(ctx, 'goldname.json')

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        for row in cursor.execute(f'SELECT weapon_name, weapon_cost FROM weapons WHERE guild_id = {ctx.guild.id}'):
            str += f'{row[0]} | {row[1]} {gold_name}\n'

        await ctx.send(str)

    @commands.command()
    async def view_shop_armors(self, ctx):
        gold_name = get_val_from_json(ctx, 'goldname.json')

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        str = 'ARMORS:\n'

        for row in cursor.execute(f'SELECT armor_name, armor_cost FROM armors WHERE guild_id = {ctx.guild.id}'):
            str += f'{row[0]} | {row[1]} {gold_name}\n'

        await ctx.send(str)

    @commands.command()
    async def view_shop_potions(self, ctx):
        gold_name = get_val_from_json(ctx, 'goldname.json')

        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()

        str = 'POTIONS:\n'

        for row in cursor.execute(f'SELECT potion_name, potion_cost FROM potions WHERE guild_id = {ctx.guild.id}'):
            str += f'{row[0]} | {row[1]} {gold_name}\n'

        await ctx.send(str)


def setup(client):
    client.add_cog(Shop(client))