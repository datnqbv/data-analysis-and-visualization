#  DỰ ÁN PHÂN TÍCH VÀ TRỰC QUAN HÓA DỮ LIỆU JOBS

##  TỔNG QUAN DỰ ÁN

Dự án phân tích dữ liệu việc làm trong lĩnh vực Data Science, bao gồm EDA, làm sạch dữ liệu, phân tích nâng cao và trực quan hóa. Dự án sử dụng Python với các thư viện pandas, seaborn, matplotlib, scikit-learn.

##  CẤU TRÚC DỰ ÁN

```
Truc_quan/
├──  Data_Jobs.csv                    # Dữ liệu thô
├──  Data_Jobs_Clean.csv             # Dữ liệu đã làm sạch
├──  01_EDA_Cleaning.ipynb           # Notebook EDA & Làm sạch
├──  02_Advanced_Analysis_NLP_Stats_Model.ipynb  # Notebook phân tích nâng cao (tùy chọn)
├──  analysis.py                     # Script phân tích cơ bản
├──  Clean_data.py                   # Script làm sạch dữ liệu
├──  charts/                         # Thư mục chứa biểu đồ
│   ├── experience_distribution.png
│   ├── heatmap_correlation.png
│   ├── jobs_by_location.png
│   ├── salary_boxplot_top5.png
│   ├── salary_distribution.png
│   ├── top_10_jobs.png
│   └── top5_jobs_by_location.png
└──  README.md                       # File hướng dẫn này
```

##  DỮ LIỆU

### Dataset gốc: `Data_Jobs.csv`
- **Kích thước:** 3,187 records × 24 columns
- **Nguồn:** Dữ liệu việc làm Data Science
- **Encoding:** Latin1

### Dataset đã làm sạch: `Data_Jobs_Clean.csv`
- **Kích thước:** 3,127 records × 25 columns
- **Đã xử lý:** Missing values, outliers, chuẩn hóa
- **Encoding:** UTF-8

### Các cột chính:
- `Job_Title`: Tên công việc
- `Min_YOE`: Số năm kinh nghiệm tối thiểu
- `Est_Salary`: Lương ước tính (VND)
- `Location`: Địa điểm làm việc
- `JD_Trans`: Mô tả công việc
- `Data_Engineer`, `Data_Analyst`, `Data_Scientist`, etc.: Các role flags

##  HƯỚNG DẪN CHẠY DỰ ÁN

### 1. Cài đặt thư viện
```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy statsmodels
```

### 2. Chạy theo thứ tự:

#### Bước 1: EDA & Làm sạch dữ liệu
```bash
# Chạy notebook hoặc script
jupyter notebook 01_EDA_Cleaning.ipynb
# hoặc
python Clean_data.py
```

#### Bước 2: Phân tích nâng cao
```bash
jupyter notebook 02_Advanced_Analysis_NLP_Stats_Model.ipynb
```

#### Bước 3: Phân tích cơ bản (tùy chọn)
```bash
python analysis.py
```

##  CÁC PHÂN TÍCH ĐÃ THỰC HIỆN

### 1. **EDA & Data Cleaning** (`01_EDA_Cleaning.ipynb`)
- ✅ Khảo sát dữ liệu thô
- ✅ Xử lý missing values
- ✅ Xử lý outliers (z-score)
- ✅ Chuẩn hóa dữ liệu
- ✅ So sánh trước/sau làm sạch

### 2. **Advanced Analysis** (`02_Advanced_Analysis_NLP_Stats_Model.ipynb` - tùy chọn)

####  **Biểu đồ chuyên sâu:**
- Phân bố lương theo Role
- Lương theo Location (violin plot)
- Lương theo nhóm kinh nghiệm
- Pairplot mở rộng

####  **NLP Analysis:**
- Khai thác văn bản JD_Trans
- Đếm tần suất kỹ năng (Python, SQL, Power BI, etc.)
- Bigram analysis

####  **Mô hình hóa & đánh giá:**
- Linear Regression (baseline)
- Ridge Regression
- Cross-validation (CV=5)
- Model evaluation (MAE, MAPE)

####  **Clustering & Tương quan:**
- K-means clustering
- Elbow method, Silhouette score
- Correlation matrix & Random Forest feature importance

####  **Phân tích nhóm (nếu dùng clustering):**
- Phân tích đặc điểm từng cluster

####  **Tương quan & tầm quan trọng biến:**
- Ma trận tương quan
- Random Forest feature importance
- Trực quan hóa tương quan

### 3. **Basic Analysis** (`analysis.py`)
- 7 biểu đồ cơ bản
- Thống kê mô tả
- Lưu biểu đồ vào thư mục `charts/`

##  KẾT QUẢ CHÍNH

