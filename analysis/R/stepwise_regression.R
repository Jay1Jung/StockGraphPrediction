#!/usr/bin/env Rscript

# **1. Package Management**

# Function to check and install missing packages
install_if_missing <- function(packages) {
  for(pkg in packages){
    if(!require(pkg, character.only = TRUE)){
      install.packages(pkg, repos = "https://cloud.r-project.org/")
      if(!require(pkg, character.only = TRUE)){
        stop(paste("Package", pkg, "could not be installed."))
      }
    }
  }
}

# Define required packages, including 'lubridate' for date handling
required_packages <- c("readr", "corrplot", "psych", "olsrr", "stringdist", "lubridate", "future.apply")

# Install missing packages
install_if_missing(required_packages)

# Confirm all packages are loaded
sapply(required_packages, require, character.only = TRUE)

message("---- All required packages are installed and loaded successfully ----")

# **2. Script Path Configuration**
# Function to dynamically determine the script's path
get_script_path <- function() {
  cmdArgs <- commandArgs(trailingOnly = FALSE)
  needle <- "--file="
  match <- grep(needle, cmdArgs)
  if (length(match) > 0) {
    # Rscript execution
    return(normalizePath(sub(needle, "", cmdArgs[match])))
  } else {
    # 'source'd via R console
    return(normalizePath(sys.frames()[[1]]$ofile))
  }
}

script_path <- get_script_path()
script_dir <- dirname(script_path)

# **3. CSV and Tickers File Path Setup**
# Define the path to the CSV file relative to the script's directory
csv_path <- normalizePath(file.path(script_dir, "../../", "data", "formatted", "merged_all_data.csv"), 
                         winslash = "/", mustWork = FALSE)

message(paste("CSV path set to:", csv_path))

# Define the path to the tickers.txt file relative to the script's directory
tickers_file_path <- normalizePath(file.path(script_dir, "../../", "tickers.txt"), 
                                   winslash = "/", mustWork = FALSE)

message(paste("Tickers file path set to:", tickers_file_path))

# **4. Load Tickers Function**
# Function to load tickers from a text file
load_tickers <- function(ticker_file) {
  if(!file.exists(ticker_file)){
    stop(paste("Ticker file does not exist at path:", ticker_file))
  }
  
  tickers <- readLines(ticker_file, warn = FALSE)
  
  # Clean tickers: remove whitespace and replace '.' with '-'
  tickers <- gsub("\\s+", "", tickers)  # Remove all whitespace
  tickers <- gsub("\\.", "-", tickers)  # Replace '.' with '-'
  
  # Remove empty entries
  tickers <- tickers[tickers != ""]
  
  return(tickers)
}

# **5. CSV File Existence Check**

# Check if the CSV file exists
if(!file.exists(csv_path)){
  stop(paste("CSV file does not exist at path:", csv_path))
}
message("Starting R script execution")

# **6. Data Loading and Subsetting**
# Read the CSV file
initdata <- read.csv(csv_path, stringsAsFactors = FALSE)
# Print the number of rows in the dataset
message(paste("Total rows in initdata:", nrow(initdata)))
# Display the column names
message("---- Column Names in Data Frame ----")
print(colnames(initdata))
# Convert 'Date' column to Date format if not already
if(!inherits(initdata$Date, "Date")){
  initdata$Date <- as.Date(initdata$Date)
  if(any(is.na(initdata$Date))){
    warning("Some dates could not be converted and are set to NA.")
  }
}
# Determine the subset range dynamically based on the latest date and desired window
# For example, select the last 4 years of data
# Define the number of years to include
years_to_include <- 4
# Find the latest date in the data
latest_date <- max(initdata$Date, na.rm = TRUE)
# Define the start date by subtracting 'years_to_include' from the latest date
start_date <- latest_date %m-% years(years_to_include)
# Find the row indices where Date >= start_date
subset_rows <- which(initdata$Date >= start_date)
# Check if any rows meet the condition
if(length(subset_rows) == 0){
  stop(paste("No data available since", start_date))
}
# Define subset_start and subset_end dynamically
subset_start <- min(subset_rows)
subset_end <- nrow(initdata)
message(paste("Subsetting data from row", subset_start, "to row", subset_end, 
              "(", format(initdata$Date[subset_start], "%Y-%m-%d"), 
              "to", format(initdata$Date[subset_end], "%Y-%m-%d"), ")"))

# Subset the data
initdataf <- initdata[subset_start:subset_end, ]

# **7. Data Description**
# Describe the manufacturing_pmi_Actual if it exists
if("manufacturing_pmi_Actual" %in% colnames(initdataf)){
  message("---- Description of manufacturing_pmi_Actual ----")
  description <- describe(initdataf$manufacturing_pmi_Actual, fast = TRUE)
  print(description)
} else {
  message("Column 'manufacturing_pmi_Actual' does not exist in the subset data.")
}

