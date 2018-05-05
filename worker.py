import os
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import requests
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

Client = discord.Client()
client = commands.Bot(command_prefix = "!")
GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"
CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"


@client.event
async def on_ready():
    print("Bot is online and connected to Discord!")

@client.event
async def on_message(message):
    if message.content.lower().startswith("!stockx"):

        userID = message.author.id

        urlname = message.content.replace("!stockx ","").lower()
        #driver = webdriver.Chrome("/Users/Zain/AppData/Local/Programs/Python/Python36/Lib/site-packages/selenium/webdriver/chrome/chromedriver")  # Optional argument, if not specified will search path.
        #driver = webdriver.Chrome()

        chrome_options = Options()
        chrome_options.binary_location = GOOGLE_CHROME_BIN
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(executable_path = CHROMEDRIVER_PATH, chrome_options = chrome_options)
            
        driver.get("https://stockx.com/search?s=" + urlname);
        delay = 25
        lowestAskValueList = []
        retailPriceList = []

        try:
            wait = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
            print("Page is ready!")
            shoeURL = driver.find_elements_by_tag_name("a")
            shoeURL = shoeURL[32].get_attribute("href")
                                        
            driver.get(shoeURL)

            shoeName = (driver.find_element_by_class_name("name"))
            lastSaleValue = (driver.find_element_by_class_name("sale-value")).text
            lastSaleSize = (driver.find_elements_by_tag_name("span"))
            lowestAskValue = (driver.find_element_by_tag_name("div")).text
            for line in lowestAskValue.splitlines():
                lowestAskValueList.append(line)
            lowestAskSize = (driver.find_element_by_tag_name("div"))
            highestBidValue = (driver.find_element_by_tag_name("div"))
            highestBidSize = (driver.find_element_by_tag_name("div"))
            retailPrice = (driver.find_elements_by_tag_name("span"))
            if "h" in (retailPrice[49].text).lower():
                retailPrice[49] = "N/A"
            else:
                retailPrice[49] = retailPrice[49]
            averageSalePrice = (driver.find_elements_by_class_name("gauge-value"))

            '''await client.send_message(message.channel, "<@%s> StockX Information" % (userID))
            await client.send_message(message.channel, "Shoe Name: " + shoeName.text)
            await client.send_message(message.channel, "Last Sale Price: " + lastSaleValue)
            await client.send_message(message.channel, "Last Sale Size: " + lastSaleSize[23].text)
            await client.send_message(message.channel, "Lowest Ask Price: " + lowestAskValueList[23])
            await client.send_message(message.channel, "Lowest Ask Size: " + lowestAskValueList[27])
            await client.send_message(message.channel, "Highest Bid Size: " + lowestAskValueList[33])
            await client.send_message(message.channel, "Retail Price: " + retailPrice[49].text)
            await client.send_message(message.channel, "Average Sale Price: " + averageSalePrice[2].text)

            await client.send_message(message.channel,"<@%s> StockX Information" % (userID) +
                                                      "\nShoe Name: " + shoeName.text +
                                                      "\nStockX Link: " + str(shoeURL) +
                                                      "\n\nLast Sale Price: " + lastSaleValue +
                                                      "\nLast Sale Size: " + lastSaleSize[23].text +
                                                      "\n\nLowest Ask Price: " + lowestAskValueList[23] +
                                                      "\nLowest Ask Size: " + lowestAskValueList[27] +
                                                      "\n\nHighest Bid Price: " + lowestAskValueList[29] +
                                                      "\nHighest Bid Size: " + lowestAskValueList[33] +
                                                      "\n\nRetailPrice: " + retailPrice[49].text +
                                                      "\nAverage Sale Price: " + averageSalePrice[2].text)'''

            em = discord.Embed(title = shoeName.text, url = shoeURL)
            em.add_field(name = "Last Sale Price", value = lastSaleValue, inline = True)
            em.add_field(name = "Last Sale Size", value = lastSaleSize[23].text, inline = True)
            em.add_field(name = "\u200b", value = "\u200b")
            em.add_field(name = "Lowest Ask Price", value = lowestAskValueList[23], inline = True)
            em.add_field(name = "Lowest Ask Size", value = lowestAskValueList[27], inline = True)
            em.add_field(name = "\u200b", value = "\u200b")
            em.add_field(name = "Highest Bid Price", value = lowestAskValueList[29], inline = True)
            em.add_field(name = "Highest Bid Size", value = lowestAskValueList[33], inline = True)
            em.add_field(name = "\u200b", value = "\u200b")
            em.add_field(name = "Retail Price", value = retailPrice[49].text, inline = True)
            em.add_field(name = "Average Sale Price", value = averageSalePrice[2].text, inline = True)
            em.add_field(name = "\u200b", value = "\u200b")
            await client.send_message(message.channel, embed = em)
            
        except TimeoutException:
            print("Loading took too much time! Timed out")
            
client.run("NDM5NDYyNjYwMDYxNTI4MDc4.DcTwAg.clVEOYntxI2UkgmcT-zbpmET4G8")
