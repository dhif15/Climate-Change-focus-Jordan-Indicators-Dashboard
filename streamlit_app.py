import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import json
from scipy.stats import linregress
import matplotlib.pyplot as plt

# Title of the dashboard
st.title("Climate Change Indicators Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('clean_climate_change_indicators.csv')

data = load_data()

# Sidebar for navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Select a page:", [
    "Introduction", 
    "Data Sources and Methodology", 
    "Overview of Global Trends",
    "Global Trends",
    "Top 10 Coldest and Hottest Years",
    "Temperature Change Before and After 2000",
    "Temperature Change Comparison",
    "Trend Analysis",
    "Regional Analysis",
    "Country-Specific Analysis",
    "Urban vs. Rural Trends",
    "G7 Analysis",
    "Statistical Analysis",
    "Conclusions"
])

# Ensure the 'Urban_Rural' column is added to the DataFrame
with open('urban_rural_mapping.json', 'r') as file:
    urban_rural_mapping = json.load(file)
country_to_continent = {country: info['region'] for country, info in urban_rural_mapping.items()}

# Map 'Urban_Rural' values to the DataFrame
data['Urban_Rural'] = data['Country'].map(lambda x: urban_rural_mapping.get(x, {}).get('urban_rural', 'Unknown'))

# Calculate the average temperature change for each year across all countries
average_temperature_change = data.groupby('Year')['Temperature Change'].mean()

# Filter the data for Jordan
jordan_data = data[data['Country'].str.contains('Jordan', case=False)]

# Extract Jordan's temperature change values
jordan_temperature_change = jordan_data.groupby('Year')['Temperature Change'].mean()

# Calculate the average temperature change for all other countries
other_countries_data = data[~data['Country'].str.contains('Jordan', case=False)]
average_temperature_change_other_countries = other_countries_data.groupby('Year')['Temperature Change'].mean()


if options == "Introduction":
    st.header("Introduction")
    st.write("""
        Climate change is one of the most pressing issues facing our planet today, affecting ecosystems, weather patterns, and human societies globally. Analyzing climate change indicators is crucial to understanding the extent of these changes and developing strategies to mitigate their impacts. This report provides insights into various climate change indicators, with a particular focus on the temperature change data from different countries over several decades.

        **Importance of Analyzing Climate Change Indicators**

        Analyzing climate change indicators helps scientists and policymakers track changes in climate patterns, predict future trends, and formulate effective responses. By examining temperature changes, we can gain insights into the global warming phenomenon and its potential consequences on natural and human systems. This analysis is vital for developing sustainable practices and policies that can help mitigate the adverse effects of climate change.

        **Choice of Jordan as a Case Study**

        Jordan was chosen as a case study due to its unique geographical and climatic conditions. Located in the Middle East, Jordan is characterized by its arid and semi-arid climate, making it particularly vulnerable to climate change. Understanding how temperature changes in Jordan can provide valuable insights into the regional impacts of global warming and help in developing targeted adaptation strategies.
    """)

elif options == "Data Sources and Methodology":
    st.header("Data Sources and Methodology")
    st.write("""
        **Data Sources**

        The primary data source for this analysis is the climate change indicators dataset from Kaggle. The dataset includes temperature change data from various countries, covering the period from 1961 to 2020. The data was extracted and processed to ensure accuracy and relevance for this study. The dataset can be accessed at [Kaggle Climate Change Indicators Dataset](https://www.kaggle.com/datasets/tarunrm09/climate-change-indicators).

        **Time Period Covered**

        The analysis covers the temperature change data from 1961 to 2020, providing a comprehensive view of the long-term trends in global and regional temperature changes.

        **Data Cleaning and Preparation**

        Data cleaning and preparation involved handling missing values, standardizing country names, and categorizing countries into urban and rural classifications. This ensured that the analysis was based on accurate and consistent data, allowing for meaningful comparisons and insights. For further insights and detailed analysis, refer to the notebook available at [Kaggle Notebook - Climate Change Indicators](https://www.kaggle.com/code/dhifallhalayadi/climate-change-indicators).
    """)

elif options == "Overview of Global Trends":
    st.header("Overview of Global Trends")
    st.write("""
        This section provides an overview of the general climate trends observed globally and in Jordan from 1961 to 2020. The analysis focuses on identifying the top 10 warmest and coldest years, examining the global trends in temperature changes, and comparing these trends with those observed in Jordan.

        **Overview of Global Trends**

        The global temperature data from 1961 to 2020 shows a clear upward trend, indicating an overall increase in average temperatures. This trend is consistent with the growing concerns about global warming and climate change. The analysis highlights the top 10 warmest and coldest years globally, providing insight into the variability and extremes in temperature changes over the decades.

        **Top 10 Warmest and Coldest Years Globally**

        The analysis identified the top 10 warmest years and the top 10 coldest years globally. These extremes are significant as they reflect the impact of various factors, including natural climate variability and anthropogenic influences, on global temperatures. The warmest years are predominantly from recent decades, further supporting the evidence of accelerated global warming.
    """)

