import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define sector symbols and corresponding tickers
sectors = {
    "Technology": ["MSFT", "AAPL", "NVDA", "TSM", "AVGO", "ADI", "AMAT", "AMD", "CSCO", "CRM", "GFS", "INTC", "LRCX", "MCHP", "MRVL", "MU", "NXPI", "ORCL", "QCOM", "SNPS", "TER", "TXN", "VMW", "WDC", "ZBRA", "KLAC", "CDNS", "ANSS", "AKAM", "FTNT"],
    "Financial Services": ["BRK-A", "JPM", "MA", "BAC", "WFC", "C", "GS", "MS", "SCHW", "AXP", "BK", "BLK", "TROW", "STT", "PNC", "USB", "CME", "ICE", "MMC", "AON", "MET", "PRU", "AFL", "LNC", "CINF", "ALL", "PGR", "TRV", "CB", "HIG"],
    "Communication Services": ["GOOGL", "GOOG", "NFLX", "TMUS", "DIS", "CMCSA", "CHTR", "T", "VZ", "FOXA", "FOX", "IRDM", "SIRI", "AMX", "TKC", "TU", "BCE", "TEF", "ORAN", "DTEGY", "CHL", "CHT", "SKM", "KT", "LUMN", "LILA", "LILAK", "CCOI", "SJR", "WBD"],
    "Healthcare": ["LLY", "NVO", "UNH", "JNJ", "MRK", "PFE", "ABBV", "ABT", "TMO", "MDT", "BMY", "AMGN", "GILD", "DHR", "ISRG", "REGN", "BIIB", "MRNA", "DXCM", "IDXX", "SYK", "EW", "BSX", "ZBH", "CNC", "RMD", "STE", "MASI", "ALGN", "HOLX"],
    "Consumer Cyclical": ["AMZN", "TSLA", "HD", "TM", "MCD", "NKE", "SBUX", "LOW", "TGT", "TJX", "EBAY", "ROST", "MAR", "YUM", "DG", "CMG", "ULTA", "AZO", "BBY", "DHI", "LEN", "PZZA", "W", "RH", "TPX", "DKNG", "LVS", "WYNN", "BKNG", "ORLY"],
    "Industrials": ["CAT", "GE", "UNP", "RTX", "ETN", "HON", "UPS", "BA", "MMM", "DE", "LMT", "NSC", "CSX", "DAL", "AAL", "UAL", "LUV", "EXPD", "CHRW", "R", "JBHT", "KNX", "WERN", "ODFL", "HUBG", "SNDR", "MRTN", "HTLD", "ITW", "GD"],
    "Consumer Defensive": ["WMT", "PG", "COST", "KO", "PEP", "PM", "MO", "KHC", "MDLZ", "STZ", "KDP", "GIS", "CL", "CPB", "HSY", "K", "TSN", "SJM", "MKC", "CHD", "LW", "HRL", "CAG", "FDP", "HAIN", "THS", "SPTN", "BGS", "FARM", "FLO"],
    "Energy": ["XOM", "CVX", "PTR", "TTE", "COP", "SLB", "OXY", "PSX", "EOG", "MPC", "HAL", "MRO", "DVN", "PXD", "CLR", "EPD", "WMB", "KMI", "TRGP", "MMP", "OKE", "ET", "LNG", "ENLC", "CEQP", "DCP", "HESM", "ENBL", "BSM", "AM"],
    "Basic Materials": ["LIN", "BHP", "RIO", "SCCO", "SHW", "APD", "NEM", "DD", "DOW", "PPG", "ECL", "FMC", "ALB", "CE", "EMN", "AVNT", "AXTA", "ASH", "NEU", "GCP", "KRA", "NGVT", "IOSP", "OLN", "WLK", "HUN", "CC", "VNTR", "CBT", "TROX"],
    "Real Estate": ["PLD", "AMT", "EQIX", "WELL", "SPG", "PSA", "DLR", "VTR", "AVB", "ESS", "EQR", "UDR", "MAA", "SUI", "CPT", "HST", "PEAK", "AIRC", "ARE", "BXP", "SLG", "FRT", "REG", "KIM", "BRX", "ROIC", "MAC", "TCO", "WRI", "AKR"],
    "Utilities": ["NEE", "DUK", "SO", "EXC", "AEP", "XEL", "ES", "PEG", "EIX", "D", "WEC", "PCG", "SRE", "ED", "FE", "PPL", "AEE", "CMS", "DTE", "LNT", "NI", "AWK", "CNP", "NRG", "ETR", "PNW", "VST", "OGE", "POM", "IDA"]
}

# Define the start and end dates
start_date = "2019-01-01"
end_date = "2024-06-30"

# Function to normalize prices
def normalize_prices(df):
    return df / df.iloc[0]

# Function to fetch data, normalize, and calculate mean for each sector
def get_sector_data(sectors, start_date, end_date):
    sector_data = {}
    for sector, symbols in sectors.items():
        df_list = []
        for symbol in symbols:
            ticker = yf.Ticker(symbol)
            df = ticker.history(start=start_date, end=end_date, interval="1d")["Volume"]
            df.name = symbol
            df_list.append(df)
        sector_df = pd.concat(df_list, axis=1)
        sector_df = normalize_prices(sector_df)
        sector_data[sector] = sector_df.mean(axis=1)
    return pd.DataFrame(sector_data)

# Fetch S&P 500 data and normalize
spy = yf.Ticker("SPY").history(start=start_date, end=end_date, interval="1d")["Volume"]
spy = normalize_prices(spy)

# Create subplots for each year
fig, axs = plt.subplots(3, 2, figsize=(20, 15))
axs = axs.flatten()
years = range(2019, 2025)
for i, year in enumerate(years):
    if year == 2024:
        year_start = f"{year}-01-01"
        year_end = "2024-06-30"
    else:
        year_start = f"{year}-01-01"
        year_end = f"{year}-12-31"
    
    sector_data = get_sector_data(sectors, year_start, year_end)
    sector_data["S&P 500"] = spy.loc[year_start:year_end]

    for column in sector_data.columns:
        axs[i].plot(sector_data.index, sector_data[column], label=column)
    axs[i].set_title(f"Normalized Trading Volumes of Sectors and S&P 500 ({year})")
    axs[i].set_xlabel("Date")
    axs[i].set_ylabel("Normalized Trading Volume")
    axs[i].legend()

plt.tight_layout()
plt.savefig("sector_volumes_2019_2024.png")
plt.show()
