### Real-Time Ride-Sharing Analytics with Apache Spark
This project implements a real-time analytics pipeline for a ride-sharing platform using Apache Spark Structured Streaming. The pipeline processes streaming data, performs real-time aggregations, and analyzes trends over time.

## Project Structure
The project consists of three tasks with increasing complexity:

Task 1: Basic data ingestion and parsing
Task 2: Driver-based aggregations with custom batch writing
Task 3: Time-windowed analytics with watermarking

### Setup Instructions

## Install the required packages:
```
pip install pyspark
```


## Running the Applications
## Data Simulator
To simulate ride data streaming, you need to run a data generator that sends JSON data to a socket. Create a file called data_generator.py
## Start the data generator:
```
python ride_data_generator.py
```
## Task 1: Basic Data Ingestion
Code Explanation
task1_basic_streaming.py performs the following operations:

1. Creates a Spark session with the application name "RideShare-Task1"
2. Defines a schema for the incoming JSON ride data with fields:

trip_id: Integer
driver_id: Integer
distance_km: Double
fare_amount: Double
timestamp: String

3. Reads streaming data from a socket (localhost:9999)
4. Parses the JSON messages into a structured DataFrame
5. Outputs the parsed data to the console

Run the following command in a new terminal window:
```
spark-submit task1_basic_streaming.py

```
## Sample Output
```
+--------------------------------------+---------+------------+----------+-------------------+
|trip_id                              |driver_id|distance_km |fare_amount|timestamp          |
+--------------------------------------+---------+------------+----------+-------------------+
|c94b7de0-c749-479a-a55c-763ea85787b9 |72       |48.81       |74.66     |2025-04-01 17:50:25|
|09b2253a-f63b-4de5-b9ce-39fb8c0a28b4 |83       |35.1        |86.27     |2025-04-01 17:50:27|
|998d0edc-1293-4cef-80bb-4882fb583d15 |27       |3.66        |73.61     |2025-04-01 17:50:29|
+--------------------------------------+---------+------------+----------+-------------------+
```
## Task 2: Real-Time Aggregations (Driver-Level)
Code Explanation
task2_realtime_aggregations.py builds on Task 1 and adds:

1. Groups the data by driver_id
2. Calculates two aggregations:

total_fare: Sum of fare amounts for each driver
avg_distance: Average distance traveled by each driver

3. Outputs these aggregations to both the console and CSV files
4. Uses "complete" output mode to show the current state of all aggregations

Execution
Run the following command in a new terminal window:
```
spark-submit task2_realtime_aggregations.py
```

## Sample output
```
+---------+----------+------------+
|driver_id|total_fare|avg_distance|
+---------+----------+------------+
|28       |105.06    |47.29       |
|71       |136.59    |28.74       |
|99       |108.22    |33.83       |
|96       |81.45     |13.39       |
|77       |127.61    |21.81       |
|55       |142.79    |24.47       |
|38       |30.22     |49.39       |
|25       |58.86     |14.68       |
|81       |38.81     |28.64       |
|56       |75.97     |23.83       |
|49       |145.11    |18.82       |
|65       |22.0      |25.01       |
|4        |41.59     |31.87       |
|91       |196.63    |23.77       |
+---------+----------+------------+
``` 

## Task 3: Windowed Time-Based Analytics
Code Explanation
task3_windowed_analytics.py extends the pipeline to:

1. Convert the string timestamp to a proper TimestampType column named event_time
2. Use Spark's window function to:

Create 5-minute windows that slide by 1 minute
Aggregate the fare_amount within each window

3. Select the window's start and end times along with the total fare
4. Output the windowed results to both the console and CSV files

Execution
Run the following command in a new terminal window:
```
spark-submit task3_windowed_analytics.py
```
## Sample output

```
+-------------------+-------------------+----------+
|window_start       |window_end         |total_fare|
+-------------------+-------------------+----------+
|2025-04-01T22:42:00|2025-04-01T22:47:00|3287.32   |
|2025-04-01T22:39:00|2025-04-01T22:44:00|3287.32   |
|2025-04-01T22:43:00|2025-04-01T22:48:00|1829.53   |
|2025-04-01T22:40:00|2025-04-01T22:45:00|3287.32   |
|2025-04-01T22:41:00|2025-04-01T22:46:00|3287.32   |
+-------------------+-------------------+----------+
```

## Stopping the Applications
The applications run indefinitely until manually stopped. Press Ctrl+C to stop them.
## Troubleshooting

If you get "Address already in use" errors, make sure no other application is using port 9999
Check Spark logs for detailed error information
Ensure all directories have appropriate write permissions