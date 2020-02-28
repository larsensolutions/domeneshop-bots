"""
Use the DomeneshopBot

"""
from domeneshop_bots import DNSBot


if __name__ == "__main__":
    bot = DNSBot("./config.json")
    bot.has_ip_changed()
