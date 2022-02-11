import os

import discord
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# DISCORD
ALERT_CHANNEL = os.getenv("ERROR_ALERT_CHANNEL")
TEST_CHANNEL = os.getenv("TEST_CHANNEL")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
MY_USER_ID = os.getenv("MY_USER_ID")
DEVS_ID = os.getenv("DEVS_ID")

# TWILIO
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUM = os.getenv("TWILIO_PHONE_NUMBER")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER")
TWILIO_URL = "http://demo.twilio.com/docs/voice.xml"


def twilio_call():
    # if any of the env vars are missing, exit
    if not all([TWILIO_SID, TWILIO_TOKEN, TWILIO_PHONE_NUM, MY_PHONE_NUMBER]):
        print("Missing environment variables")
        raise Exception("Missing environment variables")

    client = Client(TWILIO_SID, TWILIO_TOKEN)
    call = client.calls.create(
        to=MY_PHONE_NUMBER, from_=TWILIO_PHONE_NUM, url=TWILIO_URL
    )
    print(f"Call initiated with SID: {call.sid}")


def main():
    # create discord client
    client = discord.Client()

    if not all([DISCORD_TOKEN, ALERT_CHANNEL, TEST_CHANNEL, MY_USER_ID]):
        print("Missing environment variables")
        raise Exception("Missing environment variables")

    @client.event
    async def on_ready():
        print(f"{client.user} has connected to Discord!")

    @client.event
    async def on_message(message: discord.Message):
        if message.author == client.user:
            return  # ignore self message

        isTestChannel = str(message.channel.id) == TEST_CHANNEL
        isAlertChannel = str(message.channel.id) == ALERT_CHANNEL

        # either test channel, or Sifa bot in alert channel
        if isTestChannel or isAlertChannel:
            if "greater than 10% of total balance" in message.content:
                await message.channel.send(
                    f"Account suffers great loss, Bot will initiate call"
                )
                twilio_call()

    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
