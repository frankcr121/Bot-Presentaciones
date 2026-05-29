from playwright.sync_api import sync_playwright
from lib_resources.principal import *
def main():
    with sync_playwright() as p:
            is_headless = True
            browser = p.chromium.launch(headless=is_headless, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'])
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
            page = context.new_page()
            page.goto("https://fas.crp.com.pe/os/dbstudio#/tabs/studio%2Fprimary%2FDatabases%2Fcrp_ifas%2FSQL", wait_until="networkidle")
            proceso(page)
            browser.close()

main()