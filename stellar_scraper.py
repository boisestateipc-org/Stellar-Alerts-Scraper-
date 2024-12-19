import asyncio
import smtplib
from pyppeteer import launch
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

async def scrape_disconnected_sensors():
    browser = await launch(
        headless=False,
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )
    page = await browser.newPage()

    try:
        await page.setViewport({'width': 2100, 'height': 1000})

        # Load Stellar Cyber Login Page
        await page.goto("https://cyberdome.us/login", waitUntil='networkidle2', timeout=60000)
        print("Please log in and navigate to the sensors page. Press Enter here when ready...")
        input()  # Wait for user to log in and navigate manually

        # Scrape all rows with disconnected sensors (marked with `.danger` class)
        disconnected_sensors = await page.evaluate('''() => {
            const sensors = [];
            const dangerIcons = document.querySelectorAll('mat-icon.danger');
            
            dangerIcons.forEach(icon => {
                const row = icon.closest('[role="row"]');  // Locate the parent row of the danger icon
                if (row) {
                    const gridCells = row.querySelectorAll('[role="gridcell"]');  // Extract gridcell data
                    const hostname = gridCells[0]?.innerText || "Unknown";  // First column
                    const status = gridCells[1]?.innerText || "Unknown";  // Second column
                    const time = gridCells[2]?.innerText || "Unknown";  // Third column
                    sensors.push({ hostname, status, time });
                }
            });
            return sensors;
        }''')

        # Generate HTML Report
        html_content = '''
        <html>
        <head>
            <title>Disconnected Sensors Report</title>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .danger {{
                    color: red;
                }}
            </style>
        </head>
        <body>
            <h1>Disconnected Sensors</h1>
            <table>
                <tr>
                    <th>Hostname</th>
                    <th>Status</th>
                    <th>Time</th>
                </tr>
        '''
        for sensor in disconnected_sensors:
            html_content += f'''
                <tr>
                    <td>{sensor["hostname"]}</td>
                    <td class="danger">{sensor["status"]}</td>
                    <td>{sensor["time"]}</td>
                </tr>
            '''
        html_content += '''
            </table>
        </body>
        </html>
        '''

        # Save the report as an HTML file
        report_filename = "disconnected_sensors_report.html"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"Disconnected Sensors Report generated: {report_filename}")

        # Send the report via email
        send_email_report(report_filename)

    except Exception as e:
        await page.screenshot({'path': 'error_screenshot.png'})  # Save a screenshot for debugging
        print(f"An error occurred: {e}")
    finally:
        await browser.close()

def send_email_report(report_file):
    # Email settings
    sender_email = "meganaker10@gmail.com"  #Replace with sender email 
    receiver_email = "cadenwilson605@gmail.com"  #Replace with receiver email 
    password = "rmns fvho buyy etdo"  #Replace with senders password, or import it from a password manager for more security

    # Email content
    subject = "Disconnected Sensors Report"
    body = "Attached is the Disconnected Sensors Report."

    # Set up the email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach the body text
    message.attach(MIMEText(body, 'plain'))

    # Attach the report file
    attachment = open(report_file, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(report_file)}")
    message.attach(part)
    attachment.close()

    try:
        # Send the email
        print("Sending email...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(scrape_disconnected_sensors())
