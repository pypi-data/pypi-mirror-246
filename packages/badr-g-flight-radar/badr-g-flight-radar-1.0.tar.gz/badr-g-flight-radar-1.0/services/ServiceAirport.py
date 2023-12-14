from .ApiFlightRadar import ApiFlightRadar
from models.DataSchema import Airport
from .BaseService import BaseService


class ServiceAirport(BaseService):
    """
    Service class for handling airport-related operations.

    Inherits from BaseService and includes methods to fetch, process, save, and create views for airport data.

    Attributes:
        api_wrapper (ApiFlightRadar): Instance to interact with the FlightRadar24 API.
        logger (Logger): Logger instance for logging messages.
        spark_manager (SparkManager): Instance of SparkManager for handling Spark operations.
    """

    def __init__(self, api_wrapper: ApiFlightRadar, logger, spark_manager):
        """
        Initialize ServiceAirport with API wrapper, logger, and Spark manager.

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
        Fetch airport data using the Flight Radar API.

        Returns:
            List[Airport]: A list of Airport objects or an empty list if an error occurs.
        """
        try:
            self.logger.info("Fetching airport data...")
            airports = self.api_wrapper.get_airport_data()
            return airports
        except Exception as e:
            self.logger.error(f"Error in get_data: {e}")
            return []

    def process_data(self, data):
        """
        Processes the fetched airport data.

        Args:
            data: Raw airport data to be processed.

        Returns:
            DataFrame: Processed airport data in DataFrame format or None if error.
        """
        try:
            self.logger.info("Processing airport data...")
            if not data:
                self.logger.warning("No airport data to process.")
                return None

            df_airports = self.spark_manager.create_df(data, Airport.get_schema())
            df_airports = self.spark_manager.clean_df(df_airports)
            return df_airports
        except Exception as e:
            self.logger.error(f"Error in process_data: {e}")
            return None

    def save_data(self, data):
        """
        Saves the processed airport data.

        Args:
            data: Processed airport data to be saved.
        """
        try:
            if data is None:
                self.logger.warning("No airport data available to save.")
                return

            self.logger.info("Saving airport data...")
            self.spark_manager.save_df(data, "Airport", "airport")
            self.logger.info("Airport data saved successfully.")
        except Exception as e:
            self.logger.error(f"Error in save_data: {e}")

    def create_view(self, data):
        """
        Creates a view for the processed airport data for easier querying.

        Args:
            data: Processed airport data for which the view is to be created.
        """
        try:
            if data is None:
                self.logger.warning("No airport data available to create a view.")
                return

            self.logger.info("Creating view for airport data...")
            self.spark_manager.create_view(data, "airport")
            self.logger.info("View airport created successfully for airport data.")
        except Exception as e:
            self.logger.error(f"Error in create_view: {e}")
