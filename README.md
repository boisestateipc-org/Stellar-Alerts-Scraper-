# Stellar-Alerts-Scraper-
- @author Megan Aker
- December 19th, 2024

## Project Overview 
This is a scraper for Stellar Cyber API that correctly alerts sensor status. 

### How to run
Insure that Puppeteer is installed:
- pip3 install pyppeteer
- python3 stellar_scraper.py

### Notes on use:
- In scraper.py, replace the sender and receiver email address. The sender email will need to have 
2 step auth set up and an app password created. Replace this info in the commented section in the code.
- When the script is ran, a browser will pop up. Put in your Stellar Cyber log in credentials. Then, proceed 
to the nav bar where it says "systems" and go to the "sensors" page. From there, make sure all items are on 
the page using the filter at the bottom. 
- In the terminal, it will say press enter when you reach the sensors page. 
- A .html report will be generated and sent to whom ever the receiver is.  

### Future Improvements:
- One thing to consider could be setting up a ci/cd pipeline for this to run on a schedule. However, since 
you have to manually put in log info, this may be moot. (unless you import your credentials)
- Configure a way to tell if a disconnected sensor is "new". Many sensors are many days old so not new 
information. 

