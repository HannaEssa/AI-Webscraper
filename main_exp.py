# Importing required libraries
import streamlit as st  # Streamlit is used to create interactive web applications for Python.
from scrape import scrape_website, split_dom_content, cleaned_body_content, \
    extract_body_content  # Custom functions for scraping and content processing
from parse import parse_with_ollama  # Function that interfaces with the Ollama AI model to parse content

# Streamlit title for the web app
st.title("AI Web Scraper")

# User input for the website URL. Streamlit's `text_input` creates a text box on the UI for the user to input a URL.
url = st.text_input("Enter a Website URL:")

# Button that triggers the web scraping process when clicked.
if st.button("Scraping Site"):
    # Display a message on the UI indicating that the site is being scraped.
    st.write("Scraping the Website")

    # Call the scrape_website function to scrape the content of the given URL.
    result = scrape_website(url)  # The raw HTML of the website is returned by this function.

    # Call `extract_body_content` to isolate the body content from the raw HTML.
    body_content = extract_body_content(result)

    # Clean the extracted body content by removing non-essential tags like scripts and styles.
    cleaned_content = cleaned_body_content(body_content)

    # Save the cleaned body content in session_state to use it later in the app (e.g., for parsing).
    st.session_state.dom_content = cleaned_content

    # Use Streamlit's expander to allow the user to view the DOM content. The content is displayed in a text area.
    with st.expander("View DOM content"):
        st.text_area("DOM Content", cleaned_content, height=300)

# After scraping, allow the user to specify what content they want to parse (e.g., "extract all headlines").
# Check if `dom_content` is stored in the session state (indicating the scraping process has been completed).
if "dom_content" in st.session_state:
    # Text area where the user can describe what they want to extract from the scraped DOM content.
    parse_description = st.text_area("Describe what you want to parse?")

    # Button that triggers the parsing process when clicked.
    if st.button("Parse Content"):
        if parse_description:  # Ensure the user provided a description to guide the AI model
            # Show a message that parsing is starting
            st.write("Parsing the content")

            # Split the cleaned content into smaller chunks to avoid hitting the input length limit of the AI model.
            dom_chunks = split_dom_content(st.session_state.dom_content)

            # Call the `parse_with_ollama` function to process each chunk of content using the AI model.
            result = parse_with_ollama(dom_chunks, parse_description)

            # Display the result of the parsing on the app
            st.write(result)
