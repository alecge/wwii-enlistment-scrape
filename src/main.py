import logging
import argparse
import subprocess
import scraper.scraper as scraper
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)


def convert_html():
    pass


def main():
    argparser = argparse.ArgumentParser(
        description="Scrape the site, convert HTML, and/or push to a PostgreSQL database")
    argparser.add_argument("action")
    argparser.add_argument("-D", action="store_true")

    args = argparser.parse_args()

    args = argparser.parse_args()
    if args.action == "scrape":
        if args.D:
            scraper.run()
        else:
            p = subprocess.run(["docker-compose", "up", "--build"])
    elif args.action == "csv":
        pass
    elif args.action == "postgres":
        pass
    else:
        print("Invalid args")


main()
