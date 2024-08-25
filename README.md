# apachelogparsing
Apache log parsing using python3 and visualization
Innstall following libraries for this script to work as intended
pip install pandas matplotlib seaborn loguru

Code indicators to get idea #comment
   

  -> def parse_data
    Parses Apache log data from the specified log file into a DataFrame.
  -> def compute_hourly_anomalies(counts):
    Identifies anomalies in hourly request counts using a threshold-based method.

  
   ->  pd.Series: Hours where request counts exceed the calculated threshold.
    

  -> def analyze_data(df):
    Analyzes the log data to find anomalies and generate statistics.

   ->  Compute anomalies
    anomalies = compute_hourly_anomalies(hourly_counts)

  -> Status code distribution
    status_code_counts = df['status_code'].value_counts()