###  **Insights quan trọng:**
1. **Top 10 jobs phổ biến:** Data Engineer, Data Analyst, Data Scientist
2. **Phân bố lương:** Từ 1,000 - 4,000 VND (triệu)
3. **Kinh nghiệm:** 0-10 năm, tập trung ở 1-3 năm
4. **Location:** HANOI, HCMC chiếm đa số
5. **Tương quan:** Kinh nghiệm có tương quan mạnh với lương

###  **Biểu đồ được tạo:**
- Top 10 jobs phổ biến
- Phân bố lương
- Boxplot lương theo job
- Phân bố kinh nghiệm
- Heatmap tương quan
- Jobs theo location
- Top 5 jobs theo location

##  LÝ THUYẾT NỀN TẢNG (TÓM TẮT)

- **EDA (Exploratory Data Analysis):** giai đoạn khám phá để hiểu cấu trúc, phân phối, tương quan, phát hiện dữ liệu thiếu/ngoại lai trước khi mô hình hóa. Công cụ: thống kê mô tả, histogram/boxplot/pairplot, heatmap.
- **Làm sạch dữ liệu:** đảm bảo 5 tiêu chí chất lượng (Accuracy, Completeness, Consistency, Integrity, Timeliness). Kỹ thuật dùng trong dự án:
  - Điền thiếu: median cho biến số; "Unknown" cho biến text; 0 cho cờ role.
  - Chuẩn hóa: `Job_Title` (title-case), `Location` (uppercase + mapping về tập giá trị hợp lệ).
  - Ngoại lai: z-score |z| ≤ 3 cho `Est_Salary`.
  - Tính toàn vẹn: set role theo `Job_Title`; đảm bảo có ≥1 role; `Job_ID` duy nhất.
- **NLP cơ bản:** tiền xử lý text (lowercase, lọc ký tự), đếm tần suất skill, bigram. Mục tiêu: phác họa nhu cầu kỹ năng thị trường.
- **Hồi quy tuyến tính/Ridge:** mô hình dự đoán lương theo kinh nghiệm và đặc trưng phân loại (one-hot). Ridge giảm phương sai với regularization L2. Đánh giá bằng MAE/MAPE, k-fold CV.
- **Clustering K-means:** phân cụm theo `Min_YOE`, `Est_Salary` (kèm one-hot `Location`). Chọn k bằng Elbow/Silhouette; phân tích đặc trưng từng cụm để định vị phân khúc công việc.
- **Tương quan & Feature importance:** ma trận tương quan để nhìn quan hệ tuyến tính; Random Forest importance để xem đóng góp tương đối (phi tuyến) của biến.

##  QUY TRÌNH & THỰC HÀNH

1) Chuẩn bị môi trường
- Python ≥3.9; thư viện: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `statsmodels` (nếu cần), `scipy` (nếu cần).
- Gợi ý thêm file `requirements.txt` (tuỳ chọn):
  ```
  pandas>=2.0
  numpy>=1.24
  matplotlib>=3.7
  seaborn>=0.12
  scikit-learn>=1.3
  statsmodels>=0.14
  scipy>=1.11
  ```

2) Làm sạch (reproducible) — `Clean_data.py`
- Đọc `Data_Jobs.csv` (latin1), xử lý trùng lặp/thiếu/ngoại lai/chuẩn hóa/location mapping/role flags/`Last_Updated`, xuất `Data_Jobs_Clean.csv` (utf-8-sig).
- Lưu ý: script đang dùng đường dẫn tuyệt đối `D:\Truc_quan\...`. Khi chạy ở máy khác, đổi thành đường dẫn tương đối hoặc tham số hóa (argparse).

3) EDA (giải thích & trực quan) — `01_EDA_Cleaning.ipynb`
- So sánh trước/sau làm sạch cho biến chính (`Est_Salary`, `Min_YOE`).
- Kiểm tra cấu trúc, phân phối, tương quan; ghi nhận quyết định xử lý và tác động.

4) Phân tích nâng cao — `02_Advanced_Analysis_NLP_Stats_Model.ipynb`
- Biểu đồ chuyên sâu: role/location/kinh nghiệm, pairplot.
- NLP: tần suất kỹ năng, bigram; minh họa nhu cầu skill.
- Mô hình: Linear & Ridge (pipeline chuẩn hóa/one-hot); CV=5; báo MAE/MAPE; fit/đánh giá hold-out.
- Clustering: Elbow, Silhouette; k=3 (ví dụ); phân tích cluster (lương/YOE/job phổ biến); scatter Min_YOE vs Est_Salary theo cluster.
- Tương quan & Importance: heatmap các biến số; Random Forest xem mức quan trọng biến (Min_YOE/Location...).
- Ghi chú: phần kiểm định thống kê đã bỏ theo yêu cầu.

5) Phân tích cơ bản — `analysis.py`
- Sinh 7 biểu đồ cốt lõi (top job, lương, boxplot theo top job, kinh nghiệm, heatmap, theo location, top5 theo location) và lưu tại `charts/`.

## CHI TIẾT KẾT QUẢ & DIỄN GIẢI

