import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    #browser = playwright.chromium.launch(headless=True)
    import platform
    browser = playwright.chromium.launch(headless=platform.system() != "Windows", executable_path=find_chrome_util())
    
    context = browser.new_context(color_scheme="dark", storage_state=r"auth.json")
    
    page = context.new_page()
    timeout = 120 * 1000
    page.set_default_navigation_timeout(timeout)  # 2 分钟
    page.set_default_timeout(timeout)
    
    page.goto("https://www.xianyudanji.to/tg")
    page.get_by_role("link", name=" 每日签到").click()
    page.get_by_role("button", name=" 每日签到").click()
    page.goto("https://www.xianyudanji.to/user/aff")
    print(page.locator("#main > div:nth-child(2)").evaluate("element => element.innerText").split("签到")[0]+"签到")

    # ---------------------
    context.storage_state(path=r"auth.json")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