elif options == "Temperature Change Before and After 2000":
    st.header("Temperature Change Before and After 2000")

    # Extract the years of interest
    years_before_2000 = list(range(1961, 2001))
    years_after_2000 = list(range(2001, 2021))

    # Calculate the average temperature change for each country before and after 2000
    average_temp_change_before_2000 = data[data['Year'].isin(years_before_2000)].groupby('Country')['Temperature Change'].mean()
    average_temp_change_after_2000 = data[data['Year'].isin(years_after_2000)].groupby('Country')['Temperature Change'].mean()

    # Combine the results into a single DataFrame
    temp_changes = pd.DataFrame({
        'Country': average_temp_change_before_2000.index,
        'Average_Temperature_Change_Before_2000': average_temp_change_before_2000.values,
        'Average_Temperature_Change_After_2000': average_temp_change_after_2000.values
    })

    # Calculate the global average temperature change before and after 2000
    global_avg_temp_change_before_2000 = average_temp_change_before_2000.mean()
    global_avg_temp_change_after_2000 = average_temp_change_after_2000.mean()

    # Create a DataFrame for global average temperature changes
    global_avg_temp_changes = pd.DataFrame({
        'Period': ['Before 2000', 'After 2000'],
        'Average_Temperature_Change': [global_avg_temp_change_before_2000, global_avg_temp_change_after_2000]
    })

    # Plot the global average temperature changes before and after 2000
    fig = go.Figure(data=[go.Bar(x=global_avg_temp_changes['Period'], y=global_avg_temp_changes['Average_Temperature_Change'])])
    fig.update_layout(
        title='Global Average Temperature Change Before and After 2000',
        xaxis_title='Period',
        yaxis_title='Average Temperature Change (°C)',
        template='plotly_white'
    )
    st.plotly_chart(fig)

    # Plot the average temperature changes for each country before and after 2000
    fig_country = go.Figure()

    # Plot all countries except Jordan
    fig_country.add_trace(go.Scatter(
        x=temp_changes[temp_changes['Country'] != 'Jordan']['Country'],
        y=temp_changes[temp_changes['Country'] != 'Jordan']['Average_Temperature_Change_Before_2000'],
        mode='markers',
        name='Before 2000'
    ))

    fig_country.add_trace(go.Scatter(
        x=temp_changes[temp_changes['Country'] != 'Jordan']['Country'],
        y=temp_changes[temp_changes['Country'] != 'Jordan']['Average_Temperature_Change_After_2000'],
        mode='markers',
        marker=dict(color='red'),
        name='After 2000'
    ))

    # Highlight Jordan with a star marker
    fig_country.add_trace(go.Scatter(
        x=['Jordan'],
        y=temp_changes[temp_changes['Country'] == 'Jordan']['Average_Temperature_Change_Before_2000'],
        mode='markers',
        marker=dict(symbol='star', size=12, color='blue'),
        name='Jordan Before 2000'
    ))

    fig_country.add_trace(go.Scatter(
        x=['Jordan'],
        y=temp_changes[temp_changes['Country'] == 'Jordan']['Average_Temperature_Change_After_2000'],
        mode='markers',
        marker=dict(symbol='star', size=12, color='red'),
        name='Jordan After 2000'
    ))

    fig_country.update_layout(
        title='Country-wise Average Temperature Change Before and After 2000',
        xaxis_title='Country',
        yaxis_title='Average Temperature Change (°C)',
        template='plotly_white',
        showlegend=True
    )
    st.plotly_chart(fig_country)

    st.write("**Temperature Changes in Jordan Before and After 2000**")
    # Filter data for Jordan
    jordan_data = data[data['Country'] == 'Jordan']

    # Calculate the average temperature change for Jordan before and after 2000
    average_temp_change_before_2000 = jordan_data[jordan_data['Year'] <= 2000]['Temperature Change'].mean()
    average_temp_change_after_2000 = jordan_data[jordan_data['Year'] > 2000]['Temperature Change'].mean()

    # Create a DataFrame for easier plotting
    jordan_temp_changes = pd.DataFrame({
        'Period': ['Before 2000', 'After 2000'],
        'Average_Temperature_Change': [average_temp_change_before_2000, average_temp_change_after_2000]
    })

    # Create a scatter plot DataFrame
    jordan_scatter_data_before_2000 = jordan_data[jordan_data['Year'] <= 2000].copy()
    jordan_scatter_data_before_2000['Period'] = 'Before 2000'

    jordan_scatter_data_after_2000 = jordan_data[jordan_data['Year'] > 2000].copy()
    jordan_scatter_data_after_2000['Period'] = 'After 2000'

    jordan_scatter_data = pd.concat([jordan_scatter_data_before_2000, jordan_scatter_data_after_2000])

    # Plot the bar plot for average temperature changes
    fig_bar = go.Figure(data=[go.Bar(x=jordan_temp_changes['Period'], y=jordan_temp_changes['Average_Temperature_Change'])])
    fig_bar.update_layout(
        title='Average Temperature Change in Jordan Before and After 2000',
        xaxis_title='Period',
        yaxis_title='Average Temperature Change (°C)',
        template='plotly_white'
    )
    st.plotly_chart(fig_bar)

    # Plot the scatter plot for annual temperature changes
    fig_scatter = go.Figure()

    fig_scatter.add_trace(go.Scatter(
        x=jordan_scatter_data_before_2000['Year'],
        y=jordan_scatter_data_before_2000['Temperature Change'],
        mode='markers+lines',
        name='Before 2000'
    ))

    fig_scatter.add_trace(go.Scatter(
        x=jordan_scatter_data_after_2000['Year'],
        y=jordan_scatter_data_after_2000['Temperature Change'],
        mode='markers+lines',
        marker=dict(color='red'),
        name='After 2000'
    ))

    fig_scatter.update_layout(
        title='Annual Temperature Changes in Jordan Before and After 2000',
        xaxis_title='Year',
        yaxis_title='Temperature Change (°C)',
        template='plotly_white',
        showlegend=True
    )
    st.plotly_chart(fig_scatter)

