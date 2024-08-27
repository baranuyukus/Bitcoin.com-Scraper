import openai
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

# Set up your OpenAI API key
openai.api_key = "apikey"

def fetch_article_details(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to the provided URL
        page.goto(url)

        # Wait for 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', or 'p' tags to be present in the DOM
        page.wait_for_selector("h1, h2, h3, h4, h5, h6, p")

        # Extract the body content as soon as the important tags are loaded
        body_content = page.content()

        # Close the browser
        browser.close()

        return body_content

def extract_text_from_html(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')

    text_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])
    extracted_text = "\n".join([element.get_text(strip=True) for element in text_elements])

    return extracted_text

def split_text_by_token_limit(text, max_tokens=1600):
    words = text.split()  #
    current_chunk = []
    chunks = []
    current_length = 0
    
    for word in words:
        current_chunk.append(word)
        current_length += 1  
        
        if current_length >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
    
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def extract_article_via_openai(extracted_text):
    client = openai.OpenAI(api_key=openai.api_key)
    
    
    content_chunks = split_text_by_token_limit(extracted_text, max_tokens=1500)  
    results = []
    
    for chunk in content_chunks:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts titles and articles from HTML content."},
                {"role": "user", "content": f"Extract the title and the main article content from the following text:\n\n{chunk}\n\nReturn in the format 'Title: [title] Article: [main article content]'."}
            ]
        )
        results.append(response.choices[0].message.content.strip())
        time.sleep(1)  # Adding a slight delay to avoid rate limits

    return "\n\n".join(results)



def main(url):
    body_content = fetch_article_details(url)
    extracted_text = extract_text_from_html(body_content)
    article_details = extract_article_via_openai(extracted_text)
    
    print("Orijinal Makale:")
    print("--------------------")
    print(article_details)
    print("--------------------")
    
    
# Example usage
if __name__ == "__main__":
    url = input("ICERIK URL: ")
    main(url)