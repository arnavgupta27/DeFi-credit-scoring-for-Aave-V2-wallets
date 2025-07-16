Credit Score Analysis and Results
Overview
This document analyzes the distribution and behavior of credit scores assigned to Aave V2 wallets using our machine learning pipeline.
Credit scores range from 0 to 1000, where higher scores indicate greater responsible on-chain behavior and lower risk; lower scores flag risky, bot-like, or inactive wallets.
We leverage engineer features, real DeFi risk signals, and XGBoost ML scoring, with wallet segmentation into “Prime,” “Near Prime,” “Subprime,” and “Deep Subprime” bands.

1. Score Distribution
1.1. Score Histogram (0–1000, bins of 100)
![Score Histogram by 100s](score_hist_by_100.png histogram visualizes how wallets are distributed across score intervals (0-100, 100-200, ..., 900-1000). Most users fall into the lower or baseline bands, with a long right tail. This reflects typical DeFi user behavior: most users are inactive or low-activity, while only a minority are long-lived, responsible borrowers.)

1.2. Score Density (KDE Line over Histogram)
![Score Histogram with DensityInterpretation**: The kernel density curve highlights both the main mass of scores at the baseline and the gradual thinning out for higher scores, confirming no abnormal spikes or bi-modality.]

2. Credit Bands and Segmentation
2.1. Wallet Count by Credit Band
![Credit Band Barplot](score_band_bar.png bar chart displays the number of users in each credit segment ("Prime", "Near Prime", "Subprime", "Deep Subprime"). Most users are "Deep Subprime" (inactive or minimal activity), with meaningful populations in the other bands. This clear risk stratification matches credit industry conventions and aids protocol-level decision making.)

2.2. Credit Score Distribution by Band
![Score Band Boxplot](score_band_boxplot:
Boxplots show that "Prime" users have much higher median and less spread, while "Deep Subprime" clusters at the baseline (e.g., 350 for inactives). Wider boxes in middle bands indicate more diverse user behaviors and scores.)

3. Wallet Behavior by Score Range
For each feature, insert the named plot file; add a 1-2 line summary below it as shown:
3.1. Activity Duration by Score Range
![log_activity_duration_days_by_score_bin.png](log_activity_duration_days_by users are much more likely to achieve higher scores, reflected in the rising median and upper box edges with score bins.)

3.2. Repayments by Score Range
![log_num_repays_by_score_bin.png](log_num_repays_by_score_bin.png higher score bins consistently display more repayments, indicating responsible risk management.)

3.3. Liquidations by Score Range
![log_num_liquidations_by_score_bin.png](log_num_liquidations with low scores experience more liquidations; this feature's box shrinks and drops as scores increase.)

3.4. Utilization Rate by Score Range
![utilization_rate_by_score_bin.png](utilizationigher utilization (more aggressive borrowing) is concentrated among lower and mid-range scores, supporting its penalty in scoring logic.)

3.5. Borrow–Repay Ratio by Score Range
![borrow_repay_ratio_by_score_bin.png](borrow_repay_ratio_by_score_bin.png ratios—indicative of regular periods of both borrowing and repaying—are more common among high-score users.)

3.6. Unique Token Count by Score Range
![unique_token_count_by_score_bin.png](unique_token_count_by_score_bin engaging with a greater diversity of tokens are much more likely to achieve higher scores.)

4. Feature Relationships and Correlations
![numeric_features_heatmap.png](numericThe feature correlation heatmap reveals expected relationships (e.g., counts/sums tending to co-move), and supports that features like liquidations and repayments provide non-redundant information for the model.)

5. Summary of Wallet Behaviors
Low range (Deep Subprime 0–399):

Mostly inactive, little or no repayment, short-lived. Many have only deposited, sometimes redeemed. Liquidations are rare in this range, but most users here simply haven't taken risk.

Subprime (400–599):

More activity, sometimes single or sporadic borrows/repays. Duration slowly rises. Show some engagement, but not sustained.

Near Prime (600–699):

Clear regularity in repayments, longer tenure, diversified tokens, few or no liquidations.

Prime (≥700):

Long active duration, frequent and timely repayments, diversified assets, very low or zero liquidations. Exemplifies “ideal” on-chain borrowing history.

6. Key Insights & Takeaways
The scoring model successfully segments risk and user behavior in a DeFi context, closely tracking established credit analytics methodology[].

Inactive baseline and "Prime" behavior are clearly separated, supporting both protocol risk controls and user transparency.

Visualizations confirm model calibration: Outliers are handled smoothly, and interpretability is maintained for protocol or user-facing dashboards.

7. Instructions for Reproduction
See README.md for full pipeline and data processing steps.

Plots in this analysis can be generated by running analysis_plots.py in Colab, as described in the repository.