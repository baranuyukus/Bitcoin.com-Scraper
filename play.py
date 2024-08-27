from playwright.sync_api import sync_playwright
import time

def fetch_article_details(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  
        page = browser.new_page()

        
        page.goto(url)

        # Yüklenmesini bekliyoruz. Olmadığı zaman sıkıntı çıkabiliyor.
        time.sleep(5)

        try:
            # Title'ı çıkartmaya çalışıyoruz.
            title = page.inner_text("h1.sc-jkrwJj")
            print("Title:", title)

            # Makaleyi çıkartıyoruz buradan
            article_content = page.inner_text("div.article__body")
            print("Article Content:", article_content)

        except Exception as e:
            print("Failed to load the article content:", e)
        
        # kapat
        browser.close()


url = "https://news.bitcoin.com/latam-insights-encore-el-salvadors-bitcoin-education-investments-set-to-pay-off-in-adoption/"
fetch_article_details(url)
