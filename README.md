# DeFi Credit Scoring for Aave V2 Wallets

## Overview

This project builds a robust, explainable credit scoring pipeline for Ethereum users of the Aave V2 lending protocol, assigning each wallet a score between 0 and 1000 based solely on on-chain DeFi behavior. High scores represent reliable, responsible users; lower scores flag higher risk or bot-like activity.

The project showcases a hybrid engineering pipeline:  
- **Local scripts** for scalable data flattening and feature extraction  
- **Colab notebooks** for exploratory analysis, heuristics, machine learning, comparison, and result visualization

All artifacts and documentation required by the challenge are included.

---

## Repository Structure

.
├── flatten_aave_json.py # (local) JSON flattening to tabular CSV

├── clean_and_engineer.py # (local) Data cleaning and feature engineering

├── model_training_and_analysis.ipynb # (Colab) EDA, heuristics, ML, result visualization

├── user_features_newscored.csv # Engineered features and heuristic/model scores

├── README.md # This file

├── analysis.md # Post-scoring wallet analysis, plots, insights

└── ...


---

## Pipeline and Method

**Step 1:**  
`flatten_aave_json.py`  
_Flattens nested JSON transaction records from Aave V2 to a normalized tabular CSV format, for each action type (borrow, repay, deposit, etc)_.

**Step 2:**  
`clean_and_engineer.py`  
_Cleans and standardizes the raw transaction data, handles missingness and anomalies, and creates user-level, ML-ready features—such as event counts, USD-normalized volumes, risk ratios, and unique token use._

**Step 3:**  
`model_training_and_analysis.ipynb` (Colab)  
- **Initial EDA (Exploratory Data Analysis):**  
  - Visualizes and audits the engineered features.
  - Drops constant, empty, or misleading columns.
  - Inspects distributions, outliers, and feature relationships.

- **Heuristic credit scoring:**  
  - Assigns each wallet a score 0–1000 for transparency and explainability.
  - Segments users into "inactive" (baseline), and active bands ("Prime", "Subprime", etc.)
  - Applies feature scaling, capping, and research-based weights, penalizing liquidations, rewarding repayments/activity/diversity.

- **Model training and comparison:**  
  - Trains XGBoost and LightGBM regression models using the engineered features and heuristic/label scores.
  - Compares by RMSE and R².
  - Adds final ML-predicted credit score as a new column for each wallet.

- **Visualization & analysis:**  
  - Plots credit score and band distributions, uses boxplots, histograms, and EDA to validate model and heuristic behavior.

---

## How to Run

1. Place your Aave transaction JSON file in the working directory of your local machine.
2. Run `flatten_aave_json.py` to generate the tabular CSV.
3. Run `clean_and_engineer.py` to create `user_features.csv` (user-level ML features).
4. Upload `user_features.csv` to Colab.
5. Open and run `model_training_and_analysis.ipynb` for data audit, heuristic scoring, ML model building, and prediction.  
   - The notebook will guide you through visualizations, result analysis, and export the final file with credit scores.

---

## Methodological Highlights

- **Data-Driven & Transparent:**  
  All features, weights, and methods are documented and designed for interpretability and technical rigor.
- **Risk Alignment:**  
  Liquidations sharply penalized, repayments/activity/longevity rewarded.
- **Model Selection:**  
  XGBoost selected via metric comparison (RMSE, R²) for best ML scoring.
- **Banding:**  
  Credit bands ("Prime" ... "Deep Subprime") aid in downstream analysis and communication.

---

## Deliverables

- All code (local and Colab, `.py` and `.ipynb`)
- Post-scoring analysis:  
  See [analysis.md](analysis.md) for wallet behavior insights, score distribution graphs, and feature impact commentary.
- All necessary files and scripts for re-running or extending this solution.

---

## Contact

Arnav Gupta
arnavguptamodinagar@gmail.com

