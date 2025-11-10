import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.ensemble import RandomForestRegressor
import re
from collections import Counter

# Cấu hình trang
st.set_page_config(page_title="Data Jobs Analysis Dashboard", layout="wide", page_icon="📊")

# Set seaborn theme như trong notebook
sns.set_theme(style="whitegrid")

# CSS để làm đẹp dashboard
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Cache dữ liệu để tăng tốc
@st.cache_data
def load_data():
    CLEAN_PATH = r"D:\Truc_quan\Data_Jobs_Clean.csv"
    df = pd.read_csv(CLEAN_PATH, encoding="utf-8")
    return df

# Load dữ liệu
df = load_data()

# Header
st.title("📊 Dashboard Phân Tích Thị Trường Việc Làm Data")
st.markdown("---")

# Sidebar - Bộ lọc
st.sidebar.header("🔍 Bộ Lọc Dữ Liệu")

# Lọc theo Location
if 'Location' in df.columns:
    locations = ['Tất cả'] + sorted(df['Location'].unique().tolist())
    selected_location = st.sidebar.selectbox("Chọn địa điểm:", locations)
    
    if selected_location != 'Tất cả':
        df_filtered = df[df['Location'] == selected_location].copy()
    else:
        df_filtered = df.copy()
else:
    df_filtered = df.copy()

# Lọc theo khoảng lương
if 'Est_Salary' in df.columns:
    min_salary = int(df['Est_Salary'].min())
    max_salary = int(df['Est_Salary'].max())
    salary_range = st.sidebar.slider(
        "Khoảng lương (USD):",
        min_salary, max_salary,
        (min_salary, max_salary)
    )
    df_filtered = df_filtered[
        (df_filtered['Est_Salary'] >= salary_range[0]) &
        (df_filtered['Est_Salary'] <= salary_range[1])
    ]

# Lọc theo kinh nghiệm
if 'Min_YOE' in df.columns:
    min_yoe = int(df['Min_YOE'].min())
    max_yoe = int(df['Min_YOE'].max())
    yoe_range = st.sidebar.slider(
        "Số năm kinh nghiệm:",
        min_yoe, max_yoe,
        (min_yoe, max_yoe)
    )
    df_filtered = df_filtered[
        (df_filtered['Min_YOE'] >= yoe_range[0]) &
        (df_filtered['Min_YOE'] <= yoe_range[1])
    ]

st.sidebar.markdown(f"**Số lượng công việc:** {len(df_filtered)}")

# Tab navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Tổng Quan", "💼 Phân Tích Vai Trò", "📝 Kỹ Năng (NLP)", "🎯 Clustering", "📊 Tương Quan & Feature Importance"])

