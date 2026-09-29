# DATA MASTERY ALL-IN-ONE (2026 EDITION)
## Lộ Trình Thực Chiến Toàn Diện: Data Analyst (DA) – Data Engineer (DE) – Data Scientist (DS) & MLOps

[![Build Status](https://img.shields.io/badge/PDF_Pages-162_Pages-brightgreen)](main.pdf)
[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-orange.svg)](#)

Cuốn sách và kho lưu trữ mã nguồn mở cung cấp giáo trình **All-In-One** chuẩn công nghiệp giúp bạn tự học từ con số 0 đến cấp độ Middle/Senior trong ngành dữ liệu. Toàn bộ nội dung tập trung vào **thực chiến**, đi kèm **20 dự án ứng dụng chuyên sâu**, **hướng dẫn phỏng vấn 5 vòng**, **CV chuẩn ATS**, và **120 bài tập thực hành gắn liền với số liệu cụ thể**.

---

## 📖 Tải Giáo Trình Hoàn Chỉnh (Bản PDF 162 Trang)

Bạn có thể tải hoặc đọc trực tiếp tài liệu biên soạn bằng LaTeX chuyên nghiệp:
* **[Tải File PDF: DATA_MASTERY_ALL_IN_ONE_2026.pdf (162 Trang)](main.pdf)**

---

## 📂 Cấu Trúc Kho Lưu Trữ

```text
Data_Handbook/
├── main.tex                    # Mã nguồn chính sách LaTeX All-in-One (XeLaTeX)
├── main.pdf                    # Bản PDF hoàn chỉnh đã biên dịch (162 trang)
├── README.md                   # Hướng dẫn chi tiết sử dụng kho lưu trữ
├── requirements.txt            # Danh sách thư viện Python cần thiết
│
├── chapters/                   # 16 Chương giáo trình chuyên sâu (Level 0 -> Level 10)
│   ├── ch00_setup_environment.tex      # Thiết lập môi trường Linux, VS Code, Git, Docker
│   ├── ch01_overview.tex               # Bản đồ năng lực DA vs DS vs DE, AI Copilot Workflow
│   ├── ch02_level0_fundamentals.tex    # Nền tảng Linux CLI, Bash scripting, Git Pro
│   ├── ch03_level1_python.tex          # Python từ số 0, OOP, NumPy, Pandas, Vectorization
│   ├── ch04_level2_sql.tex             # SQL từ số 0, Window Functions, Recursive CTE, Query Optimization
│   ├── ch05_level3_stats.tex           # Xác suất thống kê, Suy luận định lượng, A/B Testing, SRM
│   ├── ch06_level4_da_bi.tex           # Phân tích nghiệp vụ, Cây chỉ số KPI, Power BI / Metabase
│   ├── ch07_level5_de_etl.tex          # Kỹ nghệ dữ liệu: Data Modeling Kimball, ETL Pipeline
│   ├── ch08_level6_de_pro.tex          # Data Pipeline nâng cao: Apache Airflow, dbt, Data Quality
│   ├── ch09_level7_ml.tex              # Machine Learning từ trực giác toán học đến Scikit-Learn
│   ├── ch10_level8_bigdata.tex         # Dữ liệu lớn: Apache Spark (PySpark), Broadcast Join, Delta Lake
│   ├── ch11_level9_cloud.tex           # Hạ tầng Cloud Data: AWS S3, Snowflake, BigQuery
│   ├── ch12_level10_mlops.tex          # MLOps: FastAPI Microservice, Docker, Locust, Drift Detection
│   ├── ch13_capstone.tex               # 20 Dự Án Thực Tế Nghiên Cứu Sâu (DA, DE, DS, MLOps)
│   ├── ch14_career_cv_interview.tex    # Kỹ năng phỏng vấn 5 vòng, Bí quyết viết CV ATS, 5 Mẫu CV
│   └── ch15_solutions.tex              # Tóm tắt đáp án và chỉ dẫn thực hành
│
├── workbook/                   # Hệ thống 120 bài tập thực hành gắn với số liệu cụ thể
│   ├── part1_excel.tex         # 20 Bài tập Excel & Nghiệp vụ (kèm tệp .xlsx đa sheet)
│   ├── part2_python.tex        # 20 Bài tập Python & Pandas (kèm order_items.csv, input.csv)
│   ├── part3_sql.tex           # 20 Bài tập SQL chuyên sâu (kèm runner SQLite in-memory)
│   ├── part4_stats.tex         # 20 Bài tập Thống kê & A/B Test (kèm ab_test_checkout.csv)
│   ├── part5_business.tex      # 20 Bài toán Phân tích Nghiệp vụ (kèm customer_churn_features.csv)
│   └── part6_de_mlops.tex      # 20 Bài tập Kỹ thuật DE & MLOps (kèm raw_transactions.csv)
│
├── data/                       # Dữ liệu thực hành thực tế
│   ├── excel_practice_data.xlsx    # Bảng tính Excel 6 sheets (NhanVien, CuocVanChuyen, DoanhSo, ...)
│   ├── customers.csv               # 2,000 khách hàng trên 5 thành phố lớn
│   ├── orders.csv                  # 10,000 đơn hàng TMĐT (Completed, Cancelled, Refunded)
│   ├── order_items.csv             # 24,837 dòng chi tiết mặt hàng và doanh số GMV
│   ├── payments.csv                # 10,000 lượt thanh toán qua 4 phương thức
│   ├── input.csv                   # 5,017 bản ghi có khuyết thiếu và ngoại lai để làm sạch
│   ├── raw_transactions.csv        # 10,000 giao dịch thô kiểm thử pipeline ETL
│   ├── ab_test_checkout.csv        # 50,000 người dùng thử nghiệm luồng thanh toán
│   └── customer_churn_features.csv # 10,000 hồ sơ khách hàng dự đoán churn
│
└── code/                       # Mã nguồn thực thi chuẩn mẫu
    ├── ch02_cli/analyzer.py            # CLI Tool phân tích log
    ├── ch03_python/eda_pipeline.py     # Pipeline EDA, tăng trưởng MoM và quy luật Pareto 80/20
    ├── ch04_sql/ecommerce_queries.sql  # Toàn bộ truy vấn SQL chuẩn hóa
    ├── ch04_sql/run_queries.py         # Script nạp CSV vào SQLite và chạy truy vấn tự động
    ├── ch05_stats/ab_test_analysis.py  # Script kiểm định A/B Test (SRM, Z-test, CI)
    ├── ch07_etl/batch_etl.py           # Pipeline Batch ETL nạp dữ liệu sạch vào Data Warehouse
    ├── ch08_orchestration/ecommerce_dag.py # Apache Airflow DAG TaskFlow
    ├── ch09_ml/train_churn.py          # Huấn luyện Random Forest và xuất file model
    ├── ch10_bigdata/pyspark_pipeline.py# PySpark Broadcast Join & Aggregation
    └── ch12_mlops/app.py               # FastAPI Serving Model thời gian thực
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Thực Hành

### 1. Khởi tạo môi trường ảo Python

```bash
git clone https://github.com/TontonYuta/DataLearning.git
cd DataLearning

python3 -m venv data_env
source data_env/bin/activate
pip install -r requirements.txt
```

### 2. Chạy thử nghiệm các Project mẫu

* **Phân tích Khám phá Dữ liệu TMĐT (Project 1 - Python EDA):**
  ```bash
  python3 code/ch03_python/eda_pipeline.py
  ```

* **Thực thi phân tích SQL trên cơ sở dữ liệu in-memory (Project 2 - SQL Analytics):**
  ```bash
  python3 code/ch04_sql/run_queries.py
  ```

* **Kiểm định Thống kê & Phân tích A/B Testing (Project 3 - A/B Test):**
  ```bash
  python3 code/ch05_stats/ab_test_analysis.py
  ```

* **Chạy đường ống ETL nạp kho dữ liệu Data Warehouse (Project 5 - Batch ETL):**
  ```bash
  python3 code/ch07_etl/batch_etl.py
  ```

* **Huấn luyện Mô hình Machine Learning Churn (Project 7 - ML Pipeline):**
  ```bash
  python3 code/ch09_ml/train_churn.py
  ```

* **Khởi chạy Microservice API dự đoán thời gian thực (FastAPI Serving):**
  ```bash
  uvicorn code.ch12_mlops.app:app --host 0.0.0.0 --port 8000 --reload
  ```

---

## 🛠️ Biên Dịch Lại Sách PDF (XeLaTeX)

Tài liệu sử dụng font chữ **Times New Roman** và **Liberation Mono** trên nền `pdflatex/xelatex`:

```bash
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

---

## 💼 Kỹ Năng Nghề Nghiệp & Mẫu CV Có Sẵn

Chương 14 của cuốn sách cung cấp:
1. **Chiến lược phỏng vấn 5 vòng**: HR Screening, SQL/Python Live Coding, Business Case, System Design & Architecture, Culture Fit.
2. **Kỹ thuật viết CV chuẩn ATS**: Nguyên tắc định lượng Google XYZ (`Accomplished [X] as measured by [Y], by doing [Z]`), tối ưu từ khóa kỹ thuật.
3. **5 Bộ CV Mẫu Thực Chiến Hoàn Chỉnh**:
   * *CV 1*: Data Analyst Intern
   * *CV 2*: Data Engineer Intern
   * *CV 3*: Middle Data Analyst (2--3 năm kinh nghiệm)
   * *CV 4*: Middle Data Engineer (Data Platform & Lakehouse)
   * *CV 5*: Middle Data Scientist / MLOps Engineer

---

## 👨‍💻 Tác Giả & Đóng Góp

* Kho tài liệu được xây dựng nhằm phục vụ cộng đồng học tập dữ liệu thực chiến tại Việt Nam.
* Mọi đóng góp, phản hồi xin vui lòng tạo Issue hoặc gửi Pull Request tới [TontonYuta/DataLearning](https://github.com/TontonYuta/DataLearning).
