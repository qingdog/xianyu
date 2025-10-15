import re
from playwright.sync_api import Playwright, sync_playwright, expect
from playwright.sync_api import TimeoutError
import time
import datetime
import os
from find_chrome_util import find_chrome_util

def run(playwright: Playwright) -> None:
    '''browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(color_scheme="dark", storage_state="auth.json")'''
    import platform
    browser = playwright.chromium.launch(headless=platform.system() != "Windows", executable_path=find_chrome_util())
    context = browser.new_context(color_scheme="dark")
    page = context.new_page()
    
    page.goto("http://www.xianyudanji.ai/")
    '''
    try: page.goto('https://example.com', wait_until='domcontentloaded', timeout=3000)
    except Exception as e: 
        print("timeout...")
        page.wait_for_timeout(5000)
    # 然后显式等待某个特定元素出现（更可靠）
    #await page.wait_for_selector('div.main-content', state='visible')
    # 或者等待一段时间让JS执行
    page.wait_for_timeout(1000)
    '''
    page.get_by_role("button", name="Close this dialog").click()
    page.get_by_role("link", name=" 登录").click()
    page.get_by_role("textbox", name="请输入电子邮箱/用户名").click()
    page.get_by_role("textbox", name="请输入电子邮箱/用户名").fill("1759765836@qq.com")
    page.get_by_role("textbox", name="请输入电子邮箱/用户名").press("Tab")
    page.get_by_role("link", name="忘记密码？").press("Tab")
    page.get_by_role("textbox", name="请输入密码").fill("1759765836")
    page.get_by_role("button", name="立即登录").click()
    
    try:
        # 尝试访问页面
        #page.goto("https://www.baidu.com/", timeout=30000)
        page.goto("https://www.xianyudanji.ai/", timeout=30000)
        print("页面加载成功")
    except Exception as e:
        if "ERR_ABORTED" in str(e) or "ERR_CONNECTION_RESET" in str(e):
            print("页面打开超时了timeout=30000...")
            print(e)
            page.wait_for_timeout(2000)
        else:
            raise e
    
    max_retries = 1
    for attempt in range(max_retries):
        try:
        
            page.get_by_role("link", name="签到领永久赞助").click(button="right")
            page.get_by_role("link", name="立即签到").click()
            #page.get_by_role("link", name=" 登录").click()
            
            try:
                import os
                from dotenv import load_dotenv
                load_dotenv()

                page.get_by_role("textbox", name="请输入电子邮箱/用户名").click()
                page.get_by_role("textbox", name="请输入电子邮箱/用户名").fill(os.getenv("username"))
                page.get_by_role("textbox", name="请输入电子邮箱/用户名").press("Tab")
                page.get_by_role("link", name="忘记密码？").press("Tab")
                page.get_by_role("textbox", name="请输入密码").fill(os.getenv("password"))
                page.get_by_role("button", name="立即登录").click()
            except Exception as e:
                print(e)
            
            page.get_by_role("button", name=" 每日签到").click()
            print("每日点击成功！")
            break
        except TimeoutError as e:
            print(f"第 {attempt + 1} 次尝试失败")
            import io
            import sys
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')#改变标准输出的默认编码，修复win打印特殊字符
            print(e)
            
            # 生成带时间戳的截图文件名
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_filename = f"timeout_error_attempt_{attempt + 1}_{timestamp}.png"
            
            import platform
            # 截图保存
            if platform.system() == "Windows":
                page.screenshot(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), screenshot_filename), full_page=True)
                print(f"已保存截图: {screenshot_filename}")
            
            # 额外的调试信息
            print(f"当前URL: {page.url} 页面标题: {page.title()}")
            
            # 检查页面上的按钮数量
            buttons_count = page.get_by_role("button").count()
            print(f"页面上的按钮数量: {buttons_count}")
            
            # 检查包含"每日"文本的元素
            daily_elements = page.get_by_text("每日", exact=False).count()
            print(f"包含'每日'文本的元素数量: {daily_elements}")
            
            if attempt == max_retries - 1:
                print("所有重试尝试均失败")
                raise
            else:
                print(f"等待2秒后重试... ({attempt + 1}/{max_retries})")
                time.sleep(2)
                page.reload()  # 重新加载页面
                # 等待页面重新加载完成
                page.wait_for_load_state("networkidle")
        except Exception as e:
            print(e)
        
    
    #page.goto("https://www.xianyudanji.ai/user/aff")
    #page.get_by_text("赞助币钱包 0.9 当前余额 0 累计消费 今日已签到").click(button="right")
    title = page.evaluate('document.title')
    print(f"页面标题: {title}")  # 输出: 页面标题: Example Domain
    #result = page.evaluate('document.querySelectorAll("div.card-body")[0].textContent')
    text_from_selector = page.evaluate('''(args) => {
        return document.querySelectorAll(args[1])[args[0]].textContent;
    }''', [0, "div.card-body"])  # 传递一个列表
    print(text_from_selector)


    # ---------------------
    context.storage_state(path="auth.json")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
