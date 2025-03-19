import requests
from bs4 import BeautifulSoup
import random


def duckduckgo_search(query):
    
    possibleHeaders = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/86.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/89.0.774.54",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/74.0.3911.75",

    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36",

    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/86.0",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Mobile/15E148 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 12_4 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Mobile/15E148 Safari/537.36",

    "Mozilla/5.0 (iPad; CPU OS 14_3 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 13_5 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/537.36",

    "Mozilla/5.0 (Linux; Android 9; Samsung Galaxy Tab S4 Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.101 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; Lenovo Tab 4 10 Plus Build/OPR1.170623.023) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",

    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; rv:28.0) Gecko/20100101 Firefox/28.0",
    ]
    
    
    url = f"https://html.duckduckgo.com/html/?q={query}"  

    response = requests.get(url, headers={"User-Agent":random.choice(possibleHeaders)})
    respCode = response.status_code
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    results2 = []

    if response.status_code != 200:
        print(f"Error {response.status_code}: DuckDuckGo blocked the request.")
        return results
        
    else: 
        soup = BeautifulSoup(response.text, "html.parser")

        # Iterate through all the result titles and their corresponding details
        for result in soup.select(".result__title"):
            title = result.text.strip()
            link = result.a["href"]

            # Extract the real destination URL from the 'uddg' query parameter in DuckDuckGo
            if link.startswith('//'):
                link = 'https:' + link
            elif link.startswith('/l/?uddg='):
                link = link.split('uddg=')[1]
                link = urlparse(link).path  # Strip DuckDuckGo, get real
            
            logo = result.find_parent().select_one(".result__icon img")
            image = logo["src"] if logo else None
            
            if image and image.startswith("//"):
                image = "https:" + image 



            snippet = result.find_parent().select_one(".result__snippet")
            snippet_text = snippet.text.strip() if snippet else None  # Safely get the snippet text

            results.append((title, link, image, snippet_text))


        
        return results


('Discord in Early Talks With Bankers for Potential I.P.O.', 'https://www.nytimes.com/2025/03/05/technology/discord-ipo.html', 'https://external-content.duckduckgo.com/ip3/www.nytimes.com.ico', 'Discord was founded by Jason Citron and Stanislav Vishnevskiy, two tech workers who originally came together to build a video games studio. After releasing their first title, the two hit upon the ...')