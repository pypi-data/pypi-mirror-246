import unittest
from unittest.mock import Mock
from pyspark.sql import SparkSession, Row
from services.ApiFlightRadar import ApiFlightRadar
from services.utils.LoggerManager import LoggerManager
from services.SparkManager import SparkManager
from kpis.KPIsClass import KPIAnalytics


class TestGetMostFlights(unittest.TestCase):
    def setUp(self):
        # Creating a Spark session for testing
        self.spark = (
            SparkSession.builder.master("local").appName("TestSession").getOrCreate()
        )

        # Mocking dependencies
        self.mock_logger = Mock(spec=LoggerManager)
        self.mock_logger.info = Mock()

        self.mock_api_wrapper = Mock(spec=ApiFlightRadar)

        # Creating SparkManager and KPIAnalytics instances
        self.spark_manager = SparkManager(self.mock_logger)
        self.kpi_analytics = KPIAnalytics(
            self.spark_manager, self.mock_logger, self.mock_api_wrapper
        )

        # Preparing test data
        flight_data = [
            Row(icao_airline="AAA", status="In Progress"),
            Row(icao_airline="AAA", status="In Progress"),
            Row(icao_airline="BBB", status="In Progress"),
            Row(icao_airline="CCC", status="Completed"),
        ]
        airline_data = [
            Row(name="Airline A", icao="AAA"),
            Row(name="Airline B", icao="BBB"),
            Row(name="Airline C", icao="CCC"),
        ]

        self.flight_df = self.spark.createDataFrame(flight_data)
        self.airline_df = self.spark.createDataFrame(airline_data)

        # Creating temporary views to mimic database tables
        self.flight_df.createOrReplaceTempView("flight")
        self.airline_df.createOrReplaceTempView("airline")

    def test_get_most_flights(self):
        # Executing the method under test
        result_df = self.kpi_analytics.get_most_flights()

        # Expected result
        expected_data = [Row(name="Airline A", icao_airline="AAA", count_status=2)]
        expected_df = self.spark.createDataFrame(expected_data)

        # Assert the result
        self.assertEqual(result_df.collect(), expected_df.collect())

    def tearDown(self):
        # To stop the Spark session
        self.spark.stop()


if __name__ == "__main__":
    unittest.main()
