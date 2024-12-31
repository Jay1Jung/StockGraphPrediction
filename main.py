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

# Step 3: Define functions for modular tasks
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
    """Run the R script for stepwise regression."""
    R_SCRIPT_PATH = os.path.join(PROJECT_ROOT, "analysis", "R", "stepwise_regression.R")
    try:
        result = subprocess.run(
            ["Rscript", R_SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("R analysis completed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during R analysis:")
        print(e.stderr)

def run_m_pmi2html():
    """Run the m_pmi2html.py script."""
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
    """Run the s_pmi2html.py script."""
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
    """Run cpi2csv script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "scrap_data", "cpi2csv.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("cpi2csv.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running cpi2csv.py:")
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
    """Run the unemployment.py script."""
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
    """Run the sp500.py script."""
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

def run_pmi2csv():
    """Run pmi2csv.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "pmi2csv.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("gdp_cpi2csv.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running pmi2csv.py:")
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
    """Run leading_index2.py script."""
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

# Step 4: Main function
def main():
    parser = argparse.ArgumentParser(description="StockGraphPrediction Main Script")
    parser.add_argument(
        "-mode",
        type=str,
        required=True,
        choices=["scrap", "refine", "R", "bond", "plot"],
        help="Mode to run: scarp, refine, R, bond, or plot"
    )
    args = parser.parse_args()

    # Route to the correct functionality
    if args.mode == "scrap":
        print("Running data scrapping...")
        run_ngdp2csv() # Call ngdp2csv.py
        run_m_pmi2html()  # Call m_pmi2html.py
        run_s_pmi2html()  # Call s_pmi2html.py
        run_cpi2html()  # Call cpi2html.py
        run_fomc_IRD2html()  # Call fomc_IRD2html.py
        run_unrate2html()  # Call unrate2html.py
        run_leadingidx2html()  #Call leadingidx2html.py
    elif args.mode == "refine":
        print("Running data refining...")
        run_unemployment()  # Call unemployment.py
        run_m_pmi()
        run_s_pmi()
        run_sp500()  # Call sp500.py
        run_cpi()  # Call cpi.py
        run_nominal_gdp()  # Call gdp2csv.py 
        run_leading_index()  # Call leading_index.py
        run_federal_interest_rate()  # Call federal_interest_rate.py
        # *closing_price from stock extracted by ticker *                
        # run_closing_price()  # Call closing_price.py * not resolved ** Should be moved to refine
    elif args.mode == "R":
        print("Running R analysis...")
        run_r_analysis()
    elif args.mode == "bond":
        print("Running bond analysis...")
        # Placeholder for bond analysis functionality
    elif args.mode == "plot":
        print("Running plot")
    else:
        print("Invalid mode. Use -h for help.")

if __name__ == "__main__":
    main()
