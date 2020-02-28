"""
Tests

"""

import unittest
import sys
sys.path.append("..")
from domeneshop_bots import DNSBot


class TestDNSBot(unittest.TestCase):
    @unittest.expectedFailure
    def test_wrong_type(self):
        DNSBot("")

    @unittest.expectedFailure
    def test_empty_config(self):
        DNSBot({}, verbose=False)

    @unittest.expectedFailure
    def test_missing_config(self):
        DNSBot({
            "api": {
                "token": "<your-domeneshop.no-token>"
            },
            "track": [
                {
                    "domain": "yourdomainA.com",
                    "hosts": ["subdomainA", "subdomainB", "subdomainC"]
                },
                {"domain": "yourdomainB.com",
                 "hosts": ["@", "www"]
                 }
            ]
        })


    def test_correct_config_schema(self):
        DNSBot({
            "api": {
                "token": "<your-domeneshop.no-token>",
                "secret": "<your-domeneshop.no-secret>"
            },
            "track": [
                {
                    "domain": "yourdomainA.com",
                    "hosts": ["subdomainA", "subdomainB", "subdomainC"]
                },
                {"domain": "yourdomainB.com",
                 "hosts": ["@", "www"]
                 }
            ]
        }, verbose=True)


if __name__ == '__main__':
    unittest.main()
