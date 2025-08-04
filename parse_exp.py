# Importing required classes from LangChain
from langchain_ollama import OllamaLLM  # To use the Ollama language model for AI-powered parsing
from langchain_core.prompts import ChatPromptTemplate  # Helps in creating structured prompts for language models

# Define a prompt template. This will guide the AI model on how to extract data from the provided content.
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

# Initialize the Ollama model (in this case, Llama 3.2)
model = OllamaLLM(model="llama3.2")


# Function to parse content using the Ollama model. This function receives chunks of content and a description.
def parse_with_ollama(dom_chunks, parse_description):
    # Use the ChatPromptTemplate to format the prompt by injecting the DOM content and description.
    prompt = ChatPromptTemplate.from_template(template)

    # Chain the prompt with the model to make the model respond to the structured prompt.
    chain = prompt | model

    # List to store the parsed results for each chunk.
    parsed_results = []

    # Loop through each chunk of DOM content to parse it individually.
    for i, chunk in enumerate(dom_chunks, start=1):
        # Invoke the AI model with the current chunk of content and the parsing description.
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        # Print a message to show progress in the terminal (not shown in the UI).
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        # Append the parsed result to the list.
        parsed_results.append(response)

    # Return the parsed results as a single string (concatenating all chunks).
    return "\n".join(parsed_results)
