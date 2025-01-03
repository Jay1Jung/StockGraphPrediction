#!/usr/bin/env Rscript

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

# Define required packages
required_packages <- c("readr", "corrplot", "psych", "olsrr", "stringdist")

# Install missing packages
install_if_missing(required_packages)

# Confirm all packages are loaded
sapply(required_packages, require, character.only = TRUE)

print("---- All required packages are installed and loaded successfully ----")

# Dynamically determine the script's directory
get_script_path <- function() {
  cmdArgs <- commandArgs(trailingOnly = FALSE)
  needle <- "--file="
  match <- grep(needle, cmdArgs)
  if (length(match) > 0) {
    # Rscript
    return(normalizePath(sub(needle, "", cmdArgs[match])))
  } else {
    # 'source'd via R console
    return(normalizePath(sys.frames()[[1]]$ofile))
  }
}

script_path <- get_script_path()
script_dir <- dirname(script_path)

# Define the path to the CSV file relative to the script's directory
csv_path <- file.path(script_dir, "../../", "data", "formatted", "merged_all_data.csv")

print(paste("CSV path set to:", csv_path))

# Check if the CSV file exists
if(!file.exists(csv_path)){
  stop(paste("CSV file does not exist at path:", csv_path))
}

print("Starting R script execution")

# Read the CSV file
initdata <- read.csv(csv_path, stringsAsFactors = FALSE)

# Print the number of rows in the dataset
print(paste("Total rows in initdata:", nrow(initdata)))

# Display the column names
print("---- Column Names in Data Frame ----")
print(colnames(initdata))

# Subset the data
subset_start <- 1
subset_end <- 1461

# Validate subset range
if(nrow(initdata) < subset_end){
  stop(paste("Data has only", nrow(initdata), "rows. Cannot subset up to row", subset_end))
}

# Subset the data
initdataf <- initdata[subset_start:subset_end, ]

# Describe the manufacturing_pmi_Actual
print("---- Description of manufacturing_pmi_Actual ----")
description <- describe(initdataf$manufacturing_pmi_Actual, fast = TRUE)
print(description)

# ---------------------- #
# **Added Helper Function**
# ---------------------- #

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
      print(paste0("Found a close match for '", missing, "': '", closest, "'. Renaming it to '", missing, "'."))
      # Rename the column in the data frame
      names(data_frame)[names(data_frame) == closest] <- missing
      # Update the available_cols vector
      available_cols[available_cols == closest] <- missing
    } else {
      print(paste0("No close match found for '", missing, "'. Please verify the column name."))
    }
  }
  return(data_frame)
}

# Define a function to perform analysis for a given stock
perform_stock_analysis <- function(stock_symbol, data_frame, pmi_column) {
  stock_column <- paste0(stock_symbol, "_closing")
  if(!stock_column %in% colnames(data_frame)) {
    print(paste("Stock column", stock_column, "not found in data. Skipping analysis for", stock_symbol))
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
    print(paste("Missing predictor columns for", stock_symbol, ":", paste(missing_predictors, collapse = ", ")))
    
    # Call the suggestion and renaming function
    data_frame <- suggest_and_rename_columns(missing_predictors, colnames(data_frame), data_frame)
    
    # Re-check if columns are now present after renaming
    missing_predictors <- setdiff(predictor_columns, colnames(data_frame))
    if(length(missing_predictors) > 0){
      print(paste("Still missing predictor columns for", stock_symbol, ":", paste(missing_predictors, collapse = ", ")))
      return(NULL)  # Skip analysis for this stock
    }
  }
  
  # Ensure columns are numeric
  columns_to_check <- c(stock_column, predictor_columns)
  for(col in columns_to_check){
    if(!is.numeric(data_frame[[col]])){
      print(paste("Converting column", col, "to numeric."))
      data_frame[[col]] <- as.numeric(data_frame[[col]])
      if(any(is.na(data_frame[[col]]))){
        print(paste("Warning: NAs introduced by coercion in column", col))
      }
    }
  }
  
  # Perform correlation test
  corr_columns <- c(stock_column, predictor_columns)
  available_corr_columns <- corr_columns[sapply(data_frame[, corr_columns], function(x) !all(is.na(x)))]
  
  if(length(available_corr_columns) < 2){
    print(paste("Not enough columns available for correlation analysis for", stock_symbol))
  } else {
    corr_results <- corr.test(data_frame[, available_corr_columns], adjust = "none")
    print(paste("---- Correlation Test Results for", stock_symbol, "----"))
    print(corr_results)
  }
  
  # Build the linear model
  formula_str <- paste(stock_column, "~", paste(predictor_columns, collapse = " + "))
  formula <- as.formula(formula_str)
  
  stock_model <- lm(formula, data = data_frame)
  print(paste("---- Linear Model Summary for", stock_symbol, "----"))
  print(summary(stock_model))
  
  # Perform stepwise regression
  step_results <- ols_step_both_p(stock_model, pent=0.05, prem=0.10, progress=TRUE, detail=TRUE)
  print(paste("---- Stepwise Regression Results for", stock_symbol, "----"))
  print(step_results)
  
  # Check VIF and Tolerance
  vif_tol <- ols_vif_tol(stock_model)
  print(paste("---- VIF and Tolerance for", stock_symbol, "----"))
  print(vif_tol)
}

