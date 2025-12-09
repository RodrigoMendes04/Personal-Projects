import feedparser

class JobScraper:
    def __init__(self, url):
        self.url = url

    def fetch_jobs(self):
        print(f"[Scraper] Reading RSS Feed: {self.url}...")

        feed = feedparser.parse(self.url)
        jobs_data = []

        if feed.bozo:
            print(f"   -> [Warning] Error parsing feed or invalid XML format.")
            return []

        for entry in feed.entries:
            try:
                title = entry.title
                link = entry.link

                # Attempt to extract author/company, fallback to 'Unknown'
                company = "Unknown"
                if 'author' in entry:
                    company = entry.author

                jobs_data.append({
                    "title": title,
                    "company": company,
                    "url": link
                })

            except AttributeError:
                continue

        print(f"[Scraper] Success! {len(jobs_data)} jobs extracted via RSS.")
        return jobs_data