# **8. Helper Functions**
# Helper function to suggest possible column name corrections and optionally rename them
suggest_and_rename_columns <- function(missing_cols, available_cols, data_frame, threshold = 0.2){
  for(missing in missing_cols){
    # Compute string distances using Jaro-Winkler method
    distances <- stringdist::stringdist(tolower(missing), tolower(available_cols), method = "jw")
    # Find the closest match
    closest <- available_cols[which.min(distances)]
    closest_distance <- min(distances)
    # If the closest distance is below a threshold (e.g., 0.2), suggest it
    if(closest_distance < threshold){
      message(paste0("Found a close match for '", missing, "': '", closest, "'. Renaming it to '", missing, "'."))
      # Rename the column in the data frame
      names(data_frame)[names(data_frame) == closest] <- missing
      # Update the available_cols vector
      available_cols[available_cols == closest] <- missing
    } else {
      message(paste0("No close match found for '", missing, "'. Please verify the column name."))
    }
  }
  return(data_frame)
}

# Function to backup existing processed CSVs
backup_existing_csv <- function(processed_dir, ticker){
  processed_csv_path <- file.path(processed_dir, paste0(ticker, ".csv"))
  if(file.exists(processed_csv_path)){
    timestamp <- format(Sys.time(), "%Y%m%d%H%M%S")
    backup_path <- file.path(processed_dir, paste0(ticker, "_backup_", timestamp, ".csv"))
    file.copy(processed_csv_path, backup_path)
    message(paste("Backed up existing CSV for", ticker, "to", backup_path))
  }
}

# Function to get PMI column based on stock symbol
get_pmi_column <- function(ticker){
  # Define PMI columns for each stock
  # Modify this as per your sector-specific PMI mappings
  sector_pmi <- list(
    # Technology Sector
    NVDA = "manufacturing_pmi_Actual",
    AAPL = "manufacturing_pmi_Actual",
    MSFT = "services_pmi_Actual",
    
    # Financial Service Sector
    BX = "services_pmi_Actual",
    V = "services_pmi_Actual",
    JPM = "services_pmi_Actual",
    
    # Consumer Cyclical Sector
    AMZN = "services_pmi_Actual",
    TSLA = "manufacturing_pmi_Actual",
    SBUX = "services_pmi_Actual",
    
    # Healthcare Sector
    LLY = "manufacturing_pmi_Actual",
    ABBV = "manufacturing_pmi_Actual",
    UNH = "services_pmi_Actual",
    
    # Communication Services Sector
    GOOGL = "services_pmi_Actual",
    META = "services_pmi_Actual",
    NFLX = "services_pmi_Actual",
    
    # Industrials Sector
    GE = "manufacturing_pmi_Actual",
    RTX = "manufacturing_pmi_Actual",
    LMT = "manufacturing_pmi_Actual",
    
    # Consumer Defensive Sector
    WMT = "services_pmi_Actual",
    COST = "services_pmi_Actual",
    TGT = "services_pmi_Actual",
    
    # Energy Sector
    XOM = NA,
    CVX = NA,
    
    # Basic Materials Sector
    LIN = NA,
    SHW = NA,
    
    # Utilities Sector
    NEE = "manufacturing_pmi_Actual"
  )
  
  if(ticker %in% names(sector_pmi)){
    return(sector_pmi[[ticker]])
  } else {
    return(NA)
  }
}

