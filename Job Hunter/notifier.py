import requests

class DiscordNotifier:
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_alert(self, job):
        # Color coding: Green (0x2ecc71) for Entry Level, Blue (0x3498db) for others
        color = 0x3498db
        title_lower = job['title'].lower()

        # Highlight entry-level positions
        if any(x in title_lower for x in ['junior', 'entry', 'intern', 'associate']):
            color = 0x2ecc71

        payload = {
            "embeds": [
                {
                    "title": job['title'],
                    "url": job['url'],
                    "color": color,
                    "fields": [
                        {
                            "name": "🏢 Company",
                            "value": job['company'],
                            "inline": True
                        },
                        {
                            "name": "📍 Source",
                            "value": "RSS Aggregator",
                            "inline": True
                        }
                    ],
                    "footer": {
                        "text": "Job Hunter Bot • Automated with Python"
                    }
                }
            ]
        }

        try:
            response = requests.post(self.webhook_url, json=payload)

            if response.status_code not in [200, 204]:
                print(f"[Discord] API Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"[Discord] Connection Error: {e}")