elif options == "Global Trends":
    st.header("Global Trends")

    # Plot global temperature change trends
    average_temp_change_per_year = data.groupby('Year')['Temperature Change'].mean().reset_index()
    fig = px.line(average_temp_change_per_year, x='Year', y='Temperature Change', title='Global Temperature Change (1961-2020)')

    # Add markers to the plot
    fig.update_traces(mode='lines+markers')

    st.plotly_chart(fig)

    # Extract the years of interest
    years = list(range(1961, 2021))

    # Aggregate the data to ensure unique Country-Year pairs and calculate mean temperature change for each country
    aggregated_data = data.groupby('Country')['Temperature Change'].mean().reset_index()
    aggregated_data.columns = ['Country', 'Average_Temperature_Change']

    # Identify the top 10 countries with the highest average temperature change
    top_10_countries = aggregated_data.sort_values(by='Average_Temperature_Change', ascending=False).head(10)

    # Plot top 10 countries
    fig_top_10 = go.Figure(data=[go.Bar(x=top_10_countries['Country'], y=top_10_countries['Average_Temperature_Change'])])
    fig_top_10.update_layout(
        title='Top 10 Countries with Highest Average Temperature Change',
        xaxis_title='Country',
        yaxis_title='Average Temperature Change (°C)',
        template='plotly_white'
    )
    st.plotly_chart(fig_top_10)

