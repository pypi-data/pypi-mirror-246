import datetime

import boto3
import matplotlib.pyplot as plt

# Initialize boto3 client
session = boto3.Session(profile_name="fbs-prod-userfull")
cloudwatch = session.client("cloudwatch")

PERIOD = 60  # Period in seconds
MAX_DATAPOINTS = 1440  # Number of data points to retrieve
MAX_TIME_RANGE = PERIOD * MAX_DATAPOINTS  # Maximum time range in seconds

end_time = datetime.datetime.now(datetime.UTC)
start_time = end_time - datetime.timedelta(minutes=MAX_TIME_RANGE / 60)

# Fetch latency data from CloudWatch
response = cloudwatch.get_metric_statistics(
    Namespace="AWS/ApiGateway",
    MetricName="Latency",
    Dimensions=[{"Name": "ApiName", "Value": "pcv-prod-api"}],
    StartTime=start_time,
    EndTime=end_time,
    Period=PERIOD,
    Statistics=["Maximum"],
)

# Extract data for histogram
latency_values = [datapoint["Maximum"] for datapoint in response["Datapoints"]]

# Define custom bins
custom_bins = [i for i in range(0, 1000, 20)]  # Equidistant bins
custom_bins += [2000, 3000, 4000, 5000, 6000]  # Non-equidistant bins

# Create Histogram
plt.hist(latency_values, bins=custom_bins, edgecolor="black")
# plt.hist(latency_values, bins=40)

plt.title("API Gateway Latency Histogram")
plt.xlabel("Latency (ms)")
plt.ylabel("Frequency")
plt.show()
