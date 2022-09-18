import datetime
import discord.colour
from DataBase.DB import DB
from loguru import logger

OwnerID = 329653972728020994
DataBaseClass: DB = None
UserColor = discord.colour.Colour.blue()
AdminColor = discord.colour.Colour.red()
OwnerColor = discord.colour.Colour.green()
TestBot: bool = False
ISDebug = False
ISPostNasaNews = False
FormatLog = '[{time:YY.M.D HH:mm:ss}] | {level}\t| {name}:{function}:{line} - {message}'

class EnergyVariables:
    def __init__(self, file_name):
        self.file_name = file_name
        self.variable = {}
        self._load_variables()

    @logger.catch()
    def _load_variables(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            for line in file:
                data = line.split(';')
                if len(data) != 3:
                    raise Exception('При парсинге файла с переменными возникла проблема парса')
                match data[0]:
                    case 'date':
                        data[2] = datetime.datetime.strptime(data[2][:-1], '%Y-%m-%d').date()
                    case 'int':
                        data[2] = int(data[2])
                    case 'bool':
                        data[2] = bool(data[2])

                self.variable[data[1]] = data[2]

    @logger.catch()
    def _write_variables(self):
        with open(self.file_name, 'w', encoding='utf-8') as file:
            for k, v in self.variable.items():
                match v:
                    case bool(v):
                        file.write(f'bool;{k};{v}\n')
                    case int(v):
                        file.write(f'int;{k};{v}\n')
                    case datetime.date():
                        file.write(f'date;{k};{v.strftime("%Y-%m-%d")}\n')

    def get(self, key, value=None):
        if key in self.variable:
            return self.variable[key]
        else:
            self.variable[key] = value
            self._write_variables()
            return value

    def set(self, key, value):
        self.variable[key] = value
        self._write_variables()


    @logger.catch()
    def __getitem__(self, item):
        if item not in self.variable:
            return None
        return self.variable[item]

    def __setitem__(self, key, value):
        self.variable[key] = value
        self._write_variables()


EnergyVariablesClass: EnergyVariables = None