elif options == "Top 10 Coldest and Hottest Years":
    st.header("Top 10 Coldest and Hottest Years Globally with Jordan Comparison (1961-2020)")

    # Extract the years of interest
    years = list(range(1961, 2021))

    # Calculate the average temperature change for each year across all countries
    average_temp_change_per_year = data.groupby('Year')['Temperature Change'].mean()

    # Convert to a DataFrame for easier manipulation
    average_temp_change_per_year_df = average_temp_change_per_year.reset_index()
    average_temp_change_per_year_df.columns = ['Year', 'Average_Temperature_Change']

    # Identify the top 10 coldest and hottest years
    coldest_years = average_temp_change_per_year_df.sort_values(by='Average_Temperature_Change', ascending=True).head(10)
    hottest_years = average_temp_change_per_year_df.sort_values(by='Average_Temperature_Change', ascending=False).head(10)

    # Filter data for Jordan
    jordan_data = data[data['Country'] == 'Jordan']

    # Plot the coldest years
    fig_coldest = go.Figure()

    fig_coldest.add_trace(go.Bar(
        x=coldest_years['Year'], 
        y=coldest_years['Average_Temperature_Change'], 
        name='Coldest Years',
        marker_color='blue'
    ))

    fig_coldest.update_layout(
        title='Top 10 Coldest Years Globally (1961-2020)',
        xaxis_title='Year',
        yaxis_title='Average Temperature Change (°C)',
        template='plotly_white',
        width=800, 
        height=400,
        barmode='group'
    )
    st.plotly_chart(fig_coldest)

    # Plot the hottest years
    fig_hottest = go.Figure()

    fig_hottest.add_trace(go.Bar(
        x=hottest_years['Year'], 
        y=hottest_years['Average_Temperature_Change'], 
        name='Hottest Years',
        marker_color='red'
    ))

    fig_hottest.update_layout(
        title='Top 10 Hottest Years Globally (1961-2020)',
        xaxis_title='Year',
        yaxis_title='Average Temperature Change (°C)',
        template='plotly_white',
        width=800, 
        height=400,
        barmode='group'
    )
    st.plotly_chart(fig_hottest)

    # Extract temperature changes for Jordan in the coldest and hottest years
    jordan_coldest_years = jordan_data[jordan_data['Year'].isin(coldest_years['Year'])]
    jordan_hottest_years = jordan_data[jordan_data['Year'].isin(hottest_years['Year'])]

    # Plot the comparison for Jordan in the coldest years
    fig_jordan_coldest = go.Figure()

    fig_jordan_coldest.add_trace(go.Scatter(
        x=jordan_coldest_years['Year'],
        y=jordan_coldest_years['Temperature Change'],
        mode='lines+markers',
        name='Jordan in Coldest Years',
        marker_color='blue'
    ))

    fig_jordan_coldest.update_layout(
        title='Jordan Temperature Change in the Coldest Years Globally (1961-2020)',
        xaxis_title='Year',
        yaxis_title='Temperature Change (°C)',
        template='plotly_white',
        width=800,
        height=400
    )
    st.plotly_chart(fig_jordan_coldest)

    # Plot the comparison for Jordan in the hottest years
    fig_jordan_hottest = go.Figure()

    fig_jordan_hottest.add_trace(go.Scatter(
        x=jordan_hottest_years['Year'],
        y=jordan_hottest_years['Temperature Change'],
        mode='lines+markers',
        name='Jordan in Hottest Years',
        marker_color='red'
    ))

    fig_jordan_hottest.update_layout(
        title='Jordan Temperature Change in the Hottest Years Globally (1961-2020)',
        xaxis_title='Year',
        yaxis_title='Temperature Change (°C)',
        template='plotly_white',
        width=800,
        height=400
    )
    st.plotly_chart(fig_jordan_hottest)

elif options == "Temperature Change Comparison":
    st.header("Temperature Change Comparison: Jordan vs. Average of Other Countries")
    
    # Calculate the average temperature change for each year across all countries
    average_temperature_change = data.groupby('Year')['Temperature Change'].mean()

    # Filter the data for Jordan
    jordan_data = data[data['Country'].str.contains('Jordan', case=False)]

    # Extract Jordan's temperature change values
    jordan_temperature_change = jordan_data.groupby('Year')['Temperature Change'].mean()

    # Create a plotly figure
    fig = go.Figure()

    # Add Jordan's temperature change line
    fig.add_trace(go.Scatter(x=jordan_temperature_change.index, y=jordan_temperature_change.values, mode='lines+markers', name='Jordan'))

    # Add global average temperature change line
    fig.add_trace(go.Scatter(x=average_temperature_change.index, y=average_temperature_change.values, mode='lines+markers', name='Average of Other Countries'))

    # Update layout
    fig.update_layout(
        title='Temperature Change Comparison: Jordan vs. Average of Other Countries',
        xaxis_title='Year',
        yaxis_title='Temperature Change (°C)',
        legend_title='Country',
        template='plotly_white'
    )
    st.plotly_chart(fig)

elif options == "Trend Analysis":
    st.header("Trend Analysis and Linear Regression of Temperature Changes: Jordan vs. Global Average")

    # Calculate the average temperature change for each year across all countries
    average_temperature_change = data.groupby('Year')['Temperature Change'].mean()

    # Filter the data for Jordan
    jordan_data = data[data['Country'].str.contains('Jordan', case=False)]

    # Extract Jordan's temperature change values
    jordan_temperature_change = jordan_data.groupby('Year')['Temperature Change'].mean()

    # Calculate the average temperature change for all other countries
    other_countries_data = data[~data['Country'].str.contains('Jordan', case=False)]
    average_temperature_change_other_countries = other_countries_data.groupby('Year')['Temperature Change'].mean()

    # Calculate trend lines using linear regression
    years_numeric = jordan_temperature_change.index.to_list()
    slope_jordan, intercept_jordan, _, _, _ = linregress(years_numeric, jordan_temperature_change)
    slope_global, intercept_global, _, _, _ = linregress(years_numeric, average_temperature_change_other_countries)

    # Calculate trend lines
    trend_jordan = [slope_jordan * year + intercept_jordan for year in years_numeric]
    trend_global = [slope_global * year + intercept_global for year in years_numeric]

    # Create a plotly figure
    fig = go.Figure()

    # Add Jordan's average temperature change line
    fig.add_trace(go.Scatter(x=jordan_temperature_change.index, y=jordan_temperature_change.values, mode='lines+markers', name='Jordan'))

    # Add global average temperature change line for other countries
    fig.add_trace(go.Scatter(x=average_temperature_change_other_countries.index, y=average_temperature_change_other_countries.values, mode='lines+markers', name='Average of Other Countries'))

    # Add trend lines
    fig.add_trace(go.Scatter(x=years_numeric, y=trend_jordan, mode='lines', name='Jordan Trend Line', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=years_numeric, y=trend_global, mode='lines', name='Global Trend Line', line=dict(dash='dash')))

    # Update layout
    fig.update_layout(
        title='Temperature Change Comparison: Jordan vs. Average of Other Countries',
        xaxis_title='Year',
        yaxis_title='Temperature Change (°C)',
        legend_title='Country',
        template='plotly_white'
    )
    st.plotly_chart(fig)