# Analysis for Technology Sector
print("===== Technology Sector =====")
tech_stocks <- list(
  list(symbol = "NVDA", pmi_column = "manufacturing_pmi_Actual"),
  list(symbol = "AAPL", pmi_column = "manufacturing_pmi_Actual"),
  list(symbol = "MSFT", pmi_column = "services_pmi_Actual")
)

for(stock in tech_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}

# Analysis for Financial Service Sector
print("===== Financial Service Sector =====")
financial_stocks <- list(
  list(symbol = "BX", pmi_column = "services_pmi_Actual"),
  list(symbol = "V", pmi_column = "services_pmi_Actual"),
  list(symbol = "JPM", pmi_column = "services_pmi_Actual")
)

for(stock in financial_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}

# Analysis for Consumer Cyclical Sector
print("===== Consumer Cyclical Sector =====")
consumer_cyclical_stocks <- list(
  list(symbol = "AMZN", pmi_column = "services_pmi_Actual"),
  list(symbol = "TSLA", pmi_column = "manufacturing_pmi_Actual"),
  list(symbol = "SBUX", pmi_column = "services_pmi_Actual")
)

for(stock in consumer_cyclical_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}

# Analysis for Healthcare Sector
print("===== Healthcare Sector =====")
healthcare_stocks <- list(
  list(symbol = "LLY", pmi_column = "manufacturing_pmi_Actual"),
  list(symbol = "ABBV", pmi_column = "manufacturing_pmi_Actual"),
  list(symbol = "UNH", pmi_column = "services_pmi_Actual")
)

for(stock in healthcare_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}

# Analysis for Communication Services Sector
print("===== Communication Services Sector =====")
communication_stocks <- list(
  list(symbol = "GOOGL", pmi_column = "services_pmi_Actual"),
  list(symbol = "META", pmi_column = "services_pmi_Actual"),
  list(symbol = "NFLX", pmi_column = "services_pmi_Actual")
)

for(stock in communication_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}

# Analysis for Industrials Sector
print("===== Industrials Sector =====")
industrials_stocks <- list(
  list(symbol = "GE", pmi_column = "manufacturing_pmi_Actual"),
  list(symbol = "RTX", pmi_column = "manufacturing_pmi_Actual"),
  list(symbol = "LMT", pmi_column = "manufacturing_pmi_Actual")
)

for(stock in industrials_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}

# Analysis for Consumer Defensive Sector
print("===== Consumer Defensive Sector =====")
consumer_defensive_stocks <- list(
  list(symbol = "WMT", pmi_column = "services_pmi_Actual"),
  list(symbol = "COST", pmi_column = "services_pmi_Actual"),
  list(symbol = "TGT", pmi_column = "services_pmi_Actual")
)

for(stock in consumer_defensive_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}

# Analysis for Energy Sector
print("===== Energy Sector =====")
energy_stocks <- list(
  list(symbol = "XOM", pmi_column = NA),
  list(symbol = "CVX", pmi_column = NA)
)

for(stock in energy_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}

# Analysis for Basic Materials Sector
print("===== Basic Materials Sector =====")
basic_materials_stocks <- list(
  list(symbol = "LIN", pmi_column = NA),
  list(symbol = "SHW", pmi_column = NA)
)

for(stock in basic_materials_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}

# Analysis for Utilities Sector
print("===== Utilities Sector =====")
utilities_stocks <- list(
  list(symbol = "NEE", pmi_column = "manufacturing_pmi_Actual")
)

for(stock in utilities_stocks){
  perform_stock_analysis(stock$symbol, initdataf, stock$pmi_column)
}
