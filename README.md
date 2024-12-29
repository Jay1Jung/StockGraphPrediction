# StockGraphPrediction
StockGraphPrediction/
│
├── data/                         # Raw and processed data files
│   ├── raw/                      # Raw data files (original downloads)
│   │   ├── sp500_data.csv
│   │   ├── manufacturing_pmi.html
│   │   └── services_pmi.html
│   │
│   ├── processed/                # Processed data for analysis
│       ├── sp500_cleaned.csv
│       ├── manufacturing_pmi.csv
│       └── services_pmi.csv
│
├── notebooks/                    # Jupyter notebooks for exploratory analysis
│   ├── data_exploration.ipynb
│   ├── data_visualization.ipynb
│   └── prediction_model.ipynb
│
├── scripts/                      # Python scripts for automation
│   ├── fetch_data/
│   │   ├── fetch_sp500.py        # Fetch S&P 500 data from Yahoo Finance
│   │   ├── fetch_pmi_data.py     # Extract PMI data from HTML
│   │   └── setup_chromedriver.py # Check/setup ChromeDriver
│   │
│   ├── preprocess_data/
│   │   ├── clean_sp500.py        # Clean and normalize S&P 500 data
│   │   └── clean_pmi.py          # Clean PMI data
│   │
│   ├── visualize_data.py         # Generate comparative plots
│   ├── train_model.py            # Train prediction models
│   └── evaluate_model.py         # Evaluate prediction performance
│
├── tests/                        # Unit and integration tests
│   ├── test_fetch_sp500.py
│   ├── test_fetch_pmi_data.py
│   └── test_preprocess_data.py
│
├── README.md                     # Project overview and instructions
├── requirements.txt              # List of required Python libraries
├── .gitignore                    # Ignore unnecessary files (e.g., .env, data files)
├── LICENSE                       # License for the repository
└── main.py                       # Main entry point for running the project

S&P 500 stocks are categorized into 9 major sectors (e.g., technology, healthcare, energy, etc.), which help visualize sector-specific trends and future trajectories from a broader perspective.

These 9 sectors have identifiable relationships with key U.S. economic indicators, such as:
Key U.S. Economic Indicators (Combined Sources):
신규 실업수당청구건수 (New Jobless Claims)
S&P 글로벌 제조업 PMI*
S&P 글로벌 서비스업 PMI*
S&P 글로벌 합성 PMI
연준 기준금리 결정* FRED - Federal Funds Rate
실질 GDP 성장률* World Bank - GDP Growth
근원 PCE 가격지수
EIA 원유재고
신규주택판매
컨퍼런스보드 소비자신뢰지수
미국 국채경매
기존주택판매
실업률* World Bank - Unemployment Rate
CPI 상승률* World Bank - CPI
PPI 상승률
경기선행지수* FRED - Leading Index

Objective:

Develop regression models to understand how these economic indicators are correlated with sector-wise stock movements.
Predict how upcoming economic announcements (e.g., CPI or interest rate changes) will affect the prices within each sector.
Challenges:

Stock price movements are influenced by unpredictable factors beyond economic indicators.
It’s crucial to determine:
How to exclude the effects of unpredictable factors.
Alternatively, how to integrate these factors effectively into the model to improve prediction accuracy.
-----

https://github.com/msitt/blpapi-python/blob/master/README.md
https://github.com/GoogleChromeLabs/chrome-for-testing/blob/main/data/latest-versions-per-milestone-with-downloads.json
