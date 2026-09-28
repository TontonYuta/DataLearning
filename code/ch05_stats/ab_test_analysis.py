"""
PROJECT 3: A/B TESTING CHECKOUT EXPERIMENT ANALYSIS
Data Mastery All-In-One (2026 Edition)
Performs SRM check, Two-Proportion Z-Test, and Segmented Analysis on ab_test_checkout.csv.
Pure Python + Pandas implementation (works with or without scipy).
"""

import math
import numpy as np
import pandas as pd
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "ab_test_checkout.csv"

def norm_cdf(z: float) -> float:
    """Cumulative distribution function for standard normal distribution."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

def run_ab_test():
    print("=" * 65)
    print("PROJECT 3: A/B TESTING STATISTICAL ANALYSIS")
    print("=" * 65)
    
    if not DATA_FILE.exists():
        print(f"Error: {DATA_FILE} not found!")
        return

    df = pd.read_csv(DATA_FILE)
    print(f"Dataset Loaded: {len(df):,} total participants.")
    
    # -------------------------------------------------------------
    # 1. SRM Check (Sample Ratio Mismatch)
    # -------------------------------------------------------------
    print("\n[STEP 1] Sample Ratio Mismatch (SRM) Validation")
    counts = df["group"].value_counts()
    n_ctrl = int(counts.get("control", 0))
    n_treat = int(counts.get("treatment", 0))
    total_n = n_ctrl + n_treat
    expected = total_n / 2.0
    
    # Chi-square Goodness of Fit (Expected 50:50) with 1 degree of freedom
    chi2_stat = ((n_ctrl - expected) ** 2 / expected) + ((n_treat - expected) ** 2 / expected)
    # For df=1, p-value = 1 - Chi2_CDF(chi2) = 2 * (1 - Norm_CDF(sqrt(chi2)))
    srm_p_value = 2.0 * (1.0 - norm_cdf(math.sqrt(chi2_stat)))
    
    print(f"Control Count  : {n_ctrl:,} ({n_ctrl/total_n*100:.2f}%)")
    print(f"Treatment Count: {n_treat:,} ({n_treat/total_n*100:.2f}%)")
    print(f"Chi2 Statistic : {chi2_stat:.4f} | p-value: {srm_p_value:.4f}")
    
    if srm_p_value < 0.01:
        print(">> [ALERT] CRITICAL SRM DETECTED! Traffic allocation is biased. Do NOT trust results.")
    else:
        print(">> [PASS] No SRM detected. Traffic is split evenly 50:50.")

    # -------------------------------------------------------------
    # 2. Conversion Metrics & Two-Proportion Z-Test
    # -------------------------------------------------------------
    print("\n[STEP 2] Conversion Rate & Two-Proportion Z-Test")
    conv_ctrl = int(df[df["group"] == "control"]["converted"].sum())
    conv_treat = int(df[df["group"] == "treatment"]["converted"].sum())
    
    cr_ctrl = conv_ctrl / n_ctrl
    cr_treat = conv_treat / n_treat
    abs_lift = cr_treat - cr_ctrl
    rel_lift = (cr_treat - cr_ctrl) / cr_ctrl * 100
    
    # Pooled standard error
    pooled_p = (conv_ctrl + conv_treat) / total_n
    se_pooled = math.sqrt(pooled_p * (1.0 - pooled_p) * (1.0 / n_ctrl + 1.0 / n_treat))
    z_stat = (cr_treat - cr_ctrl) / se_pooled
    p_val = 2.0 * (1.0 - norm_cdf(abs(z_stat)))
    
    # 95% Confidence Interval for difference
    se_diff = math.sqrt((cr_ctrl * (1.0 - cr_ctrl) / n_ctrl) + (cr_treat * (1.0 - cr_treat) / n_treat))
    ci_lower = abs_lift - 1.96 * se_diff
    ci_upper = abs_lift + 1.96 * se_diff
    
    print(f"Control CR     : {cr_ctrl:.4f} ({cr_ctrl*100:.2f}%) [{conv_ctrl:,} / {n_ctrl:,}]")
    print(f"Treatment CR   : {cr_treat:.4f} ({cr_treat*100:.2f}%) [{conv_treat:,} / {n_treat:,}]")
    print(f"Absolute Lift  : {abs_lift:+.4f} ({abs_lift*100:+.2f}% percentage points)")
    print(f"Relative Lift  : {rel_lift:+.2f}%")
    print(f"Z-Statistic    : {z_stat:.4f}")
    print(f"p-value        : {p_val:.4e}")
    print(f"95% CI of Diff : [{ci_lower*100:+.3f}%, {ci_upper*100:+.3f}%]")

    # -------------------------------------------------------------
    # 3. Segmented Analysis (Check for Simpson's Paradox)
    # -------------------------------------------------------------
    print("\n[STEP 3] Segmented Analysis by Device")
    segment_df = df.groupby(["device", "group"])["converted"].agg(["count", "sum"]).reset_index()
    segment_df["cr"] = segment_df["sum"] / segment_df["count"]
    
    for device in df["device"].unique():
        sub = segment_df[segment_df["device"] == device]
        c_sub = sub[sub["group"] == "control"].iloc[0]
        t_sub = sub[sub["group"] == "treatment"].iloc[0]
        dev_lift = (t_sub["cr"] - c_sub["cr"]) / c_sub["cr"] * 100
        print(f"- Device: {device.upper():<8} | Control: {c_sub['cr']*100:.2f}% | Treatment: {t_sub['cr']*100:.2f}% | Lift: {dev_lift:+.2f}%")

    # -------------------------------------------------------------
    # 4. Final Business Decision
    # -------------------------------------------------------------
    print("\n" + "=" * 65)
    print("EXECUTIVE DECISION & BUSINESS RECOMMENDATION")
    print("=" * 65)
    if p_val < 0.05 and abs_lift > 0 and ci_lower > 0:
        print("[RECOMMENDATION: SHIP IT!]")
        print("The new checkout flow demonstrated a statistically significant improvement.")
        print(f"Expected uplift: {rel_lift:+.2f}% with 95% confidence bounds [{ci_lower*100:+.2f}%, {ci_upper*100:+.2f}%].")
        print("Action: Roll out the new checkout design to 100% of production users.")
    else:
        print("[RECOMMENDATION: DO NOT SHIP]")
        print("No statistically significant positive effect was observed.")
        print("Action: Retain current checkout baseline and iterate on UX hypotheses.")
    print("=" * 65)

if __name__ == "__main__":
    run_ab_test()
