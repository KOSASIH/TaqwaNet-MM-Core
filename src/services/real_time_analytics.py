# src/services/real_time_analytics.py

import json
from kafka import KafkaConsumer
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window

class RealTimeAnalytics:
    def __init__(self, kafka_topic, kafka_bootstrap_servers):
        self.kafka_topic = kafka_topic
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.spark = SparkSession.builder \
            .appName("RealTimeAnalytics") \
            .getOrCreate()

    def consume_data(self):
        consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=self.kafka_bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
        
        for message in consumer:
            data = message.value
            self.process_data(data)

    def process_data(self, data):
        # Convert data to DataFrame
        df = self.spark.createDataFrame([data])
        
        # Perform real-time analytics (e.g., aggregations, windowing)
        aggregated_df = df.groupBy(window(col("timestamp"), "1 minute")) \
            .agg({"value": "avg"})  # Example aggregation
        
        # Output the results (could be to a database, dashboard, etc.)
        aggregated_df.show()

if __name__ == "__main__":
    kafka_topic = "financial_data"
    kafka_bootstrap_servers = "localhost:9092"
    
    analytics_service = RealTimeAnalytics(kafka_topic, kafka_bootstrap_servers)
    analytics_service.consume_data()
