import pandas as pd
import numpy as np
import os

# ===== 1. Đọc dữ liệu gốc =====
file_path = r"D:\Truc_quan\Data_Jobs.csv"
df = pd.read_csv(file_path, encoding="latin1")

print("📌 Kích thước dữ liệu ban đầu:", df.shape)

# ===== 2. Xử lý trùng lặp (Integrity) =====
subset_cols = [col for col in ["Job_ID", "Job_Title", "JD_Trans"] if col in df.columns] # Chỉ chọn các cột có trong DataFrame
if subset_cols: # Kiểm tra nếu có cột để xóa trùng
    df = df.drop_duplicates(subset=subset_cols) # Xóa trùng dựa trên các cột đã chọn
print("✅ Sau khi xóa trùng:", df.shape)

# ===== 3. Xử lý giá trị thiếu (Accuracy + Integrity) =====
# Numeric: median
num_cols = [col for col in ["Min_YOE", "Est_Salary"] if col in df.columns] # Chỉ chọn các cột số có trong DataFrame
for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Text: NaN -> "Unknown"
text_cols = df.select_dtypes(include="object").columns
df[text_cols] = df[text_cols].fillna("Unknown")

# Role: NaN -> 0
role_cols = ["Data_Engineer","Data_Analyst","Data_Scientist",
             "Business_Analyst","Business_Intelligence",
             "Combined_role","Others"]
for col in role_cols:
    if col not in df.columns:
        df[col] = 0
df[role_cols] = df[role_cols].fillna(0).astype(int)

# ===== 4. Chuẩn hóa dữ liệu (Consistency) =====
# Job_Title
df["Job_Title"] = df["Job_Title"].str.strip().str.title()

# Location
df["Location"] = df["Location"].str.strip().str.upper()
location_map = {
    "HN": "HANOI", "HA NOI": "HANOI", "HÀ NỘI": "HANOI",
    "HCM": "HCMC", "HO CHI MINH": "HCMC", "TPHCM": "HCMC", "TP. HCM": "HCMC",
    "VIETNAM": "VIETNAM", "VN": "VIETNAM", "VN*": "VIETNAM", "VN ( HN": "VIETNAM",
    "REMOTE": "REMOTE"
}
df["Location"] = df["Location"].replace(location_map)
valid_locations = ["HANOI", "HCMC", "VIETNAM", "REMOTE"]
df.loc[~df["Location"].isin(valid_locations), "Location"] = "UNKNOWN"

# ===== Loại bỏ dữ liệu PHILIPPINES và UNKNOWN =====
print(f"📌 Trước khi lọc Location: {df.shape[0]} dòng")
df = df[df["Location"].isin(valid_locations)]
print(f"✅ Sau khi loại bỏ PHILIPPINES & UNKNOWN: {df.shape[0]} dòng")

# Min_YOE
df["Min_YOE"] = df["Min_YOE"].round().astype(int)
df = df[df["Min_YOE"] >= 0]
# Loại bỏ các dòng có Min_YOE quá cao (ví dụ > 40 năm)
df = df[df["Min_YOE"] <= 40]

# Est_Salary: xử lý outliers (z-score)
z_scores = (df["Est_Salary"] - df["Est_Salary"].mean()) / df["Est_Salary"].std()
df = df[np.abs(z_scores) <= 3]

# ===== 5. Đảm bảo tính toàn vẹn (Integrity) =====
df.loc[df["Job_Title"].str.contains("Data Engineer", case=False), "Data_Engineer"] = 1
df.loc[df["Job_Title"].str.contains("Data Analyst", case=False), "Data_Analyst"] = 1
df.loc[df["Job_Title"].str.contains("Data Scientist", case=False), "Data_Scientist"] = 1
df.loc[df["Job_Title"].str.contains("Business Analyst", case=False), "Business_Analyst"] = 1

# Đảm bảo có ít nhất 1 role
df["Role_Sum"] = df[role_cols].sum(axis=1)
df.loc[df["Role_Sum"] == 0, "Others"] = 1
df.drop(columns="Role_Sum", inplace=True)

# Đảm bảo Job_ID duy nhất
if "Job_ID" in df.columns:
    df = df.drop_duplicates(subset=["Job_ID"])

# ===== 6. Thêm Last_Updated (Timeliness) =====
df["Last_Updated"] = pd.Timestamp.today().strftime("%Y-%m-%d")

# ===== 7. Xuất dữ liệu =====
cleaned_path = r"D:\Truc_quan\Data_Jobs_Clean.csv"
if os.path.exists(cleaned_path):
    os.remove(cleaned_path)

df.to_csv(cleaned_path, index=False, encoding="utf-8-sig")

print("✅ Dữ liệu đã làm sạch & chuẩn hóa xong")
print("📂 Lưu tại:", cleaned_path)
print("🌍 Location duy nhất:", df["Location"].unique())
print("💰 Lương min:", df["Est_Salary"].min(), "max:", df["Est_Salary"].max())
print("⏰ Last_Updated:", df["Last_Updated"].iloc[0])
