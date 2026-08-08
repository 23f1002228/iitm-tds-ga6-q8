import sys
import re
from playwright.sync_api import sync_playwright

def scrape():
    seeds = range(14, 24)  # seeds 14 through 23
    total_sum = 0.0
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for seed in seeds:
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            print(f"Navigating to {url}...")
            
            # Visit the page and wait for network to be idle
            page.goto(url, wait_until="networkidle")
            
            # Wait for the table to appear
            page.wait_for_selector("table")
            
            # Extract all td elements
            cells = page.query_selector_all("td")
            seed_sum = 0.0
            cell_contents = []
            
            for cell in cells:
                text = cell.text_content().strip()
                cell_contents.append(text)
                
                # Extract numeric values including negative numbers and decimals
                # Match patterns like -123.45, 123.45, -123, 123, -0.45, .45, etc.
                matches = re.findall(r'-?\d+\.?\d*|-?\.\d+', text)
                for match in matches:
                    try:
                        val = float(match)
                        seed_sum += val
                    except ValueError:
                        pass
            
            print(f"Seed {seed}: Found {len(cells)} td elements. Sum for this seed: {seed_sum}")
            # If the output is small, we can print a few cell examples for debugging
            if len(cell_contents) > 0:
                print(f"Sample cells: {cell_contents[:5]}")
            total_sum += seed_sum
            
        browser.close()
        
    final_total = int(round(total_sum))
    print(f"TOTAL_SUM={final_total}")
    
    expected_total = 2484661
    assert final_total == expected_total, f"Assertion failed: calculated total is {final_total}, expected {expected_total}"
    print("Scraping completed successfully. Assertion passed.")

if __name__ == "__main__":
    scrape()
