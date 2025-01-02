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

# Define the path to the CSV file
csv_path <- "/Users/dohhyungjun/Downloads/merged_all_data.csv"

# Check if the CSV file exists
if(!file.exists(csv_path)){
  stop(paste("CSV file does not exist at path:", csv_path))
}

print("Starting R script execution")

# Read the CSV file
priceindic <- read.csv(csv_path, stringsAsFactors = FALSE)

# Print the number of rows in the dataset
print(paste("Total rows in priceindic:", nrow(priceindic)))

# Display the column names
print("---- Column Names in Data Frame ----")
print(colnames(priceindic))

# Define the required columns for analysis
required_columns <- c("Closing.price", "CPI", "GDP", "LeadingIndex", "Unemployment.Rate", "Interest_rate")

# Function to suggest possible correct column names based on similarity
suggest_corrections <- function(missing_cols, available_cols) {
  for(missing in missing_cols){
    # Calculate string distances using Jaro-Winkler distance
    distances <- stringdist::stringdist(tolower(missing), tolower(available_cols), method = "jw")
    # Find the closest match
    closest <- available_cols[which.min(distances)]
    # If the closest distance is below a threshold (e.g., 0.2), suggest it
    if(min(distances) < 0.2){
      print(paste0("Did you mean '", closest, "' instead of '", missing, "'?"))
    } else {
      print(paste0("No close match found for '", missing, "'. Please verify the column name."))
    }
  }
}

# Identify missing columns
missing_columns <- setdiff(required_columns, colnames(priceindic))

if(length(missing_columns) > 0){
  print(paste("Missing required columns:", paste(missing_columns, collapse = ", ")))
  # Suggest possible corrections
  suggest_corrections(missing_columns, colnames(priceindic))
  
  # Optionally, stop execution if critical columns are missing
  # Uncomment the line below to halt the script if columns are missing
  # stop("Please correct the column names in the CSV file and rerun the script.")
  
  # Alternatively, proceed by adding missing columns with NA
  for(col in missing_columns){
    priceindic[[col]] <- NA
    print(paste("Added missing column with NA:", col))
  }
} else {
  print("All required columns are present.")
}

# Subset the data
subset_start <- 1    # Adjusted to start from 1 instead of 0
subset_end <- 1712

# Validate subset range
if(nrow(priceindic) < subset_end){
  stop(paste("Data has only", nrow(priceindic), "rows. Cannot subset up to row", subset_end))
}

# Subset the data
priceindicf <- priceindic[subset_start:subset_end, ]

# Print the number of rows in the subset
print(paste("Total rows in priceindicf:", nrow(priceindicf)))

# Optionally, display the first few rows of the subset to verify (optional)
# head(priceindicf)

# Data Type Validation
numeric_columns <- c("Closing.price", "CPI", "GDP", "LeadingIndex", "Unemployment.Rate", "Interest_rate")

for(col in numeric_columns){
  if(!is.numeric(priceindicf[[col]])){
    print(paste("Converting column", col, "to numeric."))
    priceindicf[[col]] <- as.numeric(priceindicf[[col]])
    if(any(is.na(priceindicf[[col]]))){
      print(paste("Warning: NAs introduced by coercion in column", col))
    }
  }
}

# Describe the Closing Price
description <- describe(priceindicf$Closing.price, fast = TRUE)
print("---- Description of Closing Price ----")
print(description)

# Perform Correlation Test
# Exclude columns that are entirely NA to prevent errors
corr_columns <- c("Closing.price", "CPI", "GDP", "LeadingIndex", "Unemployment.Rate")
available_corr_columns <- intersect(corr_columns, colnames(priceindicf))
available_corr_columns <- available_corr_columns[sapply(priceindicf[, available_corr_columns], function(x) !all(is.na(x)))]

# Print available_corr_columns for debugging
print("Available correlation columns:")
print(available_corr_columns)

if(length(available_corr_columns) < 2){
  print("Not enough columns available for correlation analysis.")
} else {
  # Ensure all selected columns are present in the data frame
  missing_in_subset <- setdiff(available_corr_columns, colnames(priceindicf))
  if(length(missing_in_subset) > 0){
    print(paste("These columns are missing in the subset:", paste(missing_in_subset, collapse = ", ")))
    # Remove missing columns from available_corr_columns
    available_corr_columns <- setdiff(available_corr_columns, missing_in_subset)
    print("Updated available correlation columns:")
    print(available_corr_columns)
  }
  
  # Re-check the number of available columns
  if(length(available_corr_columns) < 2){
    print("Not enough columns available for correlation analysis after removing missing columns.")
  } else {
    # Perform the correlation test
    corr_results <- corr.test(priceindicf[, available_corr_columns], adjust = "none")
    print("---- Correlation Test Results ----")
    print(corr_results)
  }
}

# Build the Linear Model
# Ensure that all predictor variables are present and not entirely NA
predictors <- c("CPI", "GDP", "LeadingIndex", "Unemployment.Rate", "Interest_rate")
available_predictors <- intersect(predictors, colnames(priceindicf))
available_predictors <- available_predictors[sapply(priceindicf[, available_predictors], function(x) !all(is.na(x)))]

if(length(available_predictors) == 0){
  stop("No predictor variables available for linear modeling.")
}

# Construct the formula dynamically
formula_str <- paste("Closing.price ~", paste(available_predictors, collapse = " + "))
formula <- as.formula(formula_str)

# Fit the linear model
Stock.model <- lm(formula, data = priceindicf)
print("---- Linear Model Summary ----")
print(summary(Stock.model))

# Perform Stepwise Regression
# Check if ols_step_both_p can be performed with available predictors
if(length(available_predictors) >= 1){
  step_results <- ols_step_both_p(Stock.model, pent=0.05, prem=0.10, progress=TRUE, detail=TRUE)
  print("---- Stepwise Regression Results ----")
  print(step_results)
} else {
  print("Not enough predictors available for stepwise regression.")
}

# Check Variance Inflation Factor (VIF) and Tolerance
if(exists("Stock.model") && length(available_predictors) >= 1){
  vif_tol <- ols_vif_tol(Stock.model)
  print("---- VIF and Tolerance ----")
  print(vif_tol)
}
