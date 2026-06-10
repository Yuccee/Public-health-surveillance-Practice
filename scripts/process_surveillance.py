import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. Create Mock Public Health Dataset (Simulating messy field data)
def generate_mock_data():
    data = {
        "report_date": ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04", "2026-06-05", "2026-06-06", "2026-06-07"],
        "facility_name": ["Wuse General Clinic", "Wuse General Clinic", "Wuse General Clinic", "Garki Hospital", "Garki Hospital", None, "Garki Hospital"],
        "waterborne_cases_reported": [3, 5, 12, 2, 4, 18, 25],  # Spike represents an outbreak
        "malaria_cases_reported": [14, 11, None, 8, 15, 12, 9]  # Simulating missing data
    }
    df = pd.DataFrame(data)
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/clinic_surveillance_raw.csv', index=False)
    print("✅ Messy mock field dataset created at data/clinic_surveillance_raw.csv")

# 2. Data Cleaning & Validation (Core MERL Data Task)
def clean_and_analyze():
    df = pd.read_csv('data/clinic_surveillance_raw.csv')
    
    # Handle missing values (Data Quality Assurance)
    df['facility_name'] = df['facility_name'].fillna("Unknown Facility")
    df['malaria_cases_reported'] = df['malaria_cases_reported'].fillna(df['malaria_cases_reported'].median())
    
    # Convert date column to datetime object
    df['report_date'] = pd.to_datetime(df['report_date'])
    
    # Outbreak Detection Rules: Trigger alert if waterborne cases > 10 in a single day
    ALERT_THRESHOLD = 10
    df['outbreak_alert'] = df['waterborne_cases_reported'] > ALERT_THRESHOLD
    
    print("\n--- Cleaned Epidemiological Surveillance Summary ---")
    print(df)
    
    # Generate an automated alert report summary
    alerts = df[df['outbreak_alert'] == True]
    if not alerts.empty:
        print("\n🚨 CRITICAL PUBLIC HEALTH ALERTS DETECTED:")
        for idx, row in alerts.iterrows():
            print(f"  - [{row['report_date'].strftime('%Y-%m-%d')}] High risk of waterborne outbreak at {row['facility_name']}! Cases: {row['waterborne_cases_reported']}")
            
    # 3. Data Visualization (Exporting trends)
    plt.figure(figsize=(10, 5))
    plt.plot(df['report_date'], df['waterborne_cases_reported'], marker='o', color='red', label='Waterborne Cases')
    plt.plot(df['report_date'], df['malaria_cases_reported'], marker='x', color='blue', label='Malaria Cases')
    plt.axhline(y=ALERT_THRESHOLD, color='gray', linestyle='--', label='Outbreak Threshold')
    plt.title('Daily Public Health Disease Surveillance Trends (Abuja Region)')
    plt.xlabel('Date')
    plt.ylabel('Number of Reported Cases')
    plt.legend()
    plt.grid(True)
    
    # Save the chart
    plt.savefig('data/surveillance_trend.png')
    print("\n📊 Trend visualization chart saved to data/surveillance_trend.png")

if __name__ == "__main__":
    generate_mock_data()
    clean_and_analyze()
