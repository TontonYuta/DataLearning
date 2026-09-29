"""
Generates concrete Excel practice workbook (excel_practice_data.xlsx)
for Workbook Part 1: 20 Excel Exercises.
"""

import random
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import date, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_EXCEL = BASE_DIR / "data" / "excel_practice_data.xlsx"

def generate_excel():
    print("Generating concrete Excel practice workbook...")
    random.seed(42)
    np.random.seed(42)

    with pd.ExcelWriter(OUTPUT_EXCEL, engine="openpyxl") as writer:
        # Sheet 1: NhanVien (A1:D101)
        nv_ids = [f"NV{101 + i}" for i in range(100)]
        ho_list = ["Nguyen", "Tran", "Le", "Pham", "Hoang", "Phan", "Vu", "Vo", "Dang", "Bui"]
        dem_list = ["Van", "Thi", "Hoang", "Minh", "Quoc", "Thanh", "Duc", "Ngoc", "Phuong"]
        ten_list = ["An", "Binh", "Cuong", "Dat", "Em", "Gia", "Hai", "Hung", "Khanh", "Linh", "Minh", "Nam", "Phong", "Quan", "Son", "Tu", "Vinh"]
        depts = ["Kinh Doanh", "Ky Thuat", "Tai Chinh", "Nhan Su", "Marketing", "Van Hanh"]

        nv_data = []
        for i, nid in enumerate(nv_ids):
            if nid == "NV105":
                name = "Phan Van Dat"
                dept = "Kinh Doanh"
                salary = 28000000
            else:
                name = f"{random.choice(ho_list)} {random.choice(dem_list)} {random.choice(ten_list)}"
                dept = random.choice(depts)
                salary = int(random.randint(12, 60) * 1000000)
            nv_data.append({"Ma_NV": nid, "Ho_Ten": name, "Phong_Ban": dept, "Luong_VND": salary})
        df_nv = pd.DataFrame(nv_data)
        df_nv.to_excel(writer, sheet_name="NhanVien", index=False)

        # Sheet 2: CuocVanChuyen (2-way matrix)
        provinces = ["Hanoi", "Ho Chi Minh", "Da Nang", "Can Tho", "Hai Phong", "Hue", "Nha Trang", "Vung Tau"]
        cuoc_data = {
            "Tinh_Thanh": provinces,
            "1kg": [22000, 30000, 26000, 32000, 24000, 27000, 29000, 31000],
            "2kg": [28000, 40000, 34000, 42000, 30000, 35000, 38000, 41000],
            "5kg": [45000, 65000, 55000, 70000, 48000, 58000, 62000, 68000],
            "10kg": [75000, 110000, 95000, 120000, 80000, 98000, 105000, 115000]
        }
        df_cuoc = pd.DataFrame(cuoc_data)
        df_cuoc.to_excel(writer, sheet_name="CuocVanChuyen", index=False)

        # Sheet 3: DoanhSo (5,000 rows)
        sales_reps = ["Nguyen Van A", "Tran Thi Binh", "Le Hoang Long", "Pham Minh Tu", "Hoang Thu Ha", "Vu Quoc Anh"]
        regions = ["Mien Bac", "Mien Trung", "Mien Nam"]
        categories = ["Dien Tu", "Thoi Trang", "Gia Dung", "My Pham", "The Thao"]
        statuses = ["COMPLETED", "COMPLETED", "COMPLETED", "OVERDUE", "CANCELLED"]

        start_dt = date(2026, 1, 1)
        doanhso_rows = []
        for i in range(5000):
            d_offset = random.randint(0, 89) # Q1 2026
            dt = start_dt + timedelta(days=d_offset)
            rep = random.choice(sales_reps)
            reg = random.choice(regions)
            cat = random.choice(categories)
            rev = round(float(random.uniform(50, 2500)), 2)
            st = random.choice(statuses)
            doanhso_rows.append({
                "Ma_Don": f"ORD_{100000 + i}",
                "Ngay": dt.strftime("%Y-%m-%d"),
                "Nhan_Vien": rep,
                "Khu_Vuc": reg,
                "Nganh_Hang": cat,
                "Doanh_Thu_USD": rev,
                "Trang_Thai": st
            })
        df_ds = pd.DataFrame(doanhso_rows)
        df_ds.to_excel(writer, sheet_name="DoanhSo", index=False)

        # Sheet 4: ChuoiHoTen (50 full names)
        hoten_samples = [
            f"{random.choice(ho_list)} {random.choice(dem_list)} {random.choice(ten_list)}"
            for _ in range(50)
        ]
        df_names = pd.DataFrame({"Ho_Va_Ten": hoten_samples})
        df_names.to_excel(writer, sheet_name="ChuoiHoTen", index=False)

        # Sheet 5: TidyData_Unpivot
        products = [f"SP_{1000 + i}" for i in range(20)]
        unpivot_data = {"Ma_SP": products}
        for m in range(1, 13):
            unpivot_data[f"Thang_{m}"] = [int(random.randint(100, 1500) * 100) for _ in range(20)]
        df_unpivot = pd.DataFrame(unpivot_data)
        df_unpivot.to_excel(writer, sheet_name="TidyData_Unpivot", index=False)

        # Sheet 6: XuatKho (Reverse search)
        xuatkho_rows = []
        base_skus = ["SP_IPHONE_15", "SP_MACBOOK_M3", "SP_AIRPODS_PRO", "SP_IPAD_AIR", "SP_WATCH_S9"]
        for i in range(200):
            sku = random.choice(base_skus)
            day = date(2026, 1, 1) + timedelta(days=i // 2)
            unit_price = 1000 + (i % 20) * 15
            qty = random.randint(1, 10)
            xuatkho_rows.append({
                "Ma_Xuat": f"XK_{1000 + i}",
                "Ma_SP": sku,
                "Ngay_Xuat": day.strftime("%Y-%m-%d"),
                "Don_Gia_USD": unit_price,
                "So_Luong": qty
            })
        df_xk = pd.DataFrame(xuatkho_rows)
        df_xk.to_excel(writer, sheet_name="XuatKho", index=False)

    print(f"Successfully created: {OUTPUT_EXCEL}")

if __name__ == "__main__":
    generate_excel()
