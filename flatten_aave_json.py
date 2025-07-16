import pandas as pd
import json
import sys
import os

def flatten_record(record):
    import pandas as pd
    flat = pd.json_normalize(record)

    # Convert _id.$oid to _id
    if "_id.$oid" in flat.columns:
        flat["_id"] = flat["_id.$oid"]
        flat = flat.drop(columns=["_id.$oid"])
    if "createdAt.$date" in flat.columns:
        flat["createdAt"] = flat["createdAt.$date"]
        flat = flat.drop(columns=["createdAt.$date"])
    if "updatedAt.$date" in flat.columns:
        flat["updatedAt"] = flat["updatedAt.$date"]
        flat = flat.drop(columns=["updatedAt.$date"])

    # Find all 'actionData.*' columns
    action_data_cols = [c for c in flat.columns if c.startswith("actionData.")]
    if action_data_cols:
        # Extract and rename them
        action_data = flat[action_data_cols].copy()
        action_data.columns = [c.replace("actionData.", "") for c in action_data_cols]
        # Drop the original 'actionData.*' columns before concatenation
        flat = flat.drop(columns=action_data_cols)
        # Concatenate the flattened columns
        flat = pd.concat([flat, action_data], axis=1)
    return flat


def main(input_json_path, output_csv_path):
    # Load input file
    try:
        with open(input_json_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("❌ Error: JSON file must contain a list of transaction records.")
        sys.exit(1)

    # Flatten all records
    flat_records = []
    for record in data:
        flat = flatten_record(record)
        flat_records.append(flat)

    # Combine into final DataFrame
    final_df = pd.concat(flat_records, ignore_index=True)

    # Save to output CSV
    final_df.to_csv(output_csv_path, index=False)
    print(f"✅ Flattened CSV saved as '{output_csv_path}' with {len(final_df)} records and {len(final_df.columns)} columns.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("\n🟡 Usage:\n  python flatten_aave_json.py <input_file.json> <output_file.csv>\n")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    main(input_path, output_path)
