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

class Shop(commands.Cog):

    pass


def setup(client):
    client.add_cog(Shop(client))