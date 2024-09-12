from .bot import Bot
from .database import DataBase
from .constants import *
from .errors import *
from .models import Participante, Corrida
from discord.ext import commands
import discord


Context = commands.Context[Bot]
Interaction = discord.Interaction[Bot]