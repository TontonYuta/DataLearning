#!/usr/bin/env python3
"""
PROJECT 0: Personal Data CLI Analyzer
Tu dong kiem tra va bao cao ho so chat luong du lieu (CSV va Parquet).
Cach dung:
    python analyzer.py --file ../../data/input.csv --output report.txt
"""

import argparse
import sys
import os
import pandas as pd
import numpy as np

def analyze_dataset(file_path: str, output_path: str = None) -> None:
    if not os.path.exists(file_path):
        print(f"[!] Loi: Khong tim thay file '{file_path}'!")
        sys.exit(1)

    print(f"[*] Dang phan tich file: {file_path}...")
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.parquet'):
            df = pd.read_parquet(file_path)
        else:
            print("[!] Chi ho tro file .csv va .parquet!")
            sys.exit(1)
    except Exception as e:
        print(f"[!] Loi khi doc file: {e}")
        sys.exit(1)

    total_rows, total_cols = df.shape
    dupes = df.duplicated().sum()
    mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)

    lines = [
        "=" * 65,
        "          BAO CAO HO SO DU LIEU (DATA PROFILING REPORT)",
        "=" * 65,
        f"Tong so ban ghi (Rows)       : {total_rows:,}",
        f"Tong so cot (Columns)        : {total_cols}",
        f"Ban ghi trung lap (Dupes)    : {dupes:,} ({dupes/total_rows*100:.2f}%)",
        f"Dung luong bo nho (RAM)      : {mem_mb:.2f} MB",
        "-" * 65,
        f"{'Ten Cot':<22} | {'Kieu Dlieu':<10} | {'Null Count':<10} | {'Null %':<7} | {'Unique'}",
        "-" * 65
    ]

    for col in df.columns:
        null_cnt = df[col].isnull().sum()
        null_pct = (null_cnt / total_rows) * 100
        dtype_str = str(df[col].dtype)
        unique_cnt = df[col].nunique()
        lines.append(f"{col:<22} | {dtype_str:<10} | {null_cnt:>10} | {null_pct:>6.1f}% | {unique_cnt:>6}")

    lines.append("-" * 65)
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        lines.append("THONG KE COT SO (NUMERICAL METRICS):")
        desc = df[num_cols].describe().T[['mean', 'std', 'min', '50%', 'max']]
        desc.rename(columns={'50%': 'median'}, inplace=True)
        lines.append(desc.to_string())

    report_str = "\n".join(lines)
    print(report_str)

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_str)
        print(f"\n[+] Da luu bao cao vao: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI Data Profiler Tool")
    parser.add_argument("--file", "-f", required=True, help="Duong dan den file du lieu")
    parser.add_argument("--output", "-o", required=False, help="Duong dan file luu bao cao")
    args = parser.parse_args()
    analyze_dataset(args.file, args.output)
