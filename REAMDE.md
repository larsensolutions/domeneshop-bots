# Domeneshop.no DNS boot

Bot for users of domeneshop.no. Keep your dns records updated with external ip for your self hosted sites and services.

See the documentation at https://api.domeneshop.no/docs/ for help on how to acquire your API credentials.

**Only IP will be updated by the bot; record type, ttl and hostname will remain the same**

```
pip3 install 
```

## Example usage

1. Fill inn API credentials and which domains/hostnames to track
```json
{
  "currentIp": "will be autofilled",
  "track": [
    {
      "domain": "yourdomainA.com",
      "hosts": ["subdomainA", "subdomainB", "subdomainC"]
    },
    { "domain": "yourdomainB.com", 
      "hosts": ["@", "www"] 
    }
  ],
  "api":{
      "token":"<your-domeneshop.no-token>",
      "secret":"<your-domeneshop.no-secret>"
  }
}
```
### Hostname types

* "@" -> https://domain.com
* "www" -> https://www.domain.com
* "subdomain" -> https://subdomain.domain.com

2. Fire the bot up
```python
from domeneshop_bots import DNSBot


if __name__ == "__main__":
    bot = DNSBot("<path-to-your-config>")
    bot.start()

```