# ============ TAB 1: TỔNG QUAN ============
with tab1:
    st.header("📈 Thống Kê Tổng Quan")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Tổng số công việc", f"{len(df_filtered):,}")
    
    with col2:
        if 'Est_Salary' in df_filtered.columns:
            avg_salary = df_filtered['Est_Salary'].mean()
            st.metric("Lương trung bình", f"${avg_salary:,.0f}")
    
    with col3:
        if 'Min_YOE' in df_filtered.columns:
            avg_yoe = df_filtered['Min_YOE'].mean()
            st.metric("Kinh nghiệm TB", f"{avg_yoe:.1f} năm")
    
    with col4:
        if 'Location' in df_filtered.columns:
            num_locations = df_filtered['Location'].nunique()
            st.metric("Số địa điểm", num_locations)
    
    st.markdown("---")
    
    # Biểu đồ chuyên sâu từ notebook - Boxplot và Violinplot
    st.subheader("1. Biểu đồ hộp (Boxplot): Phân bố lương theo Role")
    role_cols = [c for c in ["Data_Engineer","Data_Analyst","Data_Scientist",
                              "Business_Analyst","Business_Intelligence",
                              "Combined_role","Others"] if c in df_filtered.columns]
    
    if role_cols and 'Est_Salary' in df_filtered.columns:
        role_df = df_filtered.melt(
            id_vars=["Est_Salary"],
            value_vars=role_cols,
            var_name="Role",
            value_name="Flag"
        ).query("Flag==1")
        
        fig = px.box(
            role_df,
            x='Role',
            y='Est_Salary',
            title='Biểu đồ hộp - Phân bố lương theo Role',
            labels={'Est_Salary': 'Lương (USD)', 'Role': 'Vai trò'}
        )
        fig.update_layout(height=400)
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Violinplot - Lương theo Location
    st.subheader("2. Biểu đồ violin (Violinplot): Lương theo Location")
    if 'Location' in df_filtered.columns and 'Est_Salary' in df_filtered.columns:
        fig = px.violin(
            df_filtered,
            x='Location',
            y='Est_Salary',
            box=True,
            title='Biểu đồ violin - Lương theo Location',
            labels={'Est_Salary': 'Lương (USD)', 'Location': 'Địa điểm'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Lương theo Min_YOE (bin) - Boxplot
    st.subheader("3. Biểu đồ hộp (Boxplot): Lương theo nhóm kinh nghiệm")
    if 'Min_YOE' in df_filtered.columns and 'Est_Salary' in df_filtered.columns:
        df_with_bin = df_filtered.copy()
        df_with_bin['YOE_Bin'] = pd.cut(
            df_with_bin['Min_YOE'],
            bins=[-0.1,1,3,5,10,100],
            labels=["0-1","1-3","3-5","5-10","10+"]
        )
        
        fig = px.box(
            df_with_bin,
            x='YOE_Bin',
            y='Est_Salary',
            title='Biểu đồ hộp - Lương theo nhóm kinh nghiệm',
            labels={'YOE_Bin': 'Nhóm kinh nghiệm (năm)', 'Est_Salary': 'Lương (USD)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Pairplot - Mối quan hệ giữa Min_YOE và Est_Salary
    st.subheader("4. Biểu đồ phân tán (Scatter Plot): Mối quan hệ Kinh nghiệm và Lương")
    if 'Min_YOE' in df_filtered.columns and 'Est_Salary' in df_filtered.columns:
        fig = px.scatter(
            df_filtered,
            x='Min_YOE',
            y='Est_Salary',
            trendline="ols",
            title='Biểu đồ phân tán - Mối quan hệ giữa Kinh nghiệm và Lương',
            labels={'Min_YOE': 'Số năm kinh nghiệm', 'Est_Salary': 'Lương (USD)'},
            opacity=0.6
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============ TAB 2: PHÂN TÍCH VAI TRÒ ============
with tab2:
    st.header("💼 Phân Tích Theo Vai Trò")
    
    # Lấy các cột vai trò
    role_cols = [c for c in ["Data_Engineer","Data_Analyst","Data_Scientist",
                              "Business_Analyst","Business_Intelligence",
                              "Combined_role","Others"] if c in df_filtered.columns]
    
    if role_cols and 'Est_Salary' in df_filtered.columns:
        # Melt dữ liệu
        role_df = df_filtered.melt(
            id_vars=["Est_Salary", "Min_YOE"],
            value_vars=role_cols,
            var_name="Role",
            value_name="Flag"
        ).query("Flag==1")
        
        # Thống kê theo vai trò
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Biểu đồ hộp: Phân bố lương theo vai trò")
            fig = px.box(
                role_df,
                x='Role',
                y='Est_Salary',
                title='Biểu đồ hộp - Phân bố lương theo vai trò',
                labels={'Est_Salary': 'Lương (USD)', 'Role': 'Vai trò'}
            )
            fig.update_layout(height=400)
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Biểu đồ tròn: Số lượng công việc")
            role_counts = role_df['Role'].value_counts().reset_index()
            role_counts.columns = ['Role', 'Count']
            
            fig = px.pie(
                role_counts,
                values='Count',
                names='Role',
                title='Biểu đồ tròn - Phân bố vai trò'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Bảng thống kê chi tiết
        st.subheader("Thống kê chi tiết theo vai trò")
        role_stats = role_df.groupby('Role').agg({
            'Est_Salary': ['mean', 'median', 'min', 'max'],
            'Min_YOE': 'mean'
        }).round(2)
        role_stats.columns = ['Lương TB', 'Lương trung vị', 'Lương min', 'Lương max', 'Kinh nghiệm TB']
        st.dataframe(role_stats, use_container_width=True)
        
        # Lương theo nhóm kinh nghiệm (YOE_Bin) - Như trong notebook
        st.subheader("Biểu đồ hộp: Lương theo nhóm kinh nghiệm")
        df_with_bin = df_filtered.copy()
        df_with_bin['YOE_Bin'] = pd.cut(
            df_with_bin['Min_YOE'], 
            bins=[-0.1,1,3,5,10,100], 
            labels=["0-1","1-3","3-5","5-10","10+"]
        )
        
        fig = px.box(
            df_with_bin,
            x='YOE_Bin',
            y='Est_Salary',
            title='Biểu đồ hộp - Lương theo nhóm kinh nghiệm',
            labels={'YOE_Bin': 'Nhóm kinh nghiệm (năm)', 'Est_Salary': 'Lương (USD)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# ============ TAB 3: PHÂN TÍCH KỸ NĂNG (NLP) ============
with tab3:
    st.header("📝 Phân Tích Kỹ Năng (NLP trên JD_Trans)")
    
    text_series = df_filtered.get('JD_Trans')
    if text_series is not None and len(text_series) > 0:
        # Tiền xử lý văn bản như trong notebook
        corpus = text_series.fillna('').astype(str).str.lower()
        corpus = corpus.str.replace(r"[^a-z0-9\s\+\.#]", " ", regex=True)
        
        # Đếm tần suất kỹ năng
        skills = ['python','sql','power bi','excel','tableau','airflow','spark',
                  'aws','gcp','azure','java','docker','kafka','hadoop']
        counts = {}
        for skill in skills:
            pattern = re.compile(rf"\b{re.escape(skill)}\b")
            counts[skill] = corpus.apply(lambda x: len(pattern.findall(x))).sum()
        
        skills_df = pd.DataFrame(
            sorted(counts.items(), key=lambda x: x[1], reverse=True),
            columns=['skill','count']
        )
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Biểu đồ cột: Tần suất kỹ năng trong JD")
            fig = px.bar(
                skills_df,
                x='skill',
                y='count',
                title='Biểu đồ cột - Tần suất kỹ năng trong JD_Trans',
                labels={'skill': 'Kỹ năng', 'count': 'Số lần xuất hiện'},
                color='count',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=500)
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Top 10 kỹ năng")
            st.dataframe(skills_df.head(10), use_container_width=True, hide_index=True)
            
            st.info(f"""
            📊 **Phân tích:**
            - Kỹ năng phổ biến nhất: **{skills_df.iloc[0]['skill']}** ({skills_df.iloc[0]['count']} lần)
            - Tổng số lần xuất hiện: **{skills_df['count'].sum()}**
            """)
    else:
        st.warning("Không có dữ liệu JD_Trans để phân tích kỹ năng")

# ============ TAB 4: CLUSTERING ============
with tab4:
    st.header("🎯 Phân Nhóm Công Việc (Clustering)")
    
    if 'Min_YOE' in df_filtered.columns and 'Est_Salary' in df_filtered.columns:
        # Chuẩn bị dữ liệu
        cluster_features = ['Min_YOE', 'Est_Salary']
        cluster_data = df_filtered[cluster_features].copy()
        
        # Chuẩn hóa
        scaler = StandardScaler()
        cluster_data_scaled = scaler.fit_transform(cluster_data)
        
        # Chọn số cluster
        n_clusters = st.slider("Chọn số nhóm:", 2, 6, 3)
        
        # Thực hiện clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(cluster_data_scaled)
        
        df_clustered = df_filtered.copy()
        df_clustered['Cluster'] = cluster_labels
        
        # Silhouette score
        silhouette_avg = silhouette_score(cluster_data_scaled, cluster_labels)
        st.info(f"📊 Silhouette Score: {silhouette_avg:.3f} (Chất lượng phân nhóm)")
        
        # Elbow Method và Silhouette Score - Như trong notebook
        st.subheader("Biểu đồ đường: Phân tích số cluster tối ưu")
        
        inertias = []
        silhouette_scores = []
        K_range = range(2, 8)
        
        for k in K_range:
            kmeans_temp = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans_temp.fit(cluster_data_scaled)
            inertias.append(kmeans_temp.inertia_)
            silhouette_scores.append(silhouette_score(cluster_data_scaled, kmeans_temp.labels_))
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(K_range), y=inertias, mode='lines+markers', marker=dict(color='blue')))
            fig.update_layout(
                title='Biểu đồ đường - Elbow Method',
                xaxis_title='Số clusters (k)',
                yaxis_title='Inertia',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_b:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(K_range), y=silhouette_scores, mode='lines+markers', marker=dict(color='red')))
            fig.update_layout(
                title='Biểu đồ đường - Silhouette Score',
                xaxis_title='Số clusters (k)',
                yaxis_title='Silhouette Score',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Biểu đồ phân tán: Kết quả phân nhóm")
            fig = px.scatter(
                df_clustered,
                x='Min_YOE',
                y='Est_Salary',
                color='Cluster',
                title='Biểu đồ phân tán - Clustering Jobs',
                labels={'Min_YOE': 'Kinh nghiệm (năm)', 'Est_Salary': 'Lương (USD)'},
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Đặc điểm từng nhóm")
            for i in range(n_clusters):
                cluster_data_i = df_clustered[df_clustered['Cluster'] == i]
                with st.expander(f"Cluster {i} ({len(cluster_data_i)} công việc)", expanded=True):
                    st.write(f"**Lương trung bình:** ${cluster_data_i['Est_Salary'].mean():,.0f}")
                    st.write(f"**Kinh nghiệm trung bình:** {cluster_data_i['Min_YOE'].mean():.1f} năm")
                    
                    if 'Job_Title' in cluster_data_i.columns:
                        top_jobs = cluster_data_i['Job_Title'].value_counts().head(3)
                        st.write("**Top 3 Job phổ biến:**")
                        for job, count in top_jobs.items():
                            st.write(f"  • {job}: {count}")

# ============ TAB 5: TƯƠNG QUAN & FEATURE IMPORTANCE ============
with tab5:
    st.header("📊 Phân Tích Tương Quan & Tầm Quan Trọng Biến")
    
    # PHẦN 1: TƯƠNG QUAN
    st.subheader("1. Biểu đồ nhiệt (Heatmap): Ma trận tương quan")
    numeric_cols = [c for c in ['Min_YOE', 'Est_Salary', 'L1', 'MinL'] if c in df_filtered.columns]
    
    if len(numeric_cols) >= 2:
        correlation_matrix = df_filtered[numeric_cols].corr()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.imshow(
                correlation_matrix,
                text_auto='.3f',
                aspect='auto',
                color_continuous_scale='RdBu_r',
                color_continuous_midpoint=0,
                title='Biểu đồ nhiệt - Ma trận tương quan giữa các biến số'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Tương quan với Est_Salary:**")
            if 'Est_Salary' in correlation_matrix.columns:
                salary_corr = correlation_matrix['Est_Salary'].drop('Est_Salary').sort_values(key=abs, ascending=False)
                
                for var, corr in salary_corr.items():
                    st.write(f"• **{var}**: {corr:.3f}")
    
    st.markdown("---")
    
    # PHẦN 2: FEATURE IMPORTANCE (Random Forest)
    st.subheader("2. Biểu đồ thanh ngang (Barplot): Tầm quan trọng của các biến")
    
    if 'Est_Salary' in df_filtered.columns and 'Min_YOE' in df_filtered.columns:
        # Chuẩn bị dữ liệu như trong notebook
        feature_cols = ['Min_YOE']
        if 'Location' in df_filtered.columns:
            feature_cols.append('Location')
        
        X_simple = df_filtered[feature_cols].copy()
        
        # One-hot encoding cho Location
        if 'Location' in X_simple.columns:
            X_encoded = pd.get_dummies(X_simple, columns=['Location'])
        else:
            X_encoded = X_simple
        
        y_simple = df_filtered['Est_Salary']
        
        # Random Forest
        rf_model = RandomForestRegressor(n_estimators=50, random_state=42)
        rf_model.fit(X_encoded, y_simple)
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'Biến': X_encoded.columns,
            'Tầm quan trọng': rf_model.feature_importances_
        }).sort_values('Tầm quan trọng', ascending=False)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = px.bar(
                feature_importance,
                x='Tầm quan trọng',
                y='Biến',
                orientation='h',
                title='Biểu đồ thanh - Tầm quan trọng của các biến (Random Forest)',
                color='Tầm quan trọng',
                color_continuous_scale='Blues'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Chi tiết:**")
            st.dataframe(feature_importance, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # PHẦN 3: KẾT LUẬN
    st.subheader("3. Kết luận")
    
    if len(numeric_cols) >= 2 and 'Est_Salary' in correlation_matrix.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"""
            **Phân tích tương quan:**
            - Biến có tương quan mạnh nhất với lương: **{salary_corr.index[0]}**
            - Mức tương quan: **{salary_corr.iloc[0]:.3f}**
            """)
        
        with col2:
            if 'feature_importance' in locals():
                st.success(f"""
                **Tầm quan trọng biến:**
                - Biến quan trọng nhất: **{feature_importance.iloc[0]['Biến']}**
                - Mức quan trọng: **{feature_importance.iloc[0]['Tầm quan trọng']:.3f}**
                """)
    
    # Scatter plot với trendline
    if len(numeric_cols) >= 2:
        st.subheader("4. Biểu đồ phân tán (Scatter Plot): Mối quan hệ giữa các biến")
        col_x = st.selectbox("Chọn biến X:", numeric_cols, index=0)
        col_y = st.selectbox("Chọn biến Y:", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
        
        if col_x != col_y:
            fig = px.scatter(
                df_filtered,
                x=col_x,
                y=col_y,
                trendline="ols",
                title=f'Biểu đồ phân tán - Mối quan hệ giữa {col_x} và {col_y}',
                opacity=0.6
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>📊 Dashboard Phân Tích Dữ Liệu Việc Làm | Made with Streamlit</p>
</div>
""", unsafe_allow_html=True)
