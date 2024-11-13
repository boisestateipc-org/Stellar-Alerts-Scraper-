import asyncio
from pyppeteer import launch
import smtplib
from email.mime.text import MIMEText

async def check_disconnected_sensors():
    # Launch a new browser
    browser = await launch(headless=True)
    page = await browser.newPage()

    # Navigate to the Stellar Cyber sensors page
    await page.goto("https://cyberdome.us/system/collect/sensors")

    # Wait for the sensor data to load on the page
    await page.waitForSelector('[comp-id="2791"]')  # Using as an example for now

    # Evaluate the page to extract disconnected sensors
    sensor_data = await page.evaluate('''() => {
        let sensors = [];
        // Find all elements with the class indicating sensor status
        document.querySelectorAll('[comp-id="2791"]').forEach(sensor => {
            let statusText = sensor.innerText;
            if (statusText.includes("Disconnected")) {
                sensors.push(statusText);
            }
        });
        return sensors;
    }''')

    # Close the browser
    await browser.close()

    # Check for disconnected sensors and send an email if any are found
    disconnected_sensors = []
    if sensor_data:
        for sensor in sensor_data:
            inactivity_info = sensor.split("No activity in")[-1].strip()
            disconnected_sensors.append(f"Disconnected, Inactivity Duration: {inactivity_info}")
        
        # If there are disconnected sensors, send an email alert
        send_email_alert(disconnected_sensors)
    else:
        print("All sensors are connected.")

def send_email_alert(disconnected_sensors):
    # Email server configuration
    sender = 'idk@gmail.com'
    recipient = 'brian@gmail.com'
    subject = "Disconnected Sensors Alert"
    body = "\n".join(disconnected_sensors)

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # Send email
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender, 'your_password')  # Enter your email password here
            server.sendmail(sender, [recipient], msg.as_string())
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Run the async function
asyncio.get_event_loop().run_until_complete(check_disconnected_sensors())
