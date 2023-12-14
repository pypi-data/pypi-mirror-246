from .ApiFlightRadar import ApiFlightRadar
from .BaseService import BaseService
from models.DataSchema import Regional


class ServiceRegional(BaseService):
    """
    Service class for handling regional flight-related operations.

    Inherits from BaseService and includes methods to fetch, process, save, and create views for regional flight data.

    Attributes:
        api_wrapper (ApiFlightRadar): Instance to interact with the FlightRadar24 API.
        logger (Logger): Logger instance for logging messages.
        spark_manager (SparkManager): Instance of SparkManager for handling Spark operations.
    """

    def __init__(self, api_wrapper: ApiFlightRadar, logger, spark_manager):
        """
        Initialize ServiceRegional with API wrapper, logger, and Spark manager.

        Args:
            api_wrapper (ApiFlightRadar): Instance to interact with the FlightRadar24 API.
            logger (Logger): Logger instance for logging messages.
            spark_manager (SparkManager): Instance of SparkManager for handling Spark operations.
        """
        self.api_wrapper = api_wrapper
        self.logger = logger
        self.spark_manager = spark_manager

    def get_data(self):
        """
        Fetch regional flight data using the Flight Radar API.

        Returns:
            List[Regional]: A list of Regional flight objects or an empty list if an error occurs.
        """
        try:
            self.logger.info("Fetching regional flight data...")
            regional_flights = self.api_wrapper.get_regional_flights()
            return regional_flights
        except Exception as e:
            self.logger.error(f"Error in get_data: {e}")
            return []

    def process_data(self, data):
        """
        Processes the fetched regional flight data.

        Args:
            data: Raw regional flight data to be processed.

        Returns:
            DataFrame: Processed regional flight data in DataFrame format or None if error.
        """
        try:
            self.logger.info("Processing regional flight data...")
            if not data:
                self.logger.warning("No regional flight data to process.")
                return None

            df_regional_flights = self.spark_manager.create_df(
                data, Regional.get_schema()
            )
            df_regional_flights = self.spark_manager.clean_regional_df(
                df_regional_flights
            )
            return df_regional_flights
        except Exception as e:
            self.logger.error(f"Error in process_data: {e}")
            return None

    def save_data(self, data):
        """
        Saves the processed regional flight data.

        Args:
            data: Processed regional flight data to be saved.
        """
        try:
            if data is None:
                self.logger.warning("No regional flight data available to save.")
                return

            self.logger.info("Saving regional flight data...")
            self.spark_manager.save_df(data, "Regional", "regional")
            self.logger.info("Regional flight data saved successfully.")
        except Exception as e:
            self.logger.error(f"Error in save_data: {e}")

    def create_view(self, data):
        """
        Creates a view for the processed regional flight data for easier querying.

        Args:
            data: Processed regional flight data for which the view is to be created.
        """
        try:
            if data is None:
                self.logger.warning(
                    "No regional flight data available to create a view."
                )
                return

            self.logger.info("Creating view for regional flight data...")
            self.spark_manager.create_view(data, "regional")
            self.logger.info(
                "View regional created successfully for regional flight data."
            )
        except Exception as e:
            self.logger.error(f"Error in create_view: {e}")
