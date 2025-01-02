# Stock Price Prediction Using Economic Indicators

## Table of Contents
- [Introduction](#introduction)
- [Objectives](#objectives)
- [Pending Indicators](#pending-indicators)
- [Regression Models](#regression-models)
- [Challenges](#challenges)
- [Critical Considerations](#critical-considerations)
- [Additional References](#additional-references)

---

## Introduction

Understanding the intricate relationship between economic indicators and sector-wise stock movements is pivotal for accurate financial forecasting. This project aims to analyze how various economic indicators influence stock prices across different sectors and predict the impact of upcoming economic announcements on these prices. Additionally, the project explores graph-based prediction methods to enhance the accuracy and robustness of these forecasts.

---

## Objectives

1. **Correlation Analysis**
   - **Goal:** Understand how economic indicators correlate with sector-wise stock movements.
   
2. **Predictive Modeling**
   - **Goal:** Predict how upcoming economic announcements (e.g., CPI or interest rate changes) affect stock prices within each sector.
   
3. **Graph-Based Prediction**
   - **Goal:** Implement graph-based methodologies to capture complex relationships between sectors and economic indicators for improved prediction accuracy.

---

## Pending Indicators

The following economic indicators are yet to be processed and integrated into the analysis:

1. **신규 실업수당청구건수 (New Jobless Claims)**
2. **S&P 글로벌 합성 PMI (S&P Global Composite PMI)**
3. **근원 PCE 가격지수 (Core PCE Price Index)**
4. **EIA 원유재고 (EIA Crude Oil Inventories)**
5. **신규주택판매 (New Home Sales)**
6. **컨퍼런스보드 소비자신뢰지수 (Conference Board Consumer Confidence Index)**
7. **미국 국채경매 (U.S. Treasury Auctions)**
8. **기존주택판매 (Existing Home Sales)**
9. **PPI 상승률 (PPI Inflation Rate)**

---

## Regression Models

### Multiple Linear Regression

- **Purpose:** To model the linear relationship between multiple economic indicators and sector-wise stock prices.
- **Implementation:**
  - **Dependent Variable:** Sector-wise Closing Prices
  - **Independent Variables:** Economic Indicators (CPI, GDP, LeadingIndex, Unemployment.Rate, Interest_rate)

### Regularized Regression (Ridge, Lasso)

- **Purpose:** To handle multicollinearity and perform feature selection.
- **Implementation:**
  - Apply Ridge Regression to penalize large coefficients.
  - Apply Lasso Regression for both regularization and variable selection.

### Time-Series Models (ARIMA, VAR)

- **Purpose:** To capture temporal dependencies and trends in stock prices and economic indicators.
- **Implementation:**
  - Use ARIMA for individual time-series forecasting.
  - Use VAR for modeling interdependencies between multiple time-series.

### Machine Learning Models (Random Forest, Gradient Boosting)

- **Purpose:** To capture non-linear relationships and interactions between variables.
- **Implementation:**
  - Train Random Forest and Gradient Boosting models on the dataset.
  - Compare performance with regression models.

### Stepwise Regression with `olsrr`

- **Purpose:** To identify significant predictors through automated feature selection.
- **Implementation:**
  - Utilize `ols_step_both_p` from the `olsrr` package for stepwise selection.

---

## Challenges

1. **Influence of Unpredictable Factors**
   - **Issue:** Stock price movements are influenced by factors beyond economic indicators, such as geopolitical events, company-specific news, and market sentiment.
   
2. **Data Quality and Availability**
   - **Issue:** Missing data, inconsistent data sources, and varying data frequencies can hinder accurate analysis.
   
3. **Model Overfitting**
   - **Issue:** Complex models may capture noise instead of the underlying relationship, leading to poor generalization on unseen data.
   
4. **Temporal Dependencies**
   - **Issue:** Economic indicators and stock prices exhibit temporal dependencies that need to be appropriately modeled.

---

## Critical Considerations

1. **Excluding the Effects of Unpredictable Factors**
   - **Strategy:**
     - Incorporate control variables that capture market sentiment or geopolitical events.
     - Use dummy variables to represent significant events.
     - Perform residual analysis to identify patterns indicating omitted variable effects.
   
2. **Incorporating Unpredictable Factors to Improve Prediction Accuracy**
   - **Strategy:**
     - Utilize Principal Component Analysis (PCA) to reduce dimensionality and capture major variance components.
     - Implement mixed models to account for both fixed effects (economic indicators) and random effects (unpredictable factors).
     - Explore hybrid models combining statistical and machine learning approaches.
     - Use ensemble methods to aggregate predictions from multiple models for robustness.

3. **Data Type and Quality Assurance**
   - Ensure all relevant columns are numeric.
   - Handle missing values through imputation or exclusion.
   - Verify consistency in date formats and align temporal ranges across datasets.

4. **Feature Engineering**
   - Create lagged features and moving averages to capture delayed effects.
   - Develop graph-based features to represent relationships between sectors and indicators.

5. **Model Evaluation**
   - Use appropriate metrics such as RMSE, MAE, and R-squared.
   - Validate models using train-test splits that respect temporal order to prevent look-ahead bias.

---

## Additional References

### Books and Articles

1. **"Econometric Analysis" by William H. Greene**
   - Comprehensive coverage of econometric models and techniques.
   
2. **"Introduction to Time Series and Forecasting" by Peter J. Brockwell and Richard A. Davis**
   - In-depth exploration of time-series analysis methods.
   
3. **"Applied Predictive Modeling" by Max Kuhn and Kjell Johnson**
   - Practical guide to building predictive models using R.
   
4. **Research Papers on Graph Neural Networks**
   - Explore recent advancements in GNNs for financial predictions.

### Online Tutorials and Courses

1. **Coursera**
   - Courses on financial modeling, machine learning, and time-series analysis.
   
2. **edX**
   - Offers courses related to econometrics and data science.
   
3. **Kaggle**
   - Participate in financial forecasting competitions and explore related notebooks.

### R Packages Documentation

1. **`olsrr`**
   - [Documentation](https://www.rdocumentation.org/packages/olsrr/versions/4.2.0)
   
2. **`corrplot`**
   - [Documentation](https://www.rdocumentation.org/packages/corrplot/versions/0.92)
   
3. **`igraph`**
   - [Documentation](https://www.rdocumentation.org/packages/igraph/versions/1.2.6)
   
4. **`ggraph`**
   - [Documentation](https://www.rdocumentation.org/packages/ggraph/versions/2.0.7)

---

## Conclusion

This project aims to bridge the gap between economic indicators and sector-wise stock movements through robust regression models and advanced graph-based prediction techniques. By addressing the inherent challenges and incorporating critical considerations, the project seeks to enhance the accuracy and reliability of stock price predictions amidst a landscape of unpredictable influencing factors.

---

