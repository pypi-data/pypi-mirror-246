import datetime
from pyspark.sql.functions import lit
import pandas as pd
from .BaseService import BaseService


class ServiceCountry(BaseService):
    """
    Service class for handling country-related operations.

    Inherits from BaseService and includes methods to fetch, process, save, and create views for country data.

    Attributes:
        spark_manager (SparkManager): Instance of SparkManager for handling Spark operations.
        logger (Logger): Logger instance for logging messages.
    """

    def __init__(self, spark_manager, logger):
        """
        Initialize ServiceCountry with Spark manager and logger.

        Args:
            spark_manager (SparkManager): Instance of SparkManager for handling Spark operations.
            logger (Logger): Logger instance for logging messages.
        """
        self.spark_manager = spark_manager
        self.logger = logger

    def get_data(self):
        """
        Fetch country data from a specified URL and save it locally.

        Returns:
            DataFrame: Country data as a DataFrame or None if an error occurs.
        """
        try:
            self.logger.info("Fetching country data...")
            url = "https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv"
            local_csv = "countries_codes_and_coordinates.csv"
            df_countries_codes = pd.read_csv(url)
            df_countries_codes.to_csv(local_csv, index=False)
            self.logger.info("Country data fetched and saved locally.")
            df_countries_codes = self.spark_manager.spark.read.csv(
                local_csv, header=True, inferSchema=True
            )
            return df_countries_codes
        except Exception as e:
            self.logger.error(f"Error in get_data: {e}")
            return None

    def process_data(self, data):
        """
        Processes the fetched country data.

        Args:
            data: Raw country data to be processed.

        Returns:
            DataFrame: Processed country data in DataFrame format or None if error.
        """
        try:
            self.logger.info("Processing country data...")
            if data is None:
                self.logger.warning("No country data to process.")
                return None

            selected_columns = ["Country", "Numeric code"]
            data = data.select(selected_columns)
            current_date = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            data = data.withColumn("Date", lit(current_date))
            df_countries = self.spark_manager.clean_countries_data(data)
            return df_countries
        except Exception as e:
            self.logger.error(f"Error in process_data: {e}")
            return None

    def save_data(self, data):
        """
        Saves the processed country data.

        Args:
            data: Processed country data to be saved.
        """
        try:
            if data is None:
                self.logger.warning("No country data available to save.")
                return

            self.logger.info("Saving country data...")
            self.spark_manager.save_df(data, "Country", "country")
            self.logger.info("Country data saved successfully.")
        except Exception as e:
            self.logger.error(f"Error in save_data: {e}")

    def create_view(self, data):
        """
        Creates a view for the processed country data for easier querying.

        Args:
            data: Processed country data for which the view is to be created.
        """
        try:
            if data is None:
                self.logger.warning("No country data available to create a view.")
                return

            self.logger.info("Creating view for country data...")
            self.spark_manager.create_view(data, "country_code")
            self.logger.info("View country_code created successfully for country data.")
        except Exception as e:
            self.logger.error(f"Error in create_view: {e}")
