import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load data
who = pd.read_csv("WHO.csv", parse_dates=["Date_reported"])

# Calculate daily cases
who["Daily_cases"] = who.groupby("Country")["Cumulative_cases"].diff().fillna(0)

# Function to plot line chart
def line_chart(data, countries, chart_type):
    plt.figure(figsize=(10, 6))
    plt.title(f"Covid {chart_type} Cases")
    plt.xlabel("Date")
    plt.ylabel(f"{chart_type} Cases")
    plt.ticklabel_format(axis="y", style="plain")
    plt.grid(True)

    for country in countries:
        c_df = data[data["Country"] == country]
        if chart_type == "Cumulative":
            plt.plot(c_df.Date_reported, c_df.Cumulative_cases, label=country, linestyle='-', marker='o')
        elif chart_type == "Daily":
            plt.plot(c_df.Date_reported, c_df.Daily_cases, label=country, linestyle='-', marker='o')

    plt.legend()
    st.pyplot(plt)

# Streamlit app
st.title("Covid-19 Cases Visualization")

# Sidebar for country selection
selected_countries = st.sidebar.multiselect("Select Countries", who["Country"].unique())

# Sidebar for date range selection
date_range = st.sidebar.date_input("Select Date Range", [who["Date_reported"].min(), who["Date_reported"].max()])

# Convert date_range to datetime64[ns]
date_range = [pd.to_datetime(date) for date in date_range]

# Sidebar for chart type selection
chart_type = st.sidebar.radio("Select Chart Type", ["Cumulative", "Daily"])

# Filter data based on user selection
filtered_data = who[(who["Country"].isin(selected_countries)) & (who["Date_reported"] >= date_range[0]) & (who["Date_reported"] <= date_range[1])]

# Display line chart based on selected countries, date range, and chart type
if selected_countries:
    line_chart(filtered_data, selected_countries, chart_type)
else:
    st.warning("Please select at least one country.")

# Display the data table
st.dataframe(filtered_data.head(10))
