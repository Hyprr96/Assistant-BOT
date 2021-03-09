"""
Name: Pavishanan Surenthiran
Date: 2021-02-14
Description: Attempting to build my personal assistant bot
"""

# Imports
import time
import discord
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext import commands
from youtubesearchpython import VideosSearch
import os
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from passwordgenerator import pwgenerator
from saucenao_api import SauceNao
from saucenao_api.errors import UnknownClientError
from jikanpy import Jikan
import wolframalpha
import random

class AssistantClass():
    """Assistant bot class"""
    def __init__(self):
        """Initializing attributes"""
        # Tokens and Bot Prefix
        self.bot_client = discord.Client()
        self.bot_client = commands.Bot(command_prefix="!a ")
        self.bot_client.remove_command('help')
        self.token_code = "ODEwNTg0MzU2OTYyODI4MzE4.YClxgg.Qx-UflsNWG86H3i_IqfGXrEQmFg"
        self.weather_api = "http://api.openweathermap.org/data/2.5/weather?q=Toronto&units=metric&appid=f39749e137dc29218586e71c53ddbff5"

        # Help embed
        self.HelpEmbed()

        # Loading the commands
        self.BasicCommands()
        self.IntermediateCommands()

        # Starting the bot
        self.StartApp()

    def StartApp(self):
        """Starts the app"""
        # Starting the app
        @self.bot_client.event
        async def on_ready():
            await self.bot_client.change_presence(status = discord.Status.online, activity = discord.Game('prefix = !a | v2'))
            print('===============================')
            print('Assistant is now online')
            print('===============================')

        # Actually start the app
        self.bot_client.run(self.token_code)

    def HelpEmbed(self):
        """Shows the list of commands available for use"""
        @self.bot_client.command()
        async def help(ctx):
            help_embed = discord.Embed(
                timestamp = datetime.utcnow(),
                title = 'Listing all commands  |  Command prefix: !a'+'\n‎',
                colour = discord.Colour(0x8000ff)
                )

            help_embed.add_field(name = "BASIC COMMANDS", value = "------", inline=False)
            help_embed.add_field(name = "help", value = "Brings you here", inline=True)
            help_embed.add_field(name = "latency", value = "How long it takes for the bot to recieve the message", inline=True)
            help_embed.add_field(name = "clear", value = "Clears messages (default is 5)", inline=True)
            help_embed.add_field(name = "avatar", value = "Shows your avatar or whoever you mention", inline=True)
            help_embed.add_field(name = "stats", value = "Shows your 'stats' in the server", inline=True)
            help_embed.add_field(name = "hello", value = "Hello"+"\n‎", inline=True)
            help_embed.add_field(name = "timetable", value = "Shows the current Cedarbrae timetable for this week", inline=True)
            # Seperator
            help_embed.add_field(name = "‎", value = "‎", inline=False)
            help_embed.add_field(name = "INTERMEDIATE COMMANDS", value = "-----", inline=False)
            help_embed.add_field(name = "temp", value = "Shows the current temperature reading", inline=True)
            help_embed.add_field(name = "yt_search", value = "Shows the top 3 videos for whatever you searched", inline=True)
            help_embed.add_field(name = "rvrs_search", value = "Uses Google to reverse search an image link you input", inline=True)
            help_embed.add_field(name = "sauce", value = "Uses the 'SauceNao' search engine to return a possible anime sauce", inline=True)
            help_embed.add_field(name = "passgen", value = "generates a rememberable password for you", inline=True)
            help_embed.add_field(name = "find", value = "To find anime its, `find anime someanime`. To find manga, `find manga somemanga`.", inline=True)
            help_embed.add_field(name = "search", value = "Use this command if you want to find the answer to something. Its not google, it will only work for academic stuff.", inline=True)

            await ctx.send(embed = help_embed)

    def BasicCommands(self):
        """Basic Commands for Assistant"""
        # Basic Hello Command
        @self.bot_client.command()
        async def hello(ctx):
            await ctx.send("Hello ****"+str(ctx.author)[:-5]+"****!")

        # Shows the latency from you and the bot
        @self.bot_client.command()
        async def latency(ctx):
            await ctx.send("It took about ****"+str(round(self.bot_client.latency*1000))+"**** miliseconds for me to get your message!")

        # Clears specified amount of messages
        @self.bot_client.command()
        async def clear(ctx, clear_amount=5):
            if clear_amount==0:
                await ctx.send("Ok...")
            else:
                await ctx.send("Deleting ****"+str(clear_amount)+"**** messages | Requested by: "+str(ctx.author)+"!")
                time.sleep(1)
                await ctx.channel.purge(limit=clear_amount+2)
                time.sleep(1)
                await ctx.send("Deleted ****"+str(clear_amount)+"**** messages.")
                time.sleep(2)
                await ctx.channel.purge(limit=1)

        # Shows avatar pfp
        @self.bot_client.command()
        async def avatar(ctx, member:discord.Member="none"):
            if member=="none":
                member = str(ctx.author)
                ctx_avatar_embed = discord.Embed(
                    timestamp = datetime.utcnow(),
                    colour = discord.Colour(0x8000ff),
                    description = f"[Link to the avatar]({ctx.author.avatar_url})"
                )

                ctx_avatar_embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
                ctx_avatar_embed.set_author(name = member)
                ctx_avatar_embed.set_image(url = ctx.author.avatar_url)
                await ctx.send(embed = ctx_avatar_embed)
            else:
                member_avatar_embed = discord.Embed(
                    timestamp = datetime.utcnow(),
                    colour = discord.Colour(0x8000ff),
                    description = f"[Link to the avatar]({member.avatar_url})"
                )

                member_avatar_embed.set_footer(text = ctx.author, icon_url = ctx.author.avatar_url)
                member_avatar_embed.set_author(name = member)
                member_avatar_embed.set_image(url = member.avatar_url)
                await ctx.send(embed = member_avatar_embed)

        # Test command
        @self.bot_client.command()
        async def stats(ctx, member:discord.Member="none"):
            if (member=="none"):
                joined = ctx.author.joined_at
                nickname = str(ctx.author.nick)
                # None type if statement
                nitrosince = ctx.author.premium_since
                if nitrosince==None:
                    nitrosince = "None"
                else:
                    nitrosince = str(nitrosince.strftime('%m-%d-%Y'))
                status = str(ctx.author.status)
                is_mobile = str(ctx.author.is_on_mobile())
                gather_roles = ", ".join(str(r.name) for r in ctx.author.roles)
                s = gather_roles.split(',')
                await ctx.send("****"+str(ctx.author)+"****\n"
                                "---\n"
                                "Server joined date: ****"+str(joined.strftime('%m-%d-%Y')) + "****\n"
                                "Nickname: ****"+nickname+"****\n"
                                "Boosting since: ****"+nitrosince+"****\n"
                                "Status: ****"+status.upper()+"****\n"
                                "Is On Mobile?: ****"+is_mobile+"****\n"
                                "Roles: " + ", ".join(s[1:]) + "\n")
            else:
                joined = member.joined_at
                nickname = str(member.nick)
                # None type if statement
                nitrosince = member.premium_since
                if nitrosince==None:
                    nitrosince = "None"
                else:
                    nitrosince = str(nitrosince.strftime('%m-%d-%Y'))
                status = str(member.status)
                is_mobile = str(member.is_on_mobile())
                gather_roles = ", ".join(str(r.name) for r in member.roles)
                s = gather_roles.split(',')
                await ctx.send("****"+str(member)+"****\n"
                                "---\n"
                                "Server joined date: ****"+str(joined.strftime('%m-%d-%Y')) + "****\n"
                                "Nickname: ****"+nickname+"****\n"
                                "Boosting since: ****"+nitrosince+"****\n"
                                "Status: ****"+status.upper()+"****\n"
                                "Is On Mobile?: ****"+is_mobile+"****\n"
                                "Roles: " + ", ".join(s[1:]))

        @self.bot_client.command()
        async def timetable(ctx):
            cedarweek = "http://www.cedarbraeci.com/cedarweek.html"
            timetable_embed=discord.Embed(
                title="Cedarbrae timetable for this week",
                colour=0xffffff
            )
            school_pg = requests.get(cedarweek).content
            tree = BeautifulSoup(school_pg, 'html.parser')
            full_img = "http://www.cedarbraeci.com"
            imgs = []
            # Navigating tree
            for link in tree.find_all('img'):
                imgs.append(link.get('src'))
            full_img = full_img+imgs[0]

            # Setting image
            timetable_embed.set_image(url=full_img)
            await ctx.send(embed=timetable_embed)

    def IntermediateCommands(self):
        """More advanced commands"""
        # Youtube video search function
        @self.bot_client.command()
        async def yt_search(ctx, *title):
            # Start typing
            await ctx.trigger_typing()
            # Search for
            search_for = " ".join(title)
            empty_char = "‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎‎"

            # Searching the top three videos
            vs = VideosSearch(str(search_for), limit=3)
            vid = vs.result()

            if title:
                # Searching embed
                yt_embed_searching = discord.Embed(
                    title="Searching top three results: "+str(search_for[:25]+"..."),
                    colour=discord.Colour(0xff0000)
                )

                # First Section
                title_v1 = vid['result'][0]['title']
                creator_v1 = vid['result'][0]['channel']['name']
                views_v1 = vid['result'][0]['viewCount']['short']
                description_v1 = vid['result'][0]['descriptionSnippet'][0]['text']
                link_v1 = vid['result'][0]['link']
                published_v1 = vid['result'][0]['publishedTime']
                thumbnails_v1 = vid['result'][0]['thumbnails'][0]['url']

                # Embeds
                yt_embed_1 = discord.Embed(
                    colour=discord.Colour(0xff0000),
                )
                yt_embed_1.add_field(name="1. "+title_v1[:70]+"...", value="-----" +"\n"+
                                                                         description_v1+"\n"+
                                                                         "---"+"\n"+
                                                                         "Creator: ****"+creator_v1+"****\n"+
                                                                         "Views: ****"+views_v1+"****\n"+
                                                                         "Published: ****"+published_v1+"****\n"+
                                                                         "[Link to video...]("+link_v1+")"+
                                                                         "\n‎", inline=False)
                yt_embed_1.set_image(url=thumbnails_v1)

                # Second Section
                title_v2 = vid['result'][1]['title']
                creator_v2 = vid['result'][1]['channel']['name']
                views_v2 = vid['result'][1]['viewCount']['short']
                description_v2 = vid['result'][1]['descriptionSnippet'][0]['text']
                link_v2 = vid['result'][1]['link']
                published_v2 = vid['result'][1]['publishedTime']
                thumbnails_v2 = vid['result'][1]['thumbnails'][0]['url']

                # Second embed
                yt_embed_2 = discord.Embed(
                    colour=discord.Colour(0xff0000),
                )
                yt_embed_2.add_field(name="2. "+title_v2[:70]+"...", value="-----" +"\n"+
                                                                         description_v2+"\n"+
                                                                         "---"+"\n"+
                                                                         "Creator: ****"+creator_v2+"****\n"+
                                                                         "Views: ****"+views_v2+"****\n"+
                                                                         "Published: ****"+published_v2+"****\n"+
                                                                         "[Link to video...]("+link_v2+")"+
                                                                         "\n‎", inline=False)
                yt_embed_2.set_image(url=thumbnails_v2)

                # Third section
                title_v3 = vid['result'][2]['title']
                creator_v3 = vid['result'][2]['channel']['name']
                views_v3 = vid['result'][2]['viewCount']['short']
                description_v3 = vid['result'][2]['descriptionSnippet'][0]['text']
                link_v3 = vid['result'][2]['link']
                published_v3 = vid['result'][2]['publishedTime']
                thumbnails_v3 = vid['result'][2]['thumbnails'][0]['url']

                # Third Embed
                yt_embed_3 = discord.Embed(
                    colour=discord.Colour(0xff0000),
                )
                yt_embed_3.add_field(name="3. "+title_v3[:70]+"...", value="-----" +"\n"+
                                                                         description_v3+"\n"+
                                                                         "---"+"\n"+
                                                                         "Creator: ****"+creator_v3+"****\n"+
                                                                         "Views: ****"+views_v3+"****\n"+
                                                                         "Published: ****"+published_v3+"****\n"+
                                                                         "[Link to video...]("+link_v3+")"+
                                                                         "\n‎", inline=False)
                yt_embed_3.set_image(url=thumbnails_v3)

                # Sending the emebeds
                await ctx.send(embed=yt_embed_searching)
                time.sleep(1)
                await ctx.send(embed=yt_embed_1)
                await ctx.send(embed=yt_embed_2)
                await ctx.send(embed=yt_embed_3)
            else:
                # Searching embed
                yt_embed_searching = discord.Embed(
                    title="No Input Detected",
                    colour=discord.Colour(0xff0000)
                )
                await ctx.send(embed=yt_embed_searching)

        @self.bot_client.command()
        async def rvrs_search(ctx, *url):
            while True:
                # Trigger typing
                await ctx.trigger_typing()
                # Making the path to the webdriver
                chrome_options = webdriver.ChromeOptions()
                chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--no-sandbox")
                driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

                # Going to website and getting input
                driver.get("https://www.google.com/imghp?hl=en")

                # Actions
                if url:
                    searchimg_textfield = driver.find_element_by_css_selector("#sbtc > div > div.dRYYxd > div.LM8x9c > span").click() # clicking the button
                    input_url = driver.find_element_by_css_selector("#Ycyxxc").send_keys(url) # inputting the text
                    search_button = driver.find_element_by_css_selector("#RZJ9Ub").click() # clicking the search button
                else:
                    noinput_err = discord.Embed(
                        colour = discord.Colour(0xff0000),
                        title = "Error - No input",
                        description = "Put the link of the image after the command."
                        )
                    await ctx.send(embed=noinput_err)
                    break
                try:
                    # Try statement to see if there is a titlecard, if not use the possible search results
                    titlecard_info = driver.find_element_by_xpath('//*[@id="rhs"]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/h2/span').text
                    bottomtext_info = driver.find_element_by_xpath('//*[@id="rhs"]/div/div[1]/div[1]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[2]/div/span').text
                    #----
                    sauce = titlecard_info+" - "+bottomtext_info
                    sauce_embed = discord.Embed(
                        colour = discord.Colour(0xfffff),
                        title = sauce
                        )
                except selenium.common.exceptions.NoSuchElementException:
                    try:
                        possiblerelatedsearches_button = driver.find_element_by_xpath('//*[@id="topstuff"]/div/div[2]/a').text
                        # ----
                        sauce = possiblerelatedsearches_button
                        sauce_embed = discord.Embed(
                            colour = discord.Colour(0xfffff),
                            title = sauce
                            )
                    except selenium.common.exceptions.NoSuchElementException:
                        nosauce_err = discord.Embed(
                            colour = discord.Colour(0xff0000),
                            title = "Error - Couldn't find the sauce ;(",
                            description = "Double check the link and try again."
                            )
                        await ctx.send(embed=nosauce_err)
                        break
                # Sending
                await ctx.send(embed=sauce_embed)
                driver.quit()
                break

        @self.bot_client.command()
        async def passgen(ctx):
            # PIP DOWNLOAD THE PASSWORDGENERATOR PWGENERATOR
            # MODULE AND INLCUDE IT INTO THE REQUIREMENTS FILE
            await ctx.trigger_typing()
            password_gen = pwgenerator.generate()

            # Embed Pass
            embedpass = discord.Embed(
                title = "New Password Generated",
                description = "Pass: ****"+str(password_gen)+"****",
                colour = discord.Colour(0x8452fb)
                )

            # Sending it
            await ctx.send(embed=embedpass)

        @self.bot_client.command()
        async def temp(ctx):
            # Start typing
            await ctx.trigger_typing()
            # accessing json api
            json_access = requests.get(self.weather_api).json()
            # dynamic icon
            icon = json_access['weather'][0]['icon']
            icon_url = "http://openweathermap.org/img/wn/{}@2x.png"
            # json_access's
            weather = json_access['weather'][0]['main']
            temp = json_access['main']['temp']
            feels_like = json_access['main']['feels_like']
            highest_temp = json_access['main']['temp_max']
            lowest_temp = json_access['main']['temp_min']

            # Sending it
            weather_embed = discord.Embed(
                title=str(weather),
                colour=discord.Colour(0x00ffff),
                description="The temperature right now is ****"+str(temp)+
                            "°C**** but feels like ****"+str(feels_like)+"°C.**** The highest\
                              temperature all day has been ****"+str(highest_temp)+"°C**** with\
                              the lowest being ****"+str(lowest_temp)+"°C.****"
            )
            weather_embed.set_thumbnail(url=icon_url.format(icon))
            await ctx.send(embed=weather_embed)

        @self.bot_client.command()
        async def sauce(ctx, *userlink):
            await ctx.trigger_typing()
            snao_api = "646e73b5ea13820410201c76dbda0cb8b50e70d8"
            return_sauce = SauceNao(api_key=snao_api)

            if userlink:
                try:
                    # Gather Results
                    ani_results = return_sauce.from_url(userlink)
                    title = ani_results[0].title
                    sim_rate = ani_results[0].similarity
                    thumbnail = ani_results[0].thumbnail
                    author = ani_results[0].author
                    link = ani_results[0].urls
                    requests_remaining = ani_results.long_remaining

                    # ani_results_embed
                    ani_embed = discord.Embed(
                        title = '"'+title+'"',
                        colour = 0xbafc03,
                        description = "Similarity Rate: **"+str(sim_rate)+
                                      "%**\nAuthor: **"+str(author)+"**\n"+
                                      "[Link to image...]("+str(link[0])+")\n\n"+
                                      "Not quite what you're looking for? Use the '!rvrs_search' command."
                    )
                    ani_embed.set_footer(text="API requests remaining: "+str(requests_remaining))
                    ani_embed.set_image(url=str(thumbnail))
                    ani_embed.set_thumbnail(url=str(userlink[0]))
                    await ctx.send(embed=ani_embed)
                except UnknownClientError:
                    await ctx.send("Invalid link")
            else:
                await ctx.send("No link given")

        @self.bot_client.command()
        async def find(ctx, key, *search):
            await ctx.trigger_typing()
            if (key=="anime") or (key=="Anime"):
                # Creating Jikan wrapper instance 
                jikan = Jikan()
                results = jikan.search('anime', search, page=1)
    
                # Returning specific key information - Anime 
                title = results['results'][0]['title']
                stream_type = results['results'][0]['type']
                rating = results['results'][0]['score']
                episodes = results['results'][0]['episodes']
                image = results['results'][0]['image_url']
                airing = results['results'][0]['airing']
                desc = results['results'][0]['synopsis']
                rated = results['results'][0]['rated']

                # Ani-Embed 
                anisearch_embed = discord.Embed(
                    title=title+" - "+stream_type,
                    colour = 0x7aff21,
                    description="~ ＩＮＦＯ\nRATING: **"+str(rating)+
                                "**\nEPISODES: **"+str(episodes)+
                                "**\nIS AIRING?: **"+str(airing)+
                                "**\nRATED: **"+str(rated)+
                                "**\n\n~ ＳＹＮＯＰＳＩＳ\n"+str(desc)
                )
                anisearch_embed.set_thumbnail(url=image)

                # Sending gathered results 
                await ctx.send(embed=anisearch_embed)
            elif (key=="manga") or (key=="Manga"):
                # Creating Jikan wrapper instance 
                jikan = Jikan()
                results = jikan.search('manga', search, page=1)
    
                # Returning specific key information 
                title = results['results'][0]['title']
                chapters = results['results'][0]['chapters']
                publishing = results['results'][0]['publishing']
                stream_type = results['results'][0]['type']
                rating = results['results'][0]['score']
                desc = results['results'][0]['synopsis']
                image = results['results'][0]['image_url']

                # Ani-Embed 
                anisearch_embed = discord.Embed(
                    title=title+" - "+stream_type,
                    colour = 0x7aff21,
                    description="~ ＩＮＦＯ\nRATING: **"+str(rating)+
                                "**\nCHAPTERS: **"+str(chapters)+
                                "**\nIS PUBLISHING?: **"+str(publishing)+
                                "**\n\n~ ＳＹＮＯＰＳＩＳ\n"+str(desc)
                )
                anisearch_embed.set_thumbnail(url=image)

                # Sending gathered results 
                await ctx.send(embed=anisearch_embed)
            else:
                invalidsearchkey = discord.Embed(
                    title="Invalid search command",
                    description="~ If you want to search for anime its: `!a find anime JoJo` for example \
                                \n~ If you want to search for manga its: `!a find manga chainsawman` for example",
                    colour=0xff0011
                )
                # Sending error message 
                await ctx.send(embed=invalidsearchkey)

        @self.bot_client.command()
        async def search(ctx, *search):
            await ctx.trigger_typing()
            try: 
                # Setting up client object 
                api_key = "U2EKHK-PKXEVGK5TU"
                wolf_client = wolframalpha.Client(api_key)

                # Getting results 
                result_find = " ".join(search)
                api_results = wolf_client.query(str(result_find))
                return_ans = next(api_results.results).text

                # Returning results to user 
                await ctx.send(return_ans)
            except StopIteration:
                err_embed = discord.Embed(
                        title="Error :(",
                        description="You either asked the bot something that isn't academically "+
                                    "related or it just couldn't answer that question.",
                        colour=0xFF0000
                    )
                await ctx.send(embed=err_embed)

        @self.bot_client.command()
        async def isjordangay(ctx):
            await ctx.trigger_typing()
            response = ['of course', 'indubitably', 'thats a fact', 'yes', 'are you questioning his gayness?']
            s = len(response)
            rand_num = random.randint(0, s)
            await ctx.send(response[int(rand_num)])

# ------------------------------------------------------------------------------
startapp_bot = AssistantClass()
