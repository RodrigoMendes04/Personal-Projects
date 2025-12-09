import os
import time
from dotenv import load_dotenv
from database import JobDatabase
from scraper import JobScraper
from notifier import DiscordNotifier

# Load environment variables
load_dotenv()
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

if not DISCORD_WEBHOOK:
    print("ERROR: Webhook URL not found in .env file.")
    exit()

# --- CONFIGURATION ---

TARGET_URLS = [
    # We Work Remotely Feeds
    "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
    "https://weworkremotely.com/categories/data-science-jobs.rss",
    "https://weworkremotely.com/categories/remote-python-jobs.rss",
    # RemoteOK Feed
    "https://remoteok.com/rss"
]

# Keywords required in the title (Whitelist)
TECH_KEYWORDS = [
    "python", "django", "flask", "fastapi", "sql", "data", "aws", "cloud",
    "backend", "back-end", "frontend", "front-end", "full stack", "fullstack",
    "devops", "engineer", "developer", "programmer", "bot", "scraping", "etl",
    "react", "node", "javascript", "gis", "automation", "ai", "machine learning"
]

# Keywords that disqualify the job (Blacklist)
EXCLUDED_KEYWORDS = [
    "senior", "lead", "principal", "manager", "head of", "director",
    "vp", "architect", "staff "
]

def filter_job(job_title):
    """
    Returns True if the job matches criteria, False otherwise.
    Logic: Must not contain excluded words AND must contain at least one tech keyword.
    """
    title = job_title.lower()

    # 1. Exclusion Check
    for bad_word in EXCLUDED_KEYWORDS:
        if bad_word in title:
            return False

    # 2. Tech Relevance Check
    has_tech = False
    for tech in TECH_KEYWORDS:
        if tech in title:
            has_tech = True
            break

    return has_tech

def main():
    db = JobDatabase()
    notifier = DiscordNotifier(DISCORD_WEBHOOK)

    print("--- Starting Multi-Source Extraction ---")

    for url in TARGET_URLS:
        scraper = JobScraper(url)
        jobs_found = scraper.fetch_jobs()

        new_jobs_count = 0

        for job in jobs_found:
            # Skip if already in DB
            if db.job_exists(job['url']):
                continue

            # Apply Filters
            if filter_job(job['title']):
                db.add_job(job['title'], job['company'], job['url'])
                notifier.send_alert(job)
                new_jobs_count += 1
                time.sleep(0.5) # Rate limiting for Discord API

        if new_jobs_count > 0:
            print(f"   > {new_jobs_count} new alerts sent from: {url.split('/')[-1]}")
        else:
            print(f"   > No new relevant jobs from: {url.split('/')[-1]}")

    db.close()
    print("--- Cycle Complete ---")

if __name__ == "__main__":
    main()