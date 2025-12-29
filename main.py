from playwright.sync_api import sync_playwright
from colorama import Fore as F
import random
import time

# Files
from AllowedWebsites import websites
from Buttons import reject_buttons

print(F.LIGHTWHITE_EX + "Hello. I'm the bot Botron. I will visit random websites from which I am allowed." + F.RESET)
time.sleep(1)
print() # Blank line
print() # Blank line



with sync_playwright() as p:
    while True:
        site = random.choice(websites)
        print(f"Visit: {site}")
        
        browser = p.chromium.launch(headless=False)  # visible browser
        page = browser.new_page()
        
        try:
            page.goto(site, timeout=30000)
            
            #  Button check permanently while the page is open
            clicked = False
            start_time = time.time()
            while time.time() - start_time < 3:   # Check for 3 seconds
                for text in reject_buttons:
                    try:
                        locators = page.get_by_text(text, exact=False)
                        count = locators.count()
                        
                        for i in range(count):
                            btn = locators.nth(i)
                            if btn.is_visible():
                                btn.click()
                                print(f"Button '{text}' clicked.")
                                clicked = True
                                time.sleep(0.5)  # Wait after click
                                break
                        if clicked:
                            break
                    except:
                        continue
                if clicked:
                    break
                time.sleep(0.3)  # Check again every 300 milliseconds

            if not clicked:
                print(f"No decline button found on {site}.")

            # Bot scrolls down
            for _ in range(random.randint(3, 15)):
                page.mouse.wheel(0, 50)
                time.sleep(0.25)

            time.sleep(1)

            # bot scrolls back to top
            for _ in range(15):
                page.mouse.wheel(0, -70)
                time.sleep(0.25) # Scroll once every 250 milliseconds

            time.sleep(1)  # Wait
            print(f"Close: {site}\n")
            
        except Exception as e:
            print(f"Error at {site}: {e}")
        
        finally:
            browser.close()