- Top job phổ biến: nghiêng về Data Engineer/Analyst/Scientist → phản ánh cầu việc làm nhóm Data nền tảng.
- Lương ước tính: tập trung 1,000–4,000 (triệu VND), phân phối lệch phải; boxplot theo nhóm job cho thấy chênh lệch giữa top5 job phổ biến.
- Kinh nghiệm: dồn ở 1–3 năm → thị trường đòi hỏi junior–mid nhiều; phù hợp cơ hội entry-to-mid level.
- Location: HANOI/HCMC chiếm ưu thế; `REMOTE`/`VIETNAM`/`PHILIPPINES` là nhóm nhỏ hơn.
- Tương quan: `Min_YOE`–`Est_Salary` dương rõ; song còn phụ thuộc role/location.
- NLP kỹ năng: Python/SQL/BI (Power BI/Tableau/Excel) thường xuyên xuất hiện → cần đầu tư kỹ năng lõi.
- Hồi quy: Ridge giảm overfit nhẹ; MAE/MAPE ở mức baseline mô tả được xu hướng nhưng còn dư địa cải thiện (bổ sung đặc trưng).
- Clustering: cụm lương–YOE cho thấy phân khúc “junior/median” chiếm số đông, cụm “cao lương–YOE cao” nhỏ hơn.

##  KIỂM CHỨNG & TÁI LẬP

- Chạy `Clean_data.py` để tạo `Data_Jobs_Clean.csv` → mở `analysis.py` hoặc notebook nâng cao.
- Nếu không có `Data_Jobs.csv`, cần cung cấp file gốc cùng cấu trúc như mô tả.
- Kiểm tra ảnh xuất trong `charts/` khớp tiêu đề mục “Biểu đồ được tạo”.

##  HẠN CHẾ & HƯỚNG PHÁT TRIỂN

- Hạn chế:
  - Đường dẫn tuyệt đối Windows → giảm tính di động; nên tham số hóa hoặc dùng đường dẫn tương đối.
  - Lương ước tính/YOE có thể chứa nhiễu do chuẩn hóa; z-score loại ngoại lai tuyến tính, có thể bỏ sót ngoại lai phi tuyến.
  - Mô hình hồi quy đơn giản (ít biến): chưa tính đến text embedding từ `JD_Trans`, tương tác (role×YOE), hiệu ứng location sâu hơn.
  - NLP đếm tần suất đơn giản; chưa lemmatize/stemming hoặc dùng embedding.
- Phát triển:
  - Tách cấu hình (config/argparse/.env); thêm `requirements.txt` + hướng dẫn Docker.
  - Thử Regularization khác (Lasso/ElasticNet), Tree-based (XGBoost/LightGBM) và tối ưu siêu tham số.
  - Trích xuất đặc trưng từ `JD_Trans` (TF-IDF, FastText, BERT) đưa vào mô hình lương.
  - Kiểm định thống kê/Bootstrap CI (nếu cần trong báo cáo học thuật — hiện đã bỏ khỏi notebook theo yêu cầu).
  - Dashboard (Streamlit/Plotly Dash) cho tương tác trực quan.

##  THỰC HÀNH TỐT

- Một nguồn sự thật cho làm sạch: giữ logic trong `Clean_data.py` và để notebook gọi lại nếu cần.
- Gắn nhãn phiên bản dữ liệu (`Last_Updated`) để truy vết.
- Lưu toàn bộ biểu đồ và chốt seed/random_state cho tái lập.
- Thêm unit test nhẹ cho cleaning (kiểm tra mapping location, non-negative `Min_YOE`, không NA sau clean...).

##  CÔNG NGHỆ SỬ DỤNG

### **Thư viện Python:**
- `pandas`: Xử lý dữ liệu
- `numpy`: Tính toán số học
- `matplotlib`: Vẽ biểu đồ cơ bản
- `seaborn`: Vẽ biểu đồ nâng cao
- `scikit-learn`: Machine Learning
- `scipy`: Thống kê
- `statsmodels`: Mô hình thống kê

### **Kỹ thuật phân tích:**
- **EDA:** Exploratory Data Analysis
- **Data Cleaning:** Xử lý missing values, outliers
- **NLP:** Natural Language Processing
- **Machine Learning:** Regression, Clustering
- **Visualization:** 7+ loại biểu đồ khác nhau


##  GHI CHÚ

- Tất cả biểu đồ được lưu trong thư mục `charts/`
- Dữ liệu đã được làm sạch và chuẩn hóa
- Code có comment tiếng Việt để dễ hiểu
- Notebooks có thể chạy độc lập

##  MỤC TIÊU HỌC TẬP

Dự án này giúp sinh viên:
-  Thực hành EDA và Data Cleaning
-  Áp dụng Machine Learning cơ bản
-  Sử dụng các thư viện Python phổ biến
-  Trực quan hóa dữ liệu hiệu quả
-  Phân tích thống kê và NLP
-  Viết báo cáo phân tích chuyên nghiệp

