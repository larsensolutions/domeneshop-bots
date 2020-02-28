"""
Domeneshop DNS bot

Relies on external service of https://api.ipify.org

"""
import sys
import logging
import time
import json
import pprint
import schedule
from requests import get
from domeneshop import Client

from domeneshop_bots import helper


def print_domain_records(client, domain):
    """ Print records """
    pprint.pprint("DNS records for {0}:".format(domain["domain"]))
    for record in client.get_records(domain["id"]):
        pprint.pprint(record)


def print_domains(client):
    """ Print all domains """
    for domain in client.get_domains():
        pprint.pprint(domain)
        print_domain_records(client, domain)


def get_remote_ip():
    """Get the remote IP address"""
    ip = get('https://api.ipify.org').text
    return ip


class DNSBot:
    """
    Domeneshop DNS bot

    """

    @helper.on_error(msg="Failed to open config.")
    def __init__(self, path: str, verbose=False):
        """
        See the documentation at https://api.domeneshop.no/docs/ for
        help on how to acquire your API credentials.

        :param path: Path to config json

        """
        self.logger = logging.getLogger("DNSBot")
        if verbose:
            self.logger.debug("Setting verbose logging")
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        self.running = False
        with open(path, 'r') as file:
            self.config = json.loads(file.read())

    @helper.on_error(msg="Failed to start service.")
    def start(self):
        """
        Start the dns bot service

        """
        self.logger.debug("Setting up bot job, checking dns every 1 minutes")
        self.running = True
        schedule.every(1).minutes.do(self.has_ip_changed)

        while self.running:
            schedule.run_pending()
            time.sleep(1)

    @helper.on_error(msg="Something went wrong trying to stop the bot")
    def stop(self):
        """
        Stop the dns bot service

        """
        self.logger.debug("Stopping bot job")
        self.running = False
        schedule.clear()

    @helper.on_error(msg="Cant get remote IP address. Internet or https://api.ipify.org service is down.")
    def has_ip_changed(self):
        """
        Job to see if the ip has changed. Will check agains domeneshop first time the bot shcedule is running

        """
        self.logger.debug("Running bot job")
        remote_ip = get_remote_ip()
        if remote_ip != self.config["currentIp"]:
            self.__run_dns_update_job__(remote_ip)
        else:
            self.logger.debug("IP has not changed since last time")

    @helper.on_error(msg="Unable to update domeneshop dns records.")
    def __run_dns_update_job__(self, ip: str):
        """
        Iterate through all domeneshop dns records that are being tracked and updates the ip
        if is necessary.

        :param ip: the new ip to update the dns records with

        """
        self.logger.debug("Calling domeneshop and checking dns records")
        update = self.config["track"]
        client = Client(self.config["api"]["token"], self.config["api"]["secret"])
        domains = client.get_domains()
        to_update = [domain for domain in domains if any(domain["domain"] == x["domain"] for x in update)]
        for domain in to_update:
            self.logger.debug("Checking domain: %s", domain["domain"])
            source = next(source for source in update if domain["domain"] == source["domain"])
            records = client.get_records(domain["id"])
            records_to_update = [record for record in records if record["data"] != ip and any(host for host in source["hosts"] if host in record["host"])]
            for record in records_to_update:
                mod = {
                    "data": ip,
                    "type": record["type"],
                    "host": record["host"],
                    "ttl": record["ttl"]
                }
                self.logger.debug("Updating dns record %s", str(mod))
                client.modify_record(domain["id"], record["id"], mod)
