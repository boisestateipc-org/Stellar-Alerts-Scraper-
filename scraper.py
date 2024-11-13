# import asyncio
# from pyppeteer import launch

# async def scrape_sensors():
#     # Launch a headless browser instance
#     browser = await launch(headless=True)
#     page = await browser.newPage()

#     # Navigate to the given URL
#     url = "https://cyberdome.us/system/collect/sensors"
#     await page.goto(url)

#     # Wait for the page to load specific content (adjust selector as needed)
#     await page.waitForSelector('table')  # Replace with actual table or sensor selector

#     # Extract sensor data from the page (assuming data is in a table)
#     sensors = await page.evaluate('''
#         () => {
#             const rows = document.querySelectorAll('table tr');
#             let data = [];
#             rows.forEach(row => {
#                 const cells = row.querySelectorAll('td');
#                 if (cells.length > 1) {
#                     const name = cells[0].innerText.trim();
#                     const status = cells[1].innerText.trim();
#                     data.push({ name, status });
#                 }
#             });
#             return data;
#         }
#     ''')

#     # Close the browser
#     await browser.close()

#     # Process and print sensor data
#     for sensor in sensors:
#         status_text = "Active" if "active" in sensor['status'].lower() else "Inactive"
#         print(f"Sensor: {sensor['name']} - Status: {status_text}")

# # Run the asyncio event loop
# asyncio.get_event_loop().run_until_complete(scrape_sensors())
