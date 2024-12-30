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

def run_html2csv():
    """Run the html2csv.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "html2csv.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("html2csv.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running html2csv.py:")
        print(e.stderr)

def run_snp2csv():
    """Run the snp2csv.py script."""
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "refine_data", "snp2csv.py")
    try:
        result = subprocess.run(
            ["python3", SCRIPT_PATH],
            capture_output=True,
            text=True,
            check=True
        )
        print("snp2csv.py executed successfully:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error running snp2csv.py:")
        print(e.stderr)

# Step 4: Main function
def main():
    parser = argparse.ArgumentParser(description="StockGraphPrediction Main Script")
    parser.add_argument(
        "-mode",
        type=str,
        required=True,
        choices=["scrap", "refine", "R", "bond"],
        help="Mode to run: scarp, refine, R, or bond"
    )
    args = parser.parse_args()

    # Route to the correct functionality
    if args.mode == "scrap":
        print("Running data scrapping...")
        run_m_pmi2html()  # Call m_pmi2html.py
        run_s_pmi2html()  # Call s_pmi2html.py
    elif args.mode == "refine":
        print("Running data refining...")
        # run_unemployment()  # Call unemployment.py
        # run_html2csv()  # Call html2csv.py
        run_snp2csv()  # Call snp2csv.py
    elif args.mode == "R":
        print("Running R analysis...")
        run_r_analysis()
    elif args.mode == "bond":
        print("Running bond analysis...")
        # Placeholder for bond analysis functionality
    else:
        print("Invalid mode. Use -h for help.")

if __name__ == "__main__":
    main()