# **9. Stock Analysis Function**
# Define a function to perform analysis for a given stock
perform_stock_analysis <- function(stock_symbol, data_frame, pmi_column) {
  stock_column <- paste0(stock_symbol, "_closing")
  
  # Check if the stock's closing column exists
  if(!stock_column %in% colnames(data_frame)) {
    message(paste("Stock column", stock_column, "not found in data. Skipping analysis for", stock_symbol))
    return(NULL)
  }
  
  # Define predictor columns based on PMI column
  predictor_columns <- c("CPI", "GDP", "LeadingIndex", "Unemployment.Rate", "Interest_rate")
  if(!is.na(pmi_column)){
    predictor_columns <- c(predictor_columns, pmi_column)
  }
  
  # Ensure all predictor columns exist
  missing_predictors <- setdiff(predictor_columns, colnames(data_frame))
  if(length(missing_predictors) > 0) {
    message(paste("Missing predictor columns for", stock_symbol, ":", paste(missing_predictors, collapse = ", ")))
    
    # Call the suggestion and renaming function
    data_frame <- suggest_and_rename_columns(missing_predictors, colnames(data_frame), data_frame)
    
    # Re-check if columns are now present after renaming
    missing_predictors <- setdiff(predictor_columns, colnames(data_frame))
    if(length(missing_predictors) > 0){
      message(paste("Still missing predictor columns for", stock_symbol, ":", paste(missing_predictors, collapse = ", ")))
      return(NULL)  # Skip analysis for this stock
    }
  }
  
  # Ensure columns are numeric
  columns_to_check <- c(stock_column, predictor_columns)
  for(col in columns_to_check){
    if(!is.numeric(data_frame[[col]])){
      message(paste("Converting column", col, "to numeric."))
      data_frame[[col]] <- as.numeric(data_frame[[col]])
      if(any(is.na(data_frame[[col]]))){
        message(paste("Warning: NAs introduced by coercion in column", col))
      }
    }
  }
  
  # Remove predictors with zero variance
  non_constant_predictors <- predictor_columns[sapply(data_frame[, predictor_columns, drop = FALSE], function(x) var(x, na.rm = TRUE) > 0)]
  constant_predictors <- setdiff(predictor_columns, non_constant_predictors)
  
  if(length(constant_predictors) > 0){
    message(paste("Removing constant predictors for", stock_symbol, ":", paste(constant_predictors, collapse = ", ")))
    predictor_columns <- non_constant_predictors
  }
  
  if(length(predictor_columns) == 0){
    message(paste("No valid predictor columns left after removing constants for", stock_symbol, ". Skipping analysis."))
    return(NULL)
  }
  
  # Perform correlation test with error handling
  corr_columns <- c(stock_column, predictor_columns)
  available_corr_columns <- corr_columns[sapply(data_frame[, corr_columns, drop = FALSE], function(x) !all(is.na(x)))]
  
  if(length(available_corr_columns) < 2){
    message(paste("Not enough columns available for correlation analysis for", stock_symbol))
  } else {
    # Try to compute correlation, handle cases with zero variance
    tryCatch({
      corr_results <- corr.test(data_frame[, available_corr_columns, drop = FALSE], adjust = "none")
      message(paste("---- Correlation Test Results for", stock_symbol, "----"))
      print(corr_results)
    }, error = function(e){
      message(paste("Correlation test failed for", stock_symbol, ":", e$message))
    })
  }
  
  # Build the linear model with error handling
  formula_str <- paste(stock_column, "~", paste(predictor_columns, collapse = " + "))
  formula <- as.formula(formula_str)
  
  stock_model <- tryCatch({
    lm(formula, data = data_frame)
  }, error = function(e){
    message(paste("Linear model failed for", stock_symbol, ":", e$message))
    return(NULL)
  })
  
  if(is.null(stock_model)){
    return(NULL)
  }
  
  message(paste("---- Linear Model Summary for", stock_symbol, "----"))
  print(summary(stock_model))
  
  # Perform stepwise regression with error handling
  step_results <- tryCatch({
    ols_step_both_p(stock_model, pent=0.05, prem=0.10, progress=TRUE, detail=TRUE)
  }, error = function(e){
    message(paste("Stepwise regression failed for", stock_symbol, ":", e$message))
    return(NULL)
  })
  
  if(!is.null(step_results)){
    message(paste("---- Stepwise Regression Results for", stock_symbol, "----"))
    print(step_results)
  }
  
  # Check VIF and Tolerance with error handling
  vif_tol <- tryCatch({
    ols_vif_tol(stock_model)
  }, error = function(e){
    message(paste("VIF/Tolerance calculation failed for", stock_symbol, ":", e$message))
    return(NULL)
  })
  
  if(!is.null(vif_tol)){
    message(paste("---- VIF and Tolerance for", stock_symbol, "----"))
    print(vif_tol)
  }
  
  # Optionally, return the model or any other relevant information
  return(data_frame)
}

# **10. Parallel Formatting and Analysis**
# Define a function to perform parallel formatting and analysis
get_formatted_data_parallel <- function(){
  # Load all tickers
  tryCatch({
    tickers <- load_tickers(tickers_file_path)
    message(paste("Loaded", length(tickers), "tickers from", tickers_file_path))
  }, error = function(e){
    message(paste("Error loading tickers:", e$message))
    return(list())
  })
  
  data <- list()
  
  # Define a worker function for parallel processing
  worker <- function(ticker){
    pmi_column <- get_pmi_column(ticker)
    df <- perform_stock_analysis(ticker, initdataf, pmi_column)
    if(!is.null(df)){
      return(list(ticker = ticker, df = df))
    } else {
      return(NULL)
    }
  }
  
  # Use future.apply for parallel processing
  # Adjust the number of workers based on your system's capabilities
  plan(multisession, workers = 10)
  
  results <- future_lapply(tickers, worker)
  
  # Filter out NULL results and build the data list
  for(res in results){
    if(!is.null(res)){
      data[[res$ticker]] <- res$df
    }
  }
  
  message("All tickers have been processed.")
  return(data)
}

# **11. Main Formatting Process**
# Define a function to choose between sequential and parallel processing
get_formatted_data <- function(){
  # Choose between sequential or parallel processing
  # Uncomment the desired option
  
  # Sequential Processing
  # formatted_data <- list()
  # for(ticker in tickers){
  #   pmi_column <- get_pmi_column(ticker)
  #   df <- perform_stock_analysis(ticker, initdataf, pmi_column)
  #   if(!is.null(df)){
  #     formatted_data[[ticker]] <- df
  #   }
  # }
  
  # Parallel Processing
  formatted_data <- get_formatted_data_parallel()
  
  return(formatted_data)
}

# **12. Execute the Script**
formatted_data <- get_formatted_data()
print(class(formatted_data))  # Should print "list"

# Example: Accessing a specific ticker's DataFrame
example_ticker <- "AAPL"
if(example_ticker %in% names(formatted_data)){
  message(paste("\nFirst 5 rows for", example_ticker, ":"))
  print(head(formatted_data[[example_ticker]], 5))
} else {
  message(paste(example_ticker, "not found in the formatted data."))
}

