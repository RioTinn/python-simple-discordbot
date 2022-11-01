import nextcord
from nextcord import File, ButtonStyle
from nextcord.ext import commands
from nextcord.ui import Button, View

import dotenv
import aiosqlite
import datetime
from os import environ as env
import random

dotenv.load_dotenv()


def get_time():
	return datetime.datetime.now().strftime("%H:%M:%S")




intents=nextcord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents,help_command=None)

@bot.event
async def on_ready():
	 print(f"whazdup")
	 db = await aiosqlite.connect("database.db")

@bot.event
async def on_member_join(member):
	await bot.get_channel(1033304545939443807).send(f"{member.mention} присоединился к серверу, тем самым, составил нам компанию! 👋")



@bot.command(aliases=['тест'])
async def test(ctx):
	responses = ["Я функционирую!",'Перспективы у Вас хорошие.','Да!','Да-да?','У всех разумных существ есть право быть свободными.','Всего надо добиваться постепенно.','Что тебе нужно, человек?','👋', 'Привет!', 'Я здесь!']
	await ctx.send(random.choice(responses))

@bot.command(aliases=['скажи'])
async def say(ctx, *, saymsg=None):
	if saymsg != None:
		await ctx.send(saymsg)
		
	else:
		await ctx.send("Ты должен мне написать, чтобы я сказал.")


@bot.command(aliases=['серверинфо'])
async def serverinfo(ctx):
	#role_count = len(ctx.guild.roles)
	statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
	len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
	list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
	server_info_embed = nextcord.Embed(timestamp=ctx.message.created_at, color=ctx.author.color)
	server_info_embed.add_field(name="Название сервера", value=f"{ctx.guild.name}", inline=False)
	server_info_embed.add_field(name="Количество участников", value=f"{ctx.guild.member_count}", inline=False)
	#server_info_embed.add_field(name="Высшая роль", value={ctx.guild.roles}[-2], inline=False)
	server_info_embed.add_field(name="Количество ботов", value=len(list_of_bots), inline=False)   
	server_info_embed.add_field(name="Боты", value=", ".join(list_of_bots), inline=False)
	server_info_embed.add_field(name="Администратор", value=ctx.guild.owner.mention, inline=False)
	server_info_embed.add_field(name="Онлайн: ", value=f"{statuses[0]}") 
	server_info_embed.add_field(name="Оффлайн: ", value=f"{statuses[1]}")
	await ctx.send(embed=server_info_embed)

@bot.command(aliases=['хелп','помоги'])
async def help(ctx):
	
	
	help_embed = nextcord.Embed(color=ctx.author.color)
	help_embed.add_field(name="Команды:", value=f"!test [!тест] − проверяет работоспособность бота (выдаёт рандомные фразы) \n\n!say [!скажи] − возвращает ваш текст \n\n!serverinfo [!серверинфо] − информация о сервере \n\n!help [!хелп, !помоги] − все команды бота" , inline=False)
	help_embed.add_field(name="Слэш команды:", value=f"/ping − ответит вам \"Понг!\" \n\n/embed − эмбед-сообщение \n\n/key − создаёт кнопку", inline=False)

	await ctx.send(embed=help_embed)

@bot.slash_command(name="ping", description="Ответит вам \"Понг!\"")
async def ping(interaction: nextcord.Interaction):
	await interaction.response.send_message(f"Понг! \nВремя ожидания: `{round(bot.latency * 1000)} милисекунд`")

@bot.slash_command(name='key', description="Создаёт кнопку")
async def key(ctx):
	answ = Button(label="Нажми на меня!", style=ButtonStyle.green)
	
	async def answ_callback(interaction):
		await interaction.response.send_message("Поздравляю, ты нажал на меня!")

	answ.callback = answ_callback

	myview = View()
	myview.add_item(answ)
	
	
	await ctx.send(view=myview)

@bot.slash_command(name="embed", description="Возвращает эмбед-сообщение")
async def embed(
		interaction: nextcord.Interaction, description: str = nextcord.SlashOption(description="Описание", required=True), 
		title: str = nextcord.SlashOption(description="Название", required=False)
	):
	embed = nextcord.Embed(description=description)
	if title:
		embed.title = title

	await interaction.response.send_message(embed=embed)

bot.run(env['TOKEN'])