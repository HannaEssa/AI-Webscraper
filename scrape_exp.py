# Importing necessary libraries
from selenium.webdriver import Remote, ChromeOptions  # Selenium for browser automation to scrape dynamic content
from selenium.webdriver.chromium.remote_connection import \
    ChromiumRemoteConnection  # For connecting to remote browsers (headless)
from bs4 import BeautifulSoup  # BeautifulSoup for parsing HTML and extracting content

# Authentication details for connecting to a remote Selenium WebDriver instance via a proxy
AUTH = 'brd-customer-hl_582c81f9-zone-ai_scraper:p9jrgzdg9whi'  # Authentication string (replace with actual credentials)
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'  # Remote WebDriver URL using proxy credentials


# Function to scrape the content of a website
def scrape_website(website):
    print("Launching chrome browser...")

    # Establish a remote connection to the browser using the proxy WebDriver URL
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

    # Start the remote browser session
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)  # Open the website in the browser
        print('Taking page screenshot to file page.png')  # Take a screenshot of the webpage
        driver.get_screenshot_as_file('./page.png')  # Save the screenshot locally
        print('Navigated! Scraping page content...')
        html = driver.page_source  # Retrieve the page’s raw HTML content
        return html  # Return the HTML content of the page


# Function to extract the body content from the raw HTML
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")  # Parse the HTML using BeautifulSoup
    body_content = soup.body  # Extract the <body> element, which contains the main content
    if body_content:
        return str(body_content)  # Return the body content as a string
    return ""  # If no body content exists, return an empty string


# Function to clean the body content (removes <script>, <style>, and whitespace)
def cleaned_body_content(body_content):
    soup = BeautifulSoup(body_content)  # Parse the body content

    # Remove unwanted tags (scripts and styles)
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get the text content and strip unnecessary whitespace
    cleaned_content = soup.get_text(separator="\n")  # Separate text blocks with newlines
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip())  # Remove empty lines and extra spaces
    return cleaned_content  # Return the cleaned text content


# Function to split the DOM content into smaller chunks (max length of 6000 characters)
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]  # Break the DOM content into chunks, each with a maximum length of `max_length`