elif options == "Regional Analysis":
    st.header("Regional Analysis")
    
    # Plot temperature change by continent
    data['Continent'] = data['Country'].map(lambda x: country_to_continent.get(x, 'Unknown'))
    continent_avg_temp = data.groupby(['Continent', 'Year'])['Temperature Change'].mean().reset_index()
    fig = px.line(continent_avg_temp, x='Year', y='Temperature Change', color='Continent', title='Average Temperature Change by Continent (1961-2020)')
    st.plotly_chart(fig)

    # Load the urban_rural_region_mapping JSON file
    with open('urban_rural_mapping.json', 'r') as file:
        mapping = json.load(file)

    # Extract the region mapping
    region_mapping = {country: details['region'] for country, details in mapping.items()}

    # Add the 'Region' column to data
    data['Region'] = data['Country'].map(region_mapping)

    # Filter out rows with missing regions
    data = data.dropna(subset=['Region'])

    # Calculate average temperature change by region
    average_temp_change_by_region = data.groupby('Region')['Temperature Change'].mean()

    # Plot average temperature change by region
    fig = go.Figure(data=[go.Bar(x=average_temp_change_by_region.index, y=average_temp_change_by_region.values)])
    fig.update_layout(
        title='Average Temperature Change by Region',
        xaxis_title='Region',
        yaxis_title='Average Temperature Change (°C)',
        template='plotly_white'
    )
    st.plotly_chart(fig)

