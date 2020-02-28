"""
Example usage of the domeneshop bot

"""
import json
from domeneshop_bots import DNSBot


if __name__ == "__main__":
    with open("./config.json", 'r') as file:
        config = json.loads(file.read())
        bot = DNSBot(config, verbose=True)
        bot.start(interval=1)
