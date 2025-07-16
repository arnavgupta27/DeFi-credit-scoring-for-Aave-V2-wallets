import pandas as pd
import numpy as np

def clean_data(df):
    df.columns = [str(c).strip() for c in df.columns]
    required_fields = ['userWallet', 'action', 'timestamp']
    df = df.dropna(subset=required_fields)
    df = df[df['userWallet'].astype(str).str.strip().ne('')]

    df['userWallet'] = df['userWallet'].astype(str).str.strip().str.lower()
    df['action'] = df['action'].astype(str).str.strip().str.lower()
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
    df['assetSymbol'] = df.get('assetSymbol', '').astype(str).str.strip().str.upper()
    df['amount'] = pd.to_numeric(df.get('amount', np.nan), errors='coerce')
    df['assetPriceUSD'] = pd.to_numeric(df.get('assetPriceUSD', np.nan), errors='coerce')
    df['valueUSD'] = df['amount'] * df['assetPriceUSD']
    if 'referral' not in df.columns:
        df['referral'] = np.nan
    return df

def feature_engineering(df):
    grouped = df.groupby('userWallet', as_index=True)
    features = pd.DataFrame()

    def event_count(x, act): return (x['action'] == act).sum()
    def value_sum(x, act): return x.loc[(x['action'] == act) & (x['valueUSD'].notnull()), 'valueUSD'].sum()

    # Event counts
    features['num_deposits'] = grouped.apply(lambda x: event_count(x, 'deposit'))
    features['num_borrows'] = grouped.apply(lambda x: event_count(x, 'borrow'))
    features['num_repays'] = grouped.apply(lambda x: event_count(x, 'repay'))
    features['num_redeems'] = grouped.apply(lambda x: event_count(x, 'redeemunderlying'))
    features['num_liquidations'] = grouped.apply(lambda x: event_count(x, 'liquidationcall'))

    # USD-value based sums
    features['sum_deposit_usd'] = grouped.apply(lambda x: value_sum(x, 'deposit'))
    features['sum_borrow_usd'] = grouped.apply(lambda x: value_sum(x, 'borrow'))
    features['sum_repay_usd'] = grouped.apply(lambda x: value_sum(x, 'repay'))
    features['sum_redeem_usd'] = grouped.apply(lambda x: value_sum(x, 'redeemunderlying'))

    features['liquidation_ratio'] = features['num_liquidations'] / (features['num_borrows'] + 1)
    features['utilization_rate'] = features['sum_borrow_usd'] / (features['sum_deposit_usd'] + 1)
    features['borrow_repay_ratio'] = features['sum_borrow_usd'] / (features['sum_repay_usd'] + 1)
    features['unique_token_count'] = grouped['assetSymbol'].nunique()

    def activity_days(grp):
        times = grp['timestamp']
        return (times.max() - times.min()).days if times.nunique() > 1 else 0
    features['activity_duration_days'] = grouped.apply(activity_days)

    features['total_actions'] = grouped.size()
    features['actions_per_day'] = features['total_actions'] / (features['activity_duration_days'] + 1)

    def mean_interval(grp):
        times = grp['timestamp'].sort_values()
        if len(times) < 2:
            return 0.0
        intervals = times.diff().dropna().dt.total_seconds()
        return intervals.mean() if not intervals.empty else 0.0

    features['mean_txn_interval_sec'] = grouped.apply(mean_interval)

    features['referral_count'] = grouped['referral'].apply(lambda x: x.notnull().sum()) if 'referral' in df.columns else 0
    features = features.replace([np.inf, -np.inf], np.nan).fillna(0)
    return features

if __name__ == "__main__":
    input_file = 'output.csv'
    output_file = 'user_features.csv'
    df = pd.read_csv(input_file, low_memory=False)
    df_clean = clean_data(df)
    features_df = feature_engineering(df_clean)
    features_df.reset_index(inplace=True)
    features_df.to_csv(output_file, index=False)
    print(f"User-level features saved to {output_file} with {len(features_df)} users.")
