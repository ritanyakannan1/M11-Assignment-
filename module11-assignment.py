# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- DATA CREATION (DO NOT MODIFY) -----
np.random.seed(42)

quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:
                seasonal_factor = 1.3
            elif quarter.quarter == 1:
                seasonal_factor = 0.8
            
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)
            
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

customer_data = []
total_customers = 2000

age_params = {
    'Tampa': (45, 15),
    'Miami': (35, 12),
    'Orlando': (38, 14),
    'Jacksonville': (42, 13)
}

for location in locations:
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)
    
    for age in ages:
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        base_amount = np.random.gamma(shape=5, scale=20)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], p=[0.3, 0.5, 0.2])
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# ----- VISUALIZATIONS -----

def plot_quarterly_sales_trend():
    total_sales = sales_df.groupby('QuarterLabel')['Sales'].sum()
    fig, ax = plt.subplots()
    ax.plot(total_sales.index, total_sales.values, marker='o')
    ax.set_title("Total Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales ($)")
    ax.grid(True)
    plt.xticks(rotation=45)
    return fig

def plot_location_sales_comparison():
    location_sales = sales_df.groupby(['QuarterLabel', 'Location'])['Sales'].sum().unstack()
    fig, ax = plt.subplots()
    for loc in location_sales.columns:
        ax.plot(location_sales.index, location_sales[loc], marker='o', label=loc)
    ax.set_title("Sales Trends by Location")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales ($)")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)
    return fig

def plot_category_performance_by_location():
    latest = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']
    grouped = latest.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    fig, ax = plt.subplots()
    grouped.plot(kind='bar', ax=ax)
    ax.set_title("Category Performance by Location (Q4 2023)")
    return fig

def plot_sales_composition_by_location():
    grouped = sales_df.groupby(['Location', 'Category'])['Sales'].sum().unstack()
    percent = grouped.div(grouped.sum(axis=1), axis=0)
    fig, ax = plt.subplots()
    percent.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Sales Composition by Location")
    return fig

def plot_ad_spend_vs_sales():
    fig, ax = plt.subplots()
    x = sales_df['AdSpend']
    y = sales_df['Sales']
    ax.scatter(x, y, alpha=0.6)
    m, b = np.polyfit(x, y, 1)
    ax.plot(x, m*x + b)
    ax.set_title("Ad Spend vs Sales")
    return fig

def plot_ad_efficiency_over_time():
    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()
    fig, ax = plt.subplots()
    ax.plot(efficiency.index, efficiency.values, marker='o')
    ax.set_title("Ad Efficiency Over Time")
    return fig

def plot_customer_age_distribution():
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    for i, loc in enumerate(locations):
        data = customer_df[customer_df['Location'] == loc]['Age']
        axes[i].hist(data, bins=15)
        axes[i].set_title(loc)
    fig.suptitle("Customer Age Distribution")
    return fig

def plot_purchase_by_age_group():
    bins = [18, 30, 45, 60, 80]
    labels = ['18-30', '31-45', '46-60', '61+']
    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins=bins, labels=labels)
    data = [customer_df[customer_df['AgeGroup'] == grp]['PurchaseAmount'] for grp in labels]
    fig, ax = plt.subplots()
    ax.boxplot(data, labels=labels)
    ax.set_title("Purchase by Age Group")
    return fig

def plot_purchase_amount_distribution():
    fig, ax = plt.subplots()
    ax.hist(customer_df['PurchaseAmount'], bins=20)
    ax.set_title("Purchase Amount Distribution")
    return fig

def plot_sales_by_price_tier():
    totals = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    fig, ax = plt.subplots()
    ax.pie(totals, labels=totals.index, autopct='%1.1f%%')
    ax.set_title("Sales by Price Tier")
    return fig

def plot_category_market_share():
    totals = sales_df.groupby('Category')['Sales'].sum()
    fig, ax = plt.subplots()
    ax.pie(totals, labels=totals.index, autopct='%1.1f%%')
    ax.set_title("Category Market Share")
    return fig

def plot_location_sales_distribution():
    totals = sales_df.groupby('Location')['Sales'].sum()
    fig, ax = plt.subplots()
    ax.pie(totals, labels=totals.index, autopct='%1.1f%%')
    ax.set_title("Location Sales Distribution")
    return fig

def create_business_dashboard():
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    total_sales = sales_df.groupby('QuarterLabel')['Sales'].sum()
    axes[0, 0].plot(total_sales.index, total_sales.values)
    axes[0, 0].set_title("Sales Trend")

    efficiency = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()
    axes[0, 1].plot(efficiency.index, efficiency.values)
    axes[0, 1].set_title("Ad Efficiency")

    category_sales = sales_df.groupby('Category')['Sales'].sum()
    axes[1, 0].pie(category_sales, labels=category_sales.index, autopct='%1.1f%%')

    location_sales = sales_df.groupby('Location')['Sales'].sum()
    axes[1, 1].pie(location_sales, labels=location_sales.index, autopct='%1.1f%%')

    fig.suptitle("Business Dashboard")
    return fig

def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    plot_quarterly_sales_trend()
    plot_location_sales_comparison()
    plot_category_performance_by_location()
    plot_sales_composition_by_location()
    plot_ad_spend_vs_sales()
    plot_ad_efficiency_over_time()
    plot_customer_age_distribution()
    plot_purchase_by_age_group()
    plot_purchase_amount_distribution()
    plot_sales_by_price_tier()
    plot_category_market_share()
    plot_location_sales_distribution()
    create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("- Sales increase over time, with strong Q4 spikes.")
    print("- Miami is the strongest performing location overall.")
    print("- Electronics consistently leads in sales.")
    print("- More ad spend generally leads to higher sales.")
    print("- Mid-range products bring in the most revenue.")

    plt.show()

if __name__ == "__main__":
    main()