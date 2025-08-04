import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="📱 iPhone Ratings Dashboard", layout="wide")
st.title("📱 iPhone Ratings & Popularity in India")

# File upload
uploaded_file = st.file_uploader("Upload your iPhone CSV file", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    # Sidebar filters
    st.sidebar.header("🔍 Filter Options")

    models = st.sidebar.multiselect(
        "Select iPhone Models:",
        options=data['Product Name'].unique(),
        default=data['Product Name'].unique()
    )

    rating_range = st.sidebar.slider(
        "Select Star Rating Range:",
        min_value=float(data['Star Rating'].min()),
        max_value=float(data['Star Rating'].max()),
        value=(float(data['Star Rating'].min()), float(data['Star Rating'].max()))
    )

    filtered_data = data[
        (data['Product Name'].isin(models)) &
        (data['Star Rating'] >= rating_range[0]) &
        (data['Star Rating'] <= rating_range[1])
    ]

    st.subheader("📋 Filtered Dataset")
    st.dataframe(filtered_data)

    # Top 10 highest-rated iPhones
    st.subheader("🏆 Top 10 Highest Rated iPhones")
    top_10 = filtered_data.sort_values(by='Star Rating', ascending=False).head(10)
    st.table(top_10[['Product Name', 'Star Rating']])

    # Two columns for smaller charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Distribution of Star Ratings")
        fig1, ax1 = plt.subplots(figsize=(3.5, 2))
        sns.histplot(filtered_data['Star Rating'], bins=10, kde=True, ax=ax1, color='skyblue')
        ax1.set_title("Star Rating Distribution")
        st.pyplot(fig1)

    with col2:
        st.subheader("🧩 Star Rating Share (Pie Chart)")
        rating_counts = filtered_data['Star Rating'].value_counts().sort_index()
        fig3, ax3 = plt.subplots(figsize=(3, 3))
        ax3.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=140)
        ax3.axis('equal')
        st.pyplot(fig3)

    # Average Rating by Model
    st.subheader("📉 Average Rating by iPhone Model")
    avg_rating = (
        filtered_data.groupby('Product Name')['Star Rating']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    sns.barplot(x=avg_rating.values, y=avg_rating.index, ax=ax2, palette="viridis")
    ax2.set_xlabel("Average Star Rating")
    ax2.set_ylabel("Product Name")
    st.pyplot(fig2)

    # Most Common Models
    st.subheader("📊 Most Common iPhone Models")
    common_models = filtered_data['Product Name'].value_counts().head(10)
    fig4, ax4 = plt.subplots(figsize=(5, 3))
    sns.barplot(x=common_models.values, y=common_models.index, ax=ax4, palette="Set2")
    ax4.set_title("Top 10 Most Frequent iPhone Models")
    st.pyplot(fig4)

else:
    st.info("👆 Upload a CSV file to get started.")
