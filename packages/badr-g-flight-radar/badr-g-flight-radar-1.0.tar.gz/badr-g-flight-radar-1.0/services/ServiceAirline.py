from models.DataSchema import Airline
from .ApiFlightRadar import ApiFlightRadar
from .SparkManager import SparkManager
from .BaseService import BaseService


class ServiceAirline(BaseService):
    """
    Service class for handling airline-related operations.

    Inherits from BaseService and includes methods to fetch, process, save, and create views for airline data.

    Attributes:
        api_wrapper (ApiFlightRadar): Instance to interact with FlightRadar24 API.
        logger (Logger): Logger instance for logging messages.
        spark_manager (SparkManager): Instance of SparkManager for handling Spark operations.
    """

    def __init__(
        self, api_wrapper: ApiFlightRadar, logger, spark_manager: SparkManager
    ):
        """
        Initialize ServiceAirline with API wrapper, logger, and Spark manager.

        Args:
            api_wrapper (ApiFlightRadar): Instance to interact with FlightRadar24 API.
            logger (Logger): Logger instance for logging messages.
            spark_manager (SparkManager): Instance of SparkManager for handling Spark operations.
        """
        self.api_wrapper = api_wrapper
        self.logger = logger
        self.spark_manager = spark_manager

    def get_data(self):
        """
        Fetch airline data using the Flight Radar API.

        Returns:
            List[Airline]: A list of Airline objects or an empty list if an error occurs.
        """
        try:
            self.logger.info("Fetching airline data...")
            airlines = self.api_wrapper.get_airlines_data()
            return airlines
        except Exception as e:
            self.logger.error(f"Error in get_data: {e}")
            return []

    def process_data(self, data):
        """
        Processes the fetched airline data.

        Args:
            data: Raw airline data to be processed.

        Returns:
            DataFrame: Processed airline data in DataFrame format or None if error.
        """
        try:
            self.logger.info("Processing airline data...")
            if not data:
                self.logger.warning("No airline data to process.")
                return None

            df_airlines = self.spark_manager.create_df(data, Airline.get_schema())
            df_airlines = self.spark_manager.clean_df(df_airlines)
            return df_airlines
        except Exception as e:
            self.logger.error(f"Error in process_data: {e}")
            return None

    def save_data(self, data):
        """
        Saves the processed airline data.

        Args:
            data: Processed airline data to be saved.
        """
        try:
            if data is None:
                self.logger.warning("No airline data available to save.")
                return

            self.logger.info("Saving airline data...")
            self.spark_manager.save_df(data, "Airline", "airline")
            self.logger.info("Airline data saved successfully.")
        except Exception as e:
            self.logger.error(f"Error in save_data: {e}")

    def create_view(self, data):
        """
        Creates a view for the processed airline data for easier querying.

        Args:
            data: Processed airline data for which the view is to be created.
        """
        try:
            if data is None:
                self.logger.warning("No airline data available to create a view.")
                return

            self.logger.info("Creating view for airline data...")
            self.spark_manager.create_view(data, "airline")
            self.logger.info("View airline created successfully for airline data.")
        except Exception as e:
            self.logger.error(f"Error in create_view: {e}")
