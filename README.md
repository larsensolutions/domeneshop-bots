# Domeneshop.no DNS boot
Bot for users of domeneshop.no. Keep your dns records updated with external ip for your self hosted sites and services.

See the documentation at https://api.domeneshop.no/docs/ for help on how to acquire your API credentials.

**Only IP will be updated by the bot; record type, ttl and hostname will remain the same**

* Built upon [domeneshop.no's own python API](https://github.com/domeneshop/python-domeneshop). 
* Relies on the external service of https://api.ipify.org

# Installation
```
pip3 install domeneshop-bots
```

## Example usage
1. Fill inn API credentials and which domains/hostnames to track
```json
{
   "api":{
      "token":"<your-domeneshop.no-token>",
      "secret":"<your-domeneshop.no-secret>"
  },
  "track": [
    {
      "domain": "yourdomainA.com",
      "hosts": ["subdomainA", "subdomainB", "subdomainC"]
    },
    { "domain": "yourdomainB.com", 
      "hosts": ["@", "www"] 
    },
    { "domain": "yourdomainC.com", 
      "hosts": ["@", "www", "subdomain"] 
    }
  ]
}
```
### Hostname defaults
* "@" -> https://domain.com : domeneshop.no uses '@' to indicate root domain
* "www" -> https://www.domain.com : in case you have added a 'www' dns to root domain as well

* "subdomain" -> https://subdomain.domain.com : only subdomain should be specified

2. Fire the bot up, example loading json from file
```python
import json
from domeneshop_bots import DNSBot


if __name__ == "__main__":
    with open("./config.json", 'r') as file:
        config = json.loads(file.read())
        bot = DNSBot(config)
        bot.start()

```