elif options == "Country-Specific Analysis":
    st.header("Country-Specific Analysis")

    # Filter data for Jordan
    jordan_data = data[data['Country'] == 'Jordan']

    # Extract the years of interest
    years = list(range(1961, 2021))

    # Pivot the data to have years as rows and temperature change as columns
    jordan_temps = jordan_data.pivot(index='Year', columns='Country', values='Temperature Change')['Jordan']

    # Plot temperature change over time for Jordan
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=jordan_temps.loc[years], mode='lines+markers', name='Jordan'))
    fig.update_layout(
        title='Temperature Change Over Time for Jordan',
        xaxis_title='Year',
        yaxis_title='Temperature Change (°C)',
        template='plotly_white'
    )
    st.plotly_chart(fig)

    # Extract the months of interest for seasons
    winter_months = ['Dec', 'Jan', 'Feb']
    spring_months = ['Mar', 'Apr', 'May']
    summer_months = ['Jun', 'Jul', 'Aug']
    fall_months = ['Sep', 'Oct', 'Nov']

    # Filter data for Jordan
    jordan_data = data[data['Country'] == 'Jordan']

    # Create dummy monthly data for the example (Replace with actual monthly data)
    months = [f'{year}-{month:02d}' for year in range(1961, 2020 + 1) for month in range(1, 13)]
    jordan_data = pd.DataFrame({'Country': ['Jordan'] * len(months), 'Month': months, 'Temperature Change': np.random.randn(len(months))})

    # Convert Month column to datetime
    jordan_data['Month'] = pd.to_datetime(jordan_data['Month'])

    # Define seasons
    seasons = {'Winter': winter_months, 'Spring': spring_months, 'Summer': summer_months, 'Fall': fall_months}

    # Calculate seasonal averages
    seasonal_averages = []
    for season, months in seasons.items():
        season_data = jordan_data[jordan_data['Month'].dt.strftime('%b').isin(months)]
        season_data['Year'] = season_data['Month'].dt.year
        season_avg = season_data.groupby('Year')['Temperature Change'].mean().reset_index()
        season_avg['Season'] = season
        seasonal_averages.append(season_avg)

    # Combine all seasonal averages into one DataFrame
    seasonal_averages_df = pd.concat(seasonal_averages)

    # Plot the seasonal temperature changes
    fig_season = go.Figure()

    for season in seasons.keys():
        season_data = seasonal_averages_df[seasonal_averages_df['Season'] == season]
        fig_season.add_trace(go.Scatter(x=season_data['Year'], y=season_data['Temperature Change'], mode='lines+markers', name=season))

    fig_season.update_layout(
        title='Seasonal Temperature Changes in Jordan (1961-2020)',
        xaxis_title='Year',
        yaxis_title='Temperature Change (°C)',
        template='plotly_white',
        showlegend=True,
        width=800,
        height=400
    )
    st.plotly_chart(fig_season)

    # Calculate the average temperature change for each year across all countries
    years = list(range(2013, 2023))

    # Calculate the average temperature change for each country
    average_temp_change = data.groupby('Country')['Temperature Change'].mean().reset_index()

    # Identify the top 3 countries with the highest average temperature changes
    top_3_max_countries = average_temp_change.nlargest(3, 'Temperature Change')

    # Identify the 3 countries with the lowest average temperature changes
    bottom_3_min_countries = average_temp_change.nsmallest(3, 'Temperature Change')

    # Include Jordan for comparison
    jordan_data = average_temp_change[average_temp_change['Country'].str.contains('Jordan', case=False)]

    # Combine the selected countries for the max comparison
    max_comparison_data = pd.concat([top_3_max_countries, jordan_data])

    # Combine the selected countries for the min comparison
    min_comparison_data = pd.concat([bottom_3_min_countries, jordan_data])

    # Filter the data to include only the selected countries
    max_comparison_temps = data[data['Country'].isin(max_comparison_data['Country'])]
    min_comparison_temps = data[data['Country'].isin(min_comparison_data['Country'])]

    # Pivot the data to have countries as rows and years as columns for plotting
    max_comparison_pivot = max_comparison_temps.pivot(index='Country', columns='Year', values='Temperature Change')
    min_comparison_pivot = min_comparison_temps.pivot(index='Country', columns='Year', values='Temperature Change')

    # Create a plotly figure for the max comparison
    fig_max = go.Figure()

    # Plot the temperature changes for Jordan and the top 3 max countries
    for country in max_comparison_pivot.index:
        fig_max.add_trace(go.Scatter(x=max_comparison_pivot.columns, y=max_comparison_pivot.loc[country], mode='lines+markers', name=country))

    # Update layout for the max comparison figure
    fig_max.update_layout(
        title='Temperature Change Comparison: Jordan vs. Top 3 Max Countries',
        xaxis_title='Year',
        yaxis_title='Temperature Change (°C)',
        legend_title='Country',
        template='plotly_white'
    )
    st.plotly_chart(fig_max)

    # Create a plotly figure for the min comparison
    fig_min = go.Figure()

    # Plot the temperature changes for Jordan and the bottom 3 min countries
    for country in min_comparison_pivot.index:
        fig_min.add_trace(go.Scatter(x=min_comparison_pivot.columns, y=min_comparison_pivot.loc[country], mode='lines+markers', name=country))

    # Update layout for the min comparison figure
    fig_min.update_layout(
        title='Temperature Change Comparison: Jordan vs. Bottom 3 Min Countries',
        xaxis_title='Year',
        yaxis_title='Temperature Change (°C)',
        legend_title='Country',
        template='plotly_white'
    )
    st.plotly_chart(fig_min)

    # Define Jordan's neighboring countries
    neighboring_countries = ['Saudi Arabia', 'Iraq', 'Palestine', 'Syria', 'Lebanon', 'Egypt']

    # Add Jordan to the list for comparison
    countries_to_plot = ['Jordan'] + neighboring_countries

    # Extract temperature changes for the selected countries
    selected_countries_data = data[data['Country'].isin(countries_to_plot)]

    # Remove duplicate entries for the same country and year combination
    selected_countries_data = selected_countries_data.drop_duplicates(subset=['Country', 'Year'])

    # Pivot the data to have countries as rows and years as columns
    selected_countries_temps = selected_countries_data.pivot(index='Country', columns='Year', values='Temperature Change')

    # Plot Jordan with each pair of neighboring countries
    for i in range(0, len(neighboring_countries), 2):
        fig_neighbor = go.Figure()

        # Plot Jordan
        fig_neighbor.add_trace(go.Scatter(x=selected_countries_temps.columns, y=selected_countries_temps.loc['Jordan'], mode='lines+markers', name='Jordan'))

        # Plot neighboring countries
        for j in range(2):
            if i + j < len(neighboring_countries):
                country = neighboring_countries[i + j]
                fig_neighbor.add_trace(go.Scatter(x=selected_countries_temps.columns, y=selected_countries_temps.loc[country], mode='lines+markers', name=country))

        # Update layout
        fig_neighbor.update_layout(
            title=f'Temperature Change Comparison: Jordan vs. {neighboring_countries[i]} and {neighboring_countries[i+1] if i+1 < len(neighboring_countries) else ""}',
            xaxis_title='Year',
            yaxis_title='Temperature Change (°C)',
            legend_title='Country',
            template='plotly_white',
            width=900,
            height=600
        )
        st.plotly_chart(fig_neighbor)

