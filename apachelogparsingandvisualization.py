import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from loguru import logger
import re
import os


logger.add("apache_log_analysis.log", rotation="1 week", level="INFO", format="{time} {level} {message}")


LOG_PATTERN = re.compile(
    r'(?P<remote_addr>\S+) \S+ \S+ \[.*?\] "(?P<request_method>\S+) (?P<request_uri>\S+) \S+" '
    r'(?P<status_code>\d{3}) (?P<response_size>\d+|-)'
)

def parse_data(src_logf):
    
    if not os.path.isfile(src_logf):
        logger.error("Log file not found: %s", src_logf)
        return None

    data = {
        'remote_addr': [],
        'timestamp': [],
        'request_method': [],
        'request_uri': [],
        'status_code': [],
        'response_size': []
    }

    try:
        with open(src_logf, 'r') as f:
            for line in f:
                match = LOG_PATTERN.match(line)
                if match:
                    data['remote_addr'].append(match.group('remote_addr'))
                    # Extract and parse timestamp
                    timestamp_str = line.split('[')[1].split(']')[0]
                    data['timestamp'].append(datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S %z'))
                    data['request_method'].append(match.group('request_method'))
                    data['request_uri'].append(match.group('request_uri'))
                    data['status_code'].append(int(match.group('status_code')))
                    # Handle response size
                    response_size = match.group('response_size')
                    data['response_size'].append(int(response_size) if response_size != '-' else 0)
    except Exception as e:
        logger.error("Error parsing log file: %s", e)
        return None

    df = pd.DataFrame(data)
    logger.info("Logs successfully parsed from %s", src_logf)
    return df

def compute_hourly_anomalies(counts):

    mean_count = counts.mean()
    std_dev_count = counts.std()
    threshold = mean_count + 2 * std_dev_count
    anomalies = counts[counts > threshold]
    return anomalies

def analyze_data(df):
    
    df['hour'] = df['timestamp'].dt.hour
    hourly_counts = df.groupby('hour').size()

    # Compute anomalies
    anomalies = compute_hourly_anomalies(hourly_counts)

    # Status code distribution
    status_code_counts = df['status_code'].value_counts()

    logger.info("Data analysis complete. Detected %d anomalies.", len(anomalies))
    return hourly_counts, anomalies, status_code_counts

def display_data(hourly_counts, anomalies, status_code_counts):
    
    plt.figure(figsize=(14, 8))

    
    plt.subplot(2, 1, 1)
    sns.lineplot(x=hourly_counts.index, y=hourly_counts.values, label='Request Count', color='blue')
    plt.axhline(y=hourly_counts.mean(), color='r', linestyle='--', label='Mean')
    plt.axhline(y=hourly_counts.mean() + 2 * hourly_counts.std(), color='g', linestyle='--', label='Threshold')
    plt.scatter(anomalies.index, anomalies.values, color='red', zorder=5, label='Anomalies')
    plt.title('Hourly Request Counts and Detected Anomalies')
    plt.xlabel('Hour of Day')
    plt.ylabel('Request Count')
    plt.legend()
    plt.grid(True)

    plt.subplot(2, 1, 2)
    sns.barplot(x=status_code_counts.index, y=status_code_counts.values, palette='viridis')
    plt.title('HTTP Status Code Distribution')
    plt.xlabel('Status Code')
    plt.ylabel('Count')
    plt.grid(True)

    plt.tight_layout()
    plt.show()

def main():
  
    log_file_path = 'C:/Users/muhammad.bilal46/Downloads/apache_log.log'
    
    logger.info("Starting log analysis for file: %s", log_file_path)
    
    # Parse logs
    df = parse_data(log_file_path)
    if df is None:
        logger.error("Failed to parse logs.")
        return

    # Analyze data
    hourly_counts, anomalies, status_code_counts = analyze_data(df)

    # Display results
    display_data(hourly_counts, anomalies, status_code_counts)

if __name__ == "__main__":
    main()
