from typing import List
from models.DataSchema import Flight
from .BaseService import BaseService


class ServiceFlight(BaseService):
    """
    Service class for handling flight-related operations.

    Extends:
        BaseService

    Attributes:
        api_flight_radar: Instance for interacting with flight radar API.
        logger: Logger instance for logging messages.
        spark_manager: Instance of SparkManager for handling Spark operations.
    """

    def __init__(self, api_flight_radar, logger, spark_manager):
        """
        Initialize ServiceFlight with API, logger, and Spark manager.

        Args:
            api_flight_radar: Instance for interacting with flight radar API.
            logger: Logger instance for logging messages.
            spark_manager: Instance of SparkManager for handling Spark operations.
        """
        self.api_flight_radar = api_flight_radar
        self.logger = logger
        self.spark_manager = spark_manager

    def get_data(self) -> List[Flight]:
        """
        Fetch flight data using the Flight Radar API.

        Returns:
            List[Flight]: A list of Flight objects.
        """
        try:
            self.logger.info("Fetching flight data...")
            flights = self.api_flight_radar.get_flights_data()
            return flights
        except Exception as e:
            self.logger.error(f"Error in get_data: {e}")
            return []

    def process_data(self, data):
        """
        Processes the fetched flight data.

        Args:
            data: Raw flight data to be processed.

        Returns:
            DataFrame: Processed flight data in DataFrame format or None if error.
        """
        try:
            self.logger.info("Processing flight data...")
            if not data:
                self.logger.warning("No flight data to process.")
                return None
            df_flights = self.spark_manager.create_df(data, Flight.get_schema())
            df_flights = self.spark_manager.clean_df(df_flights)
            return df_flights
        except Exception as e:
            self.logger.error(f"Error in process_data: {e}")
            return None

    def save_data(self, data):
        """
        Saves the processed flight data.

        Args:
            data: Processed flight data to be saved.
        """
        try:
            if data is None:
                self.logger.warning("No flight data available to save.")
                return
            self.logger.info("Saving flight data...")
            self.spark_manager.save_df(data, "Flight", "flight")
            self.logger.info("Flight data saved successfully.")
        except Exception as e:
            self.logger.error(f"Error in save_data: {e}")

    def create_view(self, data):
        """
        Creates a view for the processed flight data for easier querying.

        Args:
            data: Processed flight data for which the view is to be created.
        """
        try:
            if data is None:
                self.logger.warning("No flight data available to create a view.")
                return
            self.logger.info("Creating view for flight data...")
            self.spark_manager.create_view(data, "flight")
            self.logger.info("View for flight data created successfully.")
        except Exception as e:
            self.logger.error(f"Error in create_view: {e}")
