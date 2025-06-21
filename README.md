# Buffett Indicator Calculator

A Python tool to calculate the Buffett Indicator (Market Cap to GDP ratio), which Warren Buffett described as "probably the best single measure of where valuations stand at any given moment."

## What is the Buffett Indicator?

The Buffett Indicator compares the total market capitalization of publicly traded stocks to the country's Gross Domestic Product (GDP):

**Buffett Indicator = (Total Market Cap / GDP) × 100**

This metric helps assess whether the stock market is overvalued or undervalued relative to the underlying economy.

## Features

- Real-time calculation using live data sources
- Scrapes Wilshire 5000 index from Google Finance
- Fetches latest US GDP data from FRED API
- Automatic conversion of Wilshire 5000 index to market capitalization
- Market valuation interpretation with visual indicators
- Clean, emoji-enhanced output with detailed calculations

## How It Works

1. **Market Cap**: Wilshire 5000 index directly represents market cap in trillion dollars
   - Example: Index 59,614.18 = $59.614 trillion market cap
2. **GDP**: Latest quarterly GDP data from FRED (in billions, converted to trillions)
3. **Calculation**: (Market Cap ÷ GDP) × 100

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Buffett-indicator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up FRED API key:
   - Get free API key from [FRED](https://fred.stlouisfed.org/docs/api/api_key.html)
   - Create `.env` file: `FRED_API_KEY=your_api_key_here`

## Usage

### Basic Usage
```bash
python buffett_indicator.py
```

### Sample Output
```
🔢 Current Buffett Indicator: 198.87%

📊 Detailed Information:
- Wilshire 5000 Index: 59,614.18
- US Stock Market Value: $59.614 trillion
- US GDP: $29.977 trillion ($29,976.64 billion)
- Data Source: Wilshire 5000 index + FRED GDP
- Measurement Time: 2025-06-21 22:12:51

💡 Calculation:
Buffett Indicator = ($59.614T ÷ $29.977T) × 100 = 198.87%

📈 Buffett Indicator Interpretation:
- 🔴 The stock market is extremely overvalued. Caution is advised.
```

### Using as Module
```python
from buffett_indicator import BuffettIndicator

indicator = BuffettIndicator()
result = indicator.calculate_buffett_indicator()

if result:
    print(f"Buffett Indicator: {result['buffett_ratio']}%")
    print(f"Market Cap: ${result['market_cap_trillions']:.3f} trillion")
    print(f"GDP: ${result['gdp_trillions']:.3f} trillion")
```

## Interpretation Guide

| Range | Indicator | Market Status |
|-------|-----------|---------------|
| < 75% | 🟢 | Significantly Undervalued |
| 75-90% | 🔵 | Fairly Valued |
| 90-115% | 🟡 | Somewhat Overvalued |
| 115-140% | 🟠 | Significantly Overvalued |
| > 140% | 🔴 | Extremely Overvalued |

## Data Sources

- **Market Capitalization**: Google Finance Wilshire 5000 index
  - Represents total US stock market value
  - Index value directly converts to trillions of dollars
- **GDP**: FRED US Nominal GDP (quarterly, annualized)
  - Series ID: GDP
  - Unit: Billions of dollars

## Technical Details

### Web Scraping
- Multiple CSS selectors for robust data extraction
- Handles Google Finance page structure changes
- 10-second timeout with comprehensive error handling

### Data Processing
- Wilshire 5000 index ÷ 1000 = Market cap in trillions
- GDP billions ÷ 1000 = GDP in trillions
- Consistent trillion-dollar units for calculation

## Requirements

```
requests
beautifulsoup4
fredapi
python-dotenv
```

## Error Handling

The tool gracefully handles:
- Network connectivity issues
- FRED API unavailability
- Google Finance page structure changes
- Missing or invalid data

## Limitations

- Web scraping dependent on Google Finance page structure
- FRED API key required for GDP data
- Quarterly GDP updates (not real-time)
- US market focus only

## Historical Context

- **Normal Range**: 50-90%
- **Dot-com Bubble (2000)**: ~140%
- **2008 Financial Crisis**: ~60%
- **Current Levels**: Often above 150-200%

## Contributing

Pull requests welcome! Areas for improvement:
- Additional market indices
- Historical data analysis
- International markets
- Data visualization

## License

MIT License

## Disclaimer

**Educational purposes only.** Not financial advice. Consult qualified financial advisors for investment decisions.

## References

- [Warren Buffett Fortune Article (2001)](https://fortune.com/2001/12/10/warren-buffett-on-the-stock-market/)
- [FRED Economic Data](https://fred.stlouisfed.org/)
- [Wilshire 5000 Index](https://wilshire.com/indexes/wilshire-5000)
- [Google Finance](https://www.google.com/finance/) 