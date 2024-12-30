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
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "fetch_data", "m_pmi2html.py")
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
    SCRIPT_PATH = os.path.join(PROJECT_ROOT, "scripts", "fetch_data", "s_pmi2html.py")
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

# Step 4: Main function
def main():
    parser = argparse.ArgumentParser(description="StockGraphPrediction Main Script")
    parser.add_argument(
        "-mode",
        type=str,
        required=True,
        choices=["dataprocess", "R", "bond"],
        help="Mode to run: dataprocess, R, or bond"
    )
    args = parser.parse_args()

    # Route to the correct functionality
    if args.mode == "dataprocess":
        print("Running data processing...")
        run_m_pmi2html()  # Call the m_pmi2html function
        run_s_pmi2html()  # Call the s_pmi2html function
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
