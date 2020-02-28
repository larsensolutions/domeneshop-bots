"""
Domeneshop DNS bot

Relies on external service of https://api.ipify.org

"""
import sys
import logging
import time
import schedule
from requests import get
from domeneshop import Client

from .helper import on_error, validator


def get_remote_ip():
    """Get the remote IP address"""
    ip = get('https://api.ipify.org').text
    return ip


class DNSBot:
    """
    Domeneshop DNS bot

    """

    @validator(schema={
        "type": "object",
        "properties": {
            "api": {
                "type": "object",
                "properties": {
                    "token": {"type": "string"},
                    "secret": {"type": "string"}
                },
                "required": ["token", "secret"]
            },
            "track": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "domain": {"type": "string"},
                        "hosts":  {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["domain", "hosts"]
                }
            }
        },
        "required": ["api", "track"]
    })
    def __init__(self, config: dict, verbose: bool = False):
        """
        See the documentation at https://api.domeneshop.no/docs/ for
        help on how to acquire your API credentials.

        :param config: config dictionary
        :param verbose: Turn on verbose logging
        """
        self.logger = logging.getLogger("DNSBot")
        if verbose:
            self.logger.debug("Verbose logging ON")
            logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        self.current_ip = None
        self.running = False
        self.track = config["track"]
        self.token = config["api"]["token"]
        self.secret = config["api"]["secret"]

    @on_error(msg="Failed to start bot.")
    def start(self, interval: int = 10):
        """
        Start the dns bot service

        :param interval: spesify how often the bot should check for IP changes. Defaults to 10 minutes.

        """
        self.logger.debug("Setting up bot job, checking dns every 1 minutes")
        self.running = True
        schedule.every(interval).minutes.do(self.has_ip_changed)

        while self.running:
            schedule.run_pending()
            time.sleep(1)

    @on_error(msg="Failed to stop bot")
    def stop(self):
        """
        Stop the dns bot service

        """
        self.logger.debug("Stopping bot job")
        self.running = False
        schedule.clear()

    @on_error(msg="Cant get remote IP address. Internet or https://api.ipify.org service is down. Will try again at next job run.")
    def has_ip_changed(self):
        """
        Job to see if the ip has changed. Will check agains domeneshop first time the bot shcedule is running

        """
        self.logger.debug("Running bot job")
        remote_ip = get_remote_ip()
        if remote_ip != self.current_ip:
            self.__run_dns_update_job__(remote_ip)
        else:
            self.logger.debug("IP has not changed since last time. All good!")

    @on_error(msg="Unable to update domeneshop dns records.")
    def __run_dns_update_job__(self, ip: str):
        """
        Iterate through all domeneshop dns records that are being tracked and updates the ip
        if is necessary.

        :param ip: the new ip to update the dns records with

        """
        self.logger.debug("Calling domeneshop and checking dns records")
        self.logger.debug("Setting current external ip to %s", ip)
        self.current_ip = ip

        client = Client(self.token, self.secret)
        domains = client.get_domains()
        to_update = [domain for domain in domains if any(domain["domain"] == x["domain"] for x in self.track)]

        for domain in to_update:
            self.logger.debug("Checking IP on tracked records for domain: %s", domain["domain"])
            source = next(source for source in self.track if domain["domain"] == source["domain"])
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
            if not records_to_update:
                self.logger.debug("No update needed for any records for this domain")
