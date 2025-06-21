import os
import requests
from bs4 import BeautifulSoup
from fredapi import Fred
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()

class BuffettIndicator:
    def __init__(self):
        self.fred_api_key = os.getenv('FRED_API_KEY')
        if self.fred_api_key:
            self.fred = Fred(api_key=self.fred_api_key)
        else:
            print("Warning: FRED API key is not set. Please set FRED_API_KEY in your .env file.")
            self.fred = None
            
    def get_wilshire_5000(self):
        """Scrape Wilshire 5000 index from Google Finance"""
        try:
            url = "https://www.google.com/finance/quote/FTW5000:INDEXNYSEGIS?hl=en"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            price_element = None
            
            price_element = soup.find('div', class_='YMlKec fxKbKc')
            
            if not price_element:
                parent_div = soup.find('div', {'jsname': 'ip75Cb', 'class': 'kf1m0'})
                if parent_div:
                    price_element = parent_div.find('div', class_='YMlKec fxKbKc')
            
            if not price_element:
                price_element = soup.find('div', class_='YMlKec')
            
            if price_element:
                price_text = price_element.text.strip().replace(',', '')
                print(f"Successfully scraped Wilshire 5000: {price_text}")
                return float(price_text)
            else:
                print("Warning: Wilshire 5000 index not found with any selector.")
                print("Available div elements with class containing 'YMlKec':")
                divs = soup.find_all('div', class_=lambda x: x and 'YMlKec' in x)
                for div in divs[:5]:
                    print(f"  - {div}")
                return None
                
        except Exception as e:
            print(f"Wilshire 5000 scraping error: {e}")
            return None
    
    def get_us_gdp(self):
        """Get US GDP data from FRED API"""
        try:
            if not self.fred:
                print("FRED API is not available.")
                return None
                
            gdp_series = self.fred.get_series('GDP', observation_start='2020-01-01')
            
            if not gdp_series.empty:
                latest_gdp = gdp_series.iloc[-1]
                return latest_gdp
            else:
                print("GDP data not found.")
                return None
                
        except Exception as e:
            print(f"Error getting GDP data: {e}")
            return None
    
    def calculate_buffett_indicator(self):
        """Calculate Buffett Indicator"""
        wilshire_index = self.get_wilshire_5000()
        gdp_billions = self.get_us_gdp()
        
        if wilshire_index is None or gdp_billions is None:
            print("Unable to retrieve necessary data.")
            return None
        
        # Wilshire 5000 index directly represents market cap in trillion dollars
        market_cap_trillions = wilshire_index / 1000
        gdp_trillions = gdp_billions / 1000
        buffett_ratio = (market_cap_trillions / gdp_trillions) * 100
        
        return {
            'buffett_ratio': round(buffett_ratio, 2),
            'wilshire_5000': wilshire_index,
            'market_cap_trillions': round(market_cap_trillions, 3),
            'gdp_trillions': round(gdp_trillions, 3),
            'gdp_billions': gdp_billions,
            'data_source': "Wilshire 5000 index + FRED GDP",
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def main():
    """Main execution function"""
    indicator = BuffettIndicator()
    result = indicator.calculate_buffett_indicator()
    
    if result:
        print(f"\n🔢 Current Buffett Indicator: {result['buffett_ratio']}%")
        print(f"\n📊 Detailed Information:")
        print(f"- Wilshire 5000 Index: {result['wilshire_5000']:,.2f}")
        print(f"- US Stock Market Value: ${result['market_cap_trillions']:,.3f} trillion")
        print(f"- US GDP: ${result['gdp_trillions']:,.3f} trillion (${result['gdp_billions']:,.2f} billion)")
        print(f"- Data Source: {result['data_source']}")
        print(f"- Measurement Time: {result['timestamp']}")
        
        print(f"\n💡 Calculation:")
        print(f"Buffett Indicator = (${result['market_cap_trillions']:,.3f}T ÷ ${result['gdp_trillions']:,.3f}T) × 100 = {result['buffett_ratio']}%")
        
        print("\n📈 Buffett Indicator Interpretation:")
        if result['buffett_ratio'] < 75:
            print("- 🟢 The stock market is significantly undervalued.")
        elif result['buffett_ratio'] < 90:
            print("- 🔵 The stock market is fairly valued.")
        elif result['buffett_ratio'] < 115:
            print("- 🟡 The stock market is somewhat overvalued.")
        elif result['buffett_ratio'] < 140:
            print("- 🟠 The stock market is significantly overvalued.")
        else:
            print("- 🔴 The stock market is extremely overvalued. Caution is advised.")
    else:
        print("❌ Unable to calculate Buffett Indicator.")

if __name__ == "__main__":
    main() 