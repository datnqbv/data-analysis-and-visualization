import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ===== 1. Đọc dữ liệu =====
file_path = r"D:\Truc_quan\Data_Jobs_Clean.csv"
df = pd.read_csv(file_path, encoding="utf-8")

print("Kích thước dữ liệu:", df.shape)
print(df.info())
print(df.describe())

# ===== 2. Tạo thư mục lưu ảnh =====
save_dir = r"D:\Truc_quan\charts"
os.makedirs(save_dir, exist_ok=True)

# ===== 3. Thống kê cơ bản =====
print("\nTop 10 Job phổ biến nhất:")
print(df["Job_Title"].value_counts().head(10))

print("\nMức lương trung bình theo Job:")
print(df.groupby("Job_Title")["Est_Salary"].mean().sort_values(ascending=False).head(10))

# ===== 4. Biểu đồ =====

# 4.1 Top 10 Job phổ biến
# This block of code is creating a bar plot to visualize the top 10 most common job titles in the
# dataset. Here's a breakdown of each step:
plt.figure(figsize=(10,6))
df["Job_Title"].value_counts().head(10).plot(kind="bar", color="skyblue")
plt.title("Top 10 Job phổ biến")
plt.xlabel("Job Title")
plt.ylabel("Số lượng")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "top_10_jobs.png"))
plt.close()

# 4.2 Phân bố mức lương
plt.figure(figsize=(8,5))
sns.histplot(df["Est_Salary"], bins=30, kde=True)
plt.title("Phân bố mức lương (Est_Salary)")
plt.xlabel("Lương ước tính")
plt.ylabel("Số lượng")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "salary_distribution.png"))
plt.close()

# 4.3 Boxplot mức lương theo Job (Top 5 job phổ biến)
top_jobs = df["Job_Title"].value_counts().head(5).index
plt.figure(figsize=(10,6))
sns.boxplot(data=df[df["Job_Title"].isin(top_jobs)], x="Job_Title", y="Est_Salary")
plt.title("Phân bố lương theo Top 5 Job phổ biến")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "salary_boxplot_top5.png"))
plt.close()

# 4.4 Phân bố số năm kinh nghiệm
plt.figure(figsize=(8,5))
sns.countplot(x="Min_YOE", data=df, palette="Set2")
plt.title("Phân bố số năm kinh nghiệm (Min_YOE)")
plt.xlabel("Số năm kinh nghiệm tối thiểu")
plt.ylabel("Số lượng Job")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "experience_distribution.png"))
plt.close()

# 4.5 Heatmap tương quan
plt.figure(figsize=(6,4))
sns.heatmap(df[["Min_YOE", "Est_Salary"]].corr(), annot=True, cmap="Blues", fmt=".2f")
plt.title("Tương quan giữa Kinh nghiệm và Lương")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "heatmap_correlation.png"))
plt.close()

# 4.6 Số lượng job theo Location
plt.figure(figsize=(8,5))
sns.countplot(x="Location", data=df, order=df["Location"].value_counts().index, palette="viridis")
plt.title("Số lượng Job theo Location")
plt.xlabel("Location")
plt.ylabel("Số lượng Job")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "jobs_by_location.png"))
plt.close()

# 4.7 Top 5 Job phổ biến phân bố theo Location (Grouped bar)
plt.figure(figsize=(10,6))
sns.countplot(x="Location", hue="Job_Title", 
              data=df[df["Job_Title"].isin(top_jobs)],
              order=df["Location"].value_counts().index,
              palette="Set3")
plt.title("Top 5 Job phổ biến theo Location")
plt.xlabel("Location")
plt.ylabel("Số lượng Job")
plt.legend(title="Job Title")
plt.tight_layout()
plt.savefig(os.path.join(save_dir, "top5_jobs_by_location.png"))
plt.close()


print(f"✅ Đã lưu tất cả biểu đồ trong thư mục: {save_dir}")
