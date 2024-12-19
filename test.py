# import asyncio
# from pyppeteer import launch

# async def scrape_disconnected_sensors():
#     # Path to the system's Chrome executable
#     chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Update for your OS if needed

#     # Launch Chrome instead of Chromium
#     browser = await launch(
#         headless=False,
#         executablePath=chrome_path,
#         args=['--no-sandbox', '--disable-setuid-sandbox']
#     )

#     page = await browser.newPage()

#     try:
#         # Set the viewport size
#         await page.setViewport({'width': 1366, 'height': 768})

#         # Set a realistic user-agent
#         await page.setUserAgent(
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#         )

#         # Navigate to the login page
#         await page.goto("https://cyberdome.us/login", waitUntil='networkidle2', timeout=60000)

#         # Wait for the username input and type the username
#         await page.waitForSelector('#mat-input-0', timeout=30000)
#         await page.type('#mat-input-0', 'your_username', {'delay': 50})  # Replace with your actual username

#         # Wait for the "Next" button to enable
#         await page.waitForFunction('document.querySelector("#login-button").disabled === false', timeout=30000)

#         # Click the "Next" button
#         await page.click('#login-button')

#         # Wait for the password input field
#         await page.waitForSelector('#password', timeout=30000)
#         await page.type('#password', 'your_password', {'delay': 50})  # Replace with your actual password

#         # Wait for and click the final login button
#         await page.waitForSelector('#password-login-button', timeout=300000)
#         await page.click('#password-login-button')

#         # Wait for navigation to confirm successful login
#         await page.waitForNavigation(waitUntil='networkidle2', timeout=60000)

#         # Navigate to the target page
#         await page.goto("https://cyberdome.us/system/collect/sensors", waitUntil='networkidle2', timeout=60000)

#         # Wait for grid cells and scrape data
#         await page.waitForSelector('[role="gridcell"]', timeout=30000)
#         grid_data = await page.evaluate('''() => {
#             let elements = Array.from(document.querySelectorAll('[role="gridcell"]'));
#             return elements.map(el => el.innerText || el.textContent);
#         }''')

#         # Filter disconnected sensors
#         disconnected_sensors = [text for text in grid_data if "Disconnected" in text]
#         print("Disconnected Sensors:", disconnected_sensors)

#     except Exception as e:
#         # Save error screenshot for debugging
#         await page.screenshot({'path': 'error_screenshot.png'})
#         print(f"An error occurred: {e}")
#     finally:
#         await browser.close()

# if __name__ == "__main__":
#     asyncio.get_event_loop().run_until_complete(scrape_disconnected_sensors())

import asyncio
from pyppeteer import launch

async def scrape_disconnected_sensors():
    # Path to the system's Chrome executable
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # Update for your OS if needed

    # Launch Chrome instead of Chromium
    browser = await launch(
        headless=False,
        executablePath=chrome_path,
        args=['--no-sandbox', '--disable-setuid-sandbox', '--start-maximized']
    )

    page = await browser.newPage()

    try:
        # Set the viewport size
        await page.setViewport({'width': 2100, 'height': 1000})

        # Set a realistic user-agent
        await page.setUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        # Navigate to the login page
        await page.goto("https://cyberdome.us/login", waitUntil='networkidle2', timeout=60000)

        # Wait for the username input and type the username
        await page.waitForSelector('#mat-input-0', timeout=30000)
        await page.type('#mat-input-0', 'your_username', {'delay': 50})  # Replace with your actual username

        # Wait for the "Next" button to enable
        await page.waitForFunction('document.querySelector("#login-button").disabled === false', timeout=30000)

        # Click the "Next" button
        await page.click('#login-button')

        # Wait for the password input field
        await page.waitForSelector('#password', timeout=30000)
        await page.type('#password', 'your_password', {'delay': 50})  # Replace with your actual password

        # Wait for and click the final login button
        await page.waitForSelector('#password-login-button', timeout=300000)
        await page.click('#password-login-button')

        # Wait for navigation to confirm successful login
        await page.waitForNavigation(waitUntil='networkidle2', timeout=60000)

        # Debugging: Save the HTML content after login
        with open('post_login_page.html', 'w', encoding='utf-8') as f:
            f.write(await page.content())

        # Manually navigate to the sensors page
        await page.goto("https://cyberdome.us/system/collect/sensors", waitUntil='networkidle2', timeout=60000)

        # Debugging: Save the sensors page content
        with open('sensors_page.html', 'w', encoding='utf-8') as f:
            f.write(await page.content())

        # Wait for grid cells and scrape data
        await page.waitForSelector('[role="gridcell"]', timeout=30000)
        grid_data = await page.evaluate('''() => {
            let elements = Array.from(document.querySelectorAll('[role="gridcell"]'));
            return elements.map(el => el.innerText || el.textContent);
        }''')

        # Filter disconnected sensors
        disconnected_sensors = [text for text in grid_data if "Disconnected" in text]
        print("Disconnected Sensors:", disconnected_sensors)

    except Exception as e:
        # Save error screenshot for debugging
        await page.screenshot({'path': 'error_screenshot.png'})
        print(f"An error occurred: {e}")
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(scrape_disconnected_sensors())
