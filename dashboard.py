import streamlit as st
import os
import pandas as pd
from datetime import datetime
import glob
from config.settings import GOOGLE_ANALYTICS_ID

# Page Config
st.set_page_config(page_title="Gaia Dashboard", layout="wide")

st.title("Gaia Project Dashboard")

# Sidebar
st.sidebar.header("Settings")
ga_id = st.sidebar.text_input("GA4 Measurement ID", value=GOOGLE_ANALYTICS_ID)

# Metrics
st.markdown("### 📊 Project Overview")
docs_dir = "docs"
files = glob.glob(os.path.join(docs_dir, "article_*.html"))
total_articles = len(files)

col1, col2, col3 = st.columns(3)
col1.metric("Total Articles", total_articles)
col1.caption(f"Last Index Update: {datetime.fromtimestamp(os.path.getmtime(os.path.join(docs_dir, 'index.html'))).strftime('%Y-%m-%d %H:%M') if os.path.exists(os.path.join(docs_dir, 'index.html')) else 'N/A'}")

# Analytics Link
st.markdown("---")
st.markdown("### 📈 Google Analytics")

if "G-" not in ga_id or "XXXX" in ga_id:
    st.warning("GA4 Measurement ID is not properly configured. Please update `config/settings.py`.")
else:
    st.success(f"Tracking ID Active: `{ga_id}`")
    st.markdown(f"""
    Access your detailed traffic reports here:
    [**Google Analytics Dashboard**](https://analytics.google.com/analytics/web/)
    """)

# Recent Articles
st.markdown("---")
st.markdown("### 📝 Recent Articles")

article_data = []
for f in sorted(files, key=os.path.getmtime, reverse=True)[:10]:
    title = "Unknown Title"
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            import re
            m = re.search(r'<title>(.*?)</title>', content)
            if m:
                title = m.group(1)
    except:
        pass
    
    article_data.append({
        "Date": datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M'),
        "Title": title,
        "Filename": os.path.basename(f)
    })

if article_data:
    df = pd.DataFrame(article_data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No articles found.")

# Quick Actions
st.markdown("---")
st.markdown("### 🚀 Quick Actions")
if st.button("Open Blog Index"):
    import webbrowser
    webbrowser.open(f"file:///{os.path.abspath(os.path.join(docs_dir, 'index.html'))}")