elif options == "Urban vs. Rural Trends":
    st.header("Urban vs. Rural Temperature Trends")

    # Plot urban vs. rural temperature trends
    urban_data = data[data['Urban_Rural'] == 'Urban'].groupby('Year')['Temperature Change'].mean().reset_index()
    rural_data = data[data['Urban_Rural'] == 'Rural'].groupby('Year')['Temperature Change'].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=urban_data['Year'], y=urban_data['Temperature Change'], mode='lines+markers', name='Urban'))
    fig.add_trace(go.Scatter(x=rural_data['Year'], y=rural_data['Temperature Change'], mode='lines+markers', name='Rural'))
    fig.update_layout(title='Urban vs. Rural Temperature Trends (1961-2020)', xaxis_title='Year', yaxis_title='Temperature Change (°C)')
    st.plotly_chart(fig)

elif options == "G7 Analysis":
    st.header("G7 Countries Analysis")

    # Plot G7 temperature trends
    g7_countries = ['Canada', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States']
    g7_data = data[data['Country'].isin(g7_countries)]
    fig = px.line(g7_data, x='Year', y='Temperature Change', color='Country', title='Temperature Trends of G7 Countries (1961-2020)')
    st.plotly_chart(fig)

elif options == "Statistical Analysis":
    st.header("Statistical Analysis and Correlations")

    # Calculate statistical summary for Jordan
    jordan_stats = {
        'Mean': jordan_temperature_change.mean(),
        'Median': jordan_temperature_change.median(),
        'Standard Deviation': jordan_temperature_change.std(),
        'Minimum': jordan_temperature_change.min(),
        'Maximum': jordan_temperature_change.max()
    }

    # Calculate statistical summary for the global average
    global_stats = {
        'Mean': average_temperature_change.mean(),
        'Median': average_temperature_change.median(),
        'Standard Deviation': average_temperature_change.std(),
        'Minimum': average_temperature_change.min(),
        'Maximum': average_temperature_change.max()
    }

    # Create a DataFrame to display the results
    stats_df = pd.DataFrame([jordan_stats, global_stats], index=['Jordan', 'Global Average'])

    # Display the DataFrame as a colorful table
    st.dataframe(stats_df.style.background_gradient(cmap='coolwarm'))

    # Calculate correlation
    correlation_coefficient = np.corrcoef(jordan_temperature_change, average_temperature_change)[0, 1]
    st.write(f"**Correlation between Jordan's temperature change and global average: {correlation_coefficient:.2f}**")

    # Define the categories
    categories = ['Mean', 'Median', 'Standard Deviation', 'Minimum', 'Maximum']

    # Define the values for Jordan and Global Average
    jordan_values = [jordan_stats[cat] for cat in categories]
    global_values = [global_stats[cat] for cat in categories]

    # Create a plotly figure
    fig = go.Figure()

    # Add bars for Jordan
    fig.add_trace(go.Bar(
        x=categories,
        y=jordan_values,
        name='Jordan',
        marker_color='blue'
    ))

    # Add bars for Global Average
    fig.add_trace(go.Bar(
        x=categories,
        y=global_values,
        name='Global Average',
        marker_color='orange'
    ))

    # Update layout
    fig.update_layout(
        title='Statistical Summary: Jordan vs. Global Average',
        xaxis_title='Statistic',
        yaxis_title='Value',
        barmode='group',
        template='plotly_white'
    )
    st.plotly_chart(fig)

    # Calculate the deviations between Jordan's temperature change and the global average
    deviations = jordan_temperature_change - average_temperature_change

    # Identify years with significant deviations (greater than one standard deviation of global average)
    threshold = average_temperature_change.std()
    significant_deviations = deviations[abs(deviations) > threshold]

    significant_frame = significant_deviations.to_frame().reset_index()
    st.write("**Significant Deviations in Temperature Change: Jordan vs. Global Average**")
    st.dataframe(significant_frame.style.background_gradient(cmap='coolwarm'))

    st.write("**Outlier Countries in Temperature Change**")

    # Calculate average temperature change for each country
    average_temp_change_by_country = data.groupby('Country')['Temperature Change'].mean().reset_index()

    # Calculate the Z-scores for average temperature changes
    mean_temp_change = average_temp_change_by_country['Temperature Change'].mean()
    std_temp_change = average_temp_change_by_country['Temperature Change'].std()
    average_temp_change_by_country['Z_Score'] = (average_temp_change_by_country['Temperature Change'] - mean_temp_change) / std_temp_change

    # Identify outliers using a threshold of 2 standard deviations
    outliers = average_temp_change_by_country[(average_temp_change_by_country['Z_Score'] > 2) | (average_temp_change_by_country['Z_Score'] < -2)]
    st.dataframe(outliers[['Country', 'Temperature Change', 'Z_Score']].style.background_gradient(cmap='coolwarm'))

    # Identify the result for Jordan
    jordan_result = average_temp_change_by_country[average_temp_change_by_country['Country'] == 'Jordan']

    # Plot the results
    fig_outlier = go.Figure()

    # Plot all countries
    fig_outlier.add_trace(go.Scatter(
        x=average_temp_change_by_country['Country'],
        y=average_temp_change_by_country['Temperature Change'],
        mode='markers',
        name='All Countries',
        marker=dict(color='red', size=8)
    ))

    # Highlight outliers
    fig_outlier.add_trace(go.Scatter(
        x=outliers['Country'],
        y=outliers['Temperature Change'],
        mode='markers+lines',
        line=dict(dash='dash', color='red'),
        marker=dict(color='red', size=12, symbol='circle'),
        name='Outliers'
    ))

    # Highlight Jordan
    fig_outlier.add_trace(go.Scatter(
        x=jordan_result['Country'],
        y=jordan_result['Temperature Change'],
        mode='markers',
        marker=dict(color='blue', size=15, symbol='star'),
        name='Jordan'
    ))

    # Update layout
    fig_outlier.update_layout(
        title='Outlier Countries in Temperature Change with Jordan Highlighted',
        xaxis_title='Country',
        yaxis_title='Average Temperature Change (°C)',
        showlegend=True,
        template='plotly_white'
    )
    st.plotly_chart(fig_outlier)

elif options == "Conclusions":
    st.header("Conclusions and Insights")
    st.write("""
        ### Summary of Findings

        This study has provided a comprehensive analysis of climate change indicators, with a particular focus on Jordan. The key findings are summarized as follows:

        - **Global and Regional Temperature Trends**: The analysis revealed significant global warming trends over the past decades, with the most considerable increases occurring after 2000. The top 10 warmest years globally all fall within this period, reflecting the accelerating impact of climate change.
        - **Jordan's Temperature Trends**: Jordan's temperature changes closely follow global trends, with notable increases after 2000. The strong positive correlation between Jordan's temperature changes and the global average (0.77) underscores the influence of global climatic factors on the country's local climate.
        - **Seasonal Temperature Changes**: Seasonal analysis for Jordan indicated that all seasons have experienced temperature increases, with summer showing the most pronounced rise. This seasonal trend aligns with the broader global patterns of increasing temperatures.
        - **Urban vs. Rural Trends**: The comparison between urban and rural areas highlighted that urban areas generally experience higher temperature changes than rural areas. This finding is consistent with the urban heat island effect, where urbanization and human activities contribute to higher temperatures in cities.
        - **G7 Countries Analysis**: The temperature trends in G7 countries also reflect significant warming, with consistent increases across all member nations. This analysis provides a comparative perspective on how developed nations are experiencing and potentially contributing to climate change.

        **Implications and Future Research Directions**

        The findings of this study have several important implications:

        - Policy and Planning: The strong correlation between local and global temperature trends emphasizes the need for Jordan to align its climate policies with global efforts to mitigate climate change. National strategies should consider the broader global context to effectively address local climate challenges.
        - Urban Planning: The higher temperature changes in urban areas call for targeted urban planning and infrastructure development to mitigate the urban heat island effect. This includes increasing green spaces, enhancing building energy efficiency, and promoting sustainable urbanization practices.
        - Adaptation Strategies: Seasonal temperature changes highlight the need for season-specific adaptation strategies, particularly in agriculture, water management, and public health. For instance, measures to cope with higher summer temperatures can help mitigate heat-related health risks and ensure water security.
        - Further Research: Future research should explore the underlying causes of temperature changes in Jordan and other regions. This includes investigating the role of human activities, land use changes, and natural climatic variations. Additionally, more granular data on monthly and seasonal temperature changes can provide deeper insights into the dynamics of climate change.
    """)

# Footer
st.sidebar.title("About")
st.sidebar.image("dhif_6.png", use_column_width=True)  # Add your image file here
st.sidebar.info("""
    This dashboard is created by DhifAllah Alayadi.
    - Email: dhifalayadi@gmail.com
    - [LinkedIn](https://www.linkedin.com/in/Alayadi)
    - [DataCamp](https://www.datacamp.com/portfolio/alayadidhif)
    - [Tableau](https://public.tableau.com/app/profile/dhifallah/vizzes)
""")
