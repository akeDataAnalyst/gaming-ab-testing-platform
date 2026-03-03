#!/usr/bin/env python
# coding: utf-8

# In[3]:


import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Gaming A/B Test Dashboard", layout="wide")

st.title("🎮 Gaming A/B Test Dashboard")
st.markdown("**Variant B (Streak Rewards) vs Variant A (Standard Rewards)**")

# Caching 
@st.cache_resource
def get_duckdb_connection():
    con = duckdb.connect(':memory:')
    con.execute("CREATE OR REPLACE TABLE fact AS SELECT * FROM read_parquet('../data/processed_data/fact_user_metrics.parquet')")
    con.execute("CREATE OR REPLACE TABLE cohort AS SELECT * FROM read_parquet('../data/processed_data/cohort_daily.parquet')")
    return con


@st.cache_data
def load_fact(_con):
    return _con.sql("SELECT * FROM fact").df()


@st.cache_data
def load_cohort(_con):
    return _con.sql("SELECT * FROM cohort ORDER BY install_day DESC, variant").df()


# Load once
con = get_duckdb_connection()
df_fact = load_fact(con)
df_cohort = load_cohort(con)

# Sidebar filters 
with st.sidebar:
    st.header("Filters")
    
    min_date = df_cohort['install_day'].min().date()
    max_date = df_cohort['install_day'].max().date()
    
    date_range = st.date_input(
        "Cohort date range",
        value=(max_date - pd.Timedelta(days=120), max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start, end = date_range
        df_filtered = df_cohort[
            (df_cohort['install_day'] >= pd.to_datetime(start)) &
            (df_cohort['install_day'] <= pd.to_datetime(end))
        ]
    else:
        df_filtered = df_cohort.copy()
    
    kpi = st.selectbox(
        "Focus KPI",
        ['retention_d1_pct', 'retention_d7_pct', 'retention_d30_pct',
         'avg_revenue', 'avg_sessions_d1', 'avg_levels_d7', 'payer_conversion_pct'],
        index=1
    )

# Main content

col_left, col_right = st.columns([3, 2])

with col_left:
    # Retention curves
    st.subheader("Retention Curves")
    melt_df = df_filtered.melt(
        id_vars=['install_day', 'variant'],
        value_vars=['retention_d1_pct', 'retention_d7_pct', 'retention_d30_pct'],
        var_name='Retention Type',
        value_name='Rate %'
    )
    melt_df['Retention Type'] = melt_df['Retention Type'].str.replace('_pct', '').str.replace('retention_', 'D')

    fig_lines = px.line(
        melt_df,
        x='install_day',
        y='Rate %',
        color='variant',
        facet_col='Retention Type',
        title='Retention by Variant',
        markers=True
    )
    fig_lines.update_layout(hovermode='x unified', height=500)
    st.plotly_chart(fig_lines, use_container_width=True)

    # Uplift bar
    st.subheader("Daily Uplift")
    pivot = df_filtered.pivot_table(index='install_day', columns='variant', values=kpi)
    pivot['uplift_%'] = (pivot['B'] / pivot['A'] - 1) * 100
    uplift_df = pivot[['uplift_%']].reset_index().dropna()
    uplift_df = uplift_df.sort_values('install_day', ascending=False)

    fig_bar = px.bar(
        uplift_df,
        x='install_day',
        y='uplift_%',
        title=f"Uplift on {kpi.replace('_pct','').replace('avg_','')}",
        color='uplift_%',
        color_continuous_scale='RdYlGn',
        text_auto='.1f'
    )
    fig_bar.update_layout(height=500, xaxis_tickangle=-45)
    fig_bar.add_hline(y=0, line_dash="dash", line_color="gray")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Summary Table")
    summary = df_filtered.groupby('variant').mean(numeric_only=True).round(2)
    st.dataframe(summary, use_container_width=True)

    if 'A' in summary.index and 'B' in summary.index:
        d7_uplift = (summary.loc['B', 'retention_d7_pct'] / summary.loc['A', 'retention_d7_pct'] - 1) * 100
        rev_uplift = (summary.loc['B', 'avg_revenue'] / summary.loc['A', 'avg_revenue'] - 1) * 100
        
        st.metric("D7 Retention Uplift", f"{d7_uplift:.1f}%")
        st.metric("Revenue Uplift", f"{rev_uplift:.1f}%")

st.markdown("---")
st.caption("Developed by Aklilu Abera | 100k-user A/B test | Built with Streamlit + DuckDB")


# In[ ]:




