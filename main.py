import os
import argparse
import subprocess

# Step 1: Dynamically set PROJECT_ROOT
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Step 2: Define commonly used paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
DRIVERS_DIR = os.path.join(PROJECT_ROOT, "drivers")
CHROMEDRIVER_PATH = os.path.join(DRIVERS_DIR, "chromedriver-mac-x64", "chromedriver")

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

# 3. Define your modular run_* functions
def run_ngdp2csv():
    """Run ngdp2csv.py script"""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "scrap_data", "ngdp2csv.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("ngdp2csv.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running ngdp2csv.py:")
        print(e.stderr)

def run_r_analysis():
    """Run R script for stepwise regression."""
    rscript_executable = "/usr/local/bin/Rscript"  
    r_script_path = "/Users/dohhyungjun/Documents/StockGraphPrediction/analysis.R"  # Update with your R script path
    try:
        result = subprocess.run(
            [rscript_executable, r_script_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("R script executed successfully.")
        print("Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the R script.")
        print("Error Output:\n", e.stderr)
    except FileNotFoundError:
        print(f"Rscript not found at {rscript_executable}. Please verify the path.")

def run_m_pmi2html():
    """Run m_pmi2html.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "scrap_data", "m_pmi2html.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("m_pmi2html.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running m_pmi2html.py:")
        print(e.stderr)

def run_s_pmi2html():
    """Run s_pmi2html.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "scrap_data", "s_pmi2html.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("s_pmi2html.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running s_pmi2html.py:")
        print(e.stderr)

def run_cpi2html():
    """Run cpi2html script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "scrap_data", "cpi2html.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("cpi2html.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running cpi2html.py:")
        print(e.stderr)

def run_fomc_IRD2html():
    """Run fomc_IRD2html script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "scrap_data", "fomc_IRD2html.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("fomc_IRD2html.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running fomc_IRD2html.py:")
        print(e.stderr)

def run_unrate2html():
    """Run unrate2html script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "scrap_data", "unrate2html.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("unrate2html.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running unrate2html.py:")
        print(e.stderr)

def run_leadingidx2html():
    """Run leadingidx2html script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "scrap_data", "leadingidx2html.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("leadingidx2html.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running leadingidx2html.py:")
        print(e.stderr)

def run_unemployment():
    """Run unemployment.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "unemployment.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("unemployment.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running unemployment.py:")
        print(e.stderr)

def run_sp500():
    """Run sp500.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "sp500.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("sp500.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running sp500.py:")
        print(e.stderr)

def run_cpi():
    """Run cpi.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "cpi.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("cpi executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running cpi.py:")
        print(e.stderr)

def run_nominal_gdp():
    """Run nominal_gdp script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "nominal_gdp.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("nominal_gdp executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running nominal_gdp.py:")
        print(e.stderr)

def run_m_pmi():
    """Run m_pmi.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "m_pmi.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("m_pmi.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running m_pmi.py:")
        print(e.stderr)

def run_s_pmi():
    """Run s_pmi.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "s_pmi.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("s_pmi.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running s_pmi.py:")
        print(e.stderr)

def run_federal_interest_rate():
    """Run federal_interest_rate.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "federal_interest_rate.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("federal_interest_rate.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running federal_interest_rate.py:")
        print(e.stderr)

def run_leading_index():
    """Run leading_index.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "leading_index.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("leading_index.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running leading_index.py:")
        print(e.stderr)

def run_closing_price():
    """Placeholder for refining stock data from tickers (closing_price.py)."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "closing_price.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("closing_price.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running closing_price.py:")
        print(e.stderr)

def run_sp500_tickers2txt():
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "scrap_data", "sp500_tickers2txt.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("sp500_tickers2txt executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running sp500_tickers2txt.py:")
        print(e.stderr)

# 4. Additional placeholders for new -stocks commands
def run_macro():
    """
    Placeholder for calling macros or other scripts
    that handle lists of stock data.
    """
    print("\n[INFO] Running macro data tasks...")
    # Example: you might call stock_data macros here
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "stock_data", "macro.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("macro.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running macro.py:")
        print(e.stderr)
    # Add any others as needed
    print("[INFO] Macro tasks completed.\n")

def run_format():
    """
    Placeholder for handling stock data by tickers.
    Potentially calls closing_price.py or your incremental download script.
    """
    print("\n[INFO] Running ticker data tasks (stock scraping/refining)...")
    # For example:
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "stock_data", "format.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("format.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running format.py:")
        print(e.stderr)
    # Add any others as needed
    print("[INFO] Format tasks completed.\n")


# 5: Main function
def main():
    parser = argparse.ArgumentParser(description="StockGraphPrediction Main Script")
    parser.add_argument(
        "-mode",
        type=str,
        required=False,
        choices=["scrap", "refine", "R", "plot"],
        help="Mode to run: scrap, refine, R, bond, or plot (optional)."
    )
    parser.add_argument(
        "-stocks",
        type=str,
        required=False,
        choices=["macro", "format"],
        help="Run stock-related commands: 'macro' or 'ticker'."
    )
    args = parser.parse_args()

    # If user specified -stocks, run that logic and skip -mode
    if args.stocks:
        if args.stocks == "macro":
            run_macro()
        elif args.stocks == "format":
            run_format()
        return  # End here to skip the mode-based logic

    # Otherwise, fall back to mode-based logic
    if args.mode == "scrap":
        print("Running data scrapping...")
        """
        run_ngdp2csv()
        run_m_pmi2html()
        run_s_pmi2html()
        run_cpi2html()
        run_fomc_IRD2html()
        run_unrate2html()
        run_leadingidx2html()
        """
        run_sp500_tickers2txt()

    elif args.mode == "refine":
        print("Running data refining...")
        run_unemployment()
        run_m_pmi()
        run_s_pmi()
        run_sp500()
        run_cpi()
        run_nominal_gdp()
        run_leading_index()
        run_federal_interest_rate()
        # run_closing_price()  # Uncomment if you want to refine stock data in this mode

    elif args.mode == "R":
        print("Running R analysis...")
        run_r_analysis()        

    elif args.mode == "plot":
        print("Running plot")
        # Placeholder for plotting

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
