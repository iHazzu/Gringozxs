from .bot import Bot
from .pagination import Pagination
from .database import DataBase
from .constants import *
from .errors import *
from discord.ext import commands
import discord


Context = commands.Context[Bot]
Interaction = discord.Interaction[Bot]