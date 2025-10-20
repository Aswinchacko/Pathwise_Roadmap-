#!/usr/bin/env python3
"""Simple test to verify Chrome driver works and can scrape LinkedIn via Google"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_chrome():
    print("[TEST] Starting Chrome driver test...")
    
    chrome_options = Options()
    # NOT headless for debugging
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("[OK] Chrome driver initialized")
        
        # Test Google search for LinkedIn profiles
        search_query = "Full Stack Developer site:linkedin.com/in"
        url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        
        print(f"[TEST] Navigating to: {url}")
        driver.get(url)
        time.sleep(3)  # Wait for page load
        
        print(f"[TEST] Current URL: {driver.current_url}")
        print(f"[TEST] Page title: {driver.title}")
        
        # Try to find search results
        try:
            results = driver.find_elements(By.CSS_SELECTOR, "div.g")
            print(f"[FOUND] {len(results)} search results")
            
            # Extract LinkedIn URLs
            linkedin_urls = []
            for result in results[:5]:
                try:
                    link = result.find_element(By.CSS_SELECTOR, "a")
                    href = link.get_attribute("href")
                    if "linkedin.com/in/" in href:
                        linkedin_urls.append(href)
                        print(f"[FOUND] LinkedIn URL: {href}")
                except:
                    pass
            
            if linkedin_urls:
                print(f"[SUCCESS] Found {len(linkedin_urls)} LinkedIn profiles!")
            else:
                print("[WARNING] No LinkedIn URLs found in results")
                print("[INFO] Page source preview:")
                print(driver.page_source[:500])
                
        except Exception as e:
            print(f"[ERROR] Could not find search results: {e}")
        
        input("\nPress Enter to close browser...")
        driver.quit()
        print("[OK] Test complete")
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chrome()


