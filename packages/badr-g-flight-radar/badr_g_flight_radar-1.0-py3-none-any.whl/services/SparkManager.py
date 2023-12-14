from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import regexp_replace
import datetime
import glob
import os


class SparkManager:
    """
    Class for managing Spark operations including creating, cleaning, saving DataFrames, and creating views.

    Attributes:
        logger (Logger): An instance of a logging class to record log messages.
        spark (SparkSession): A SparkSession instance.
    """

    def __init__(self, logger, app_name="FlightRadarETL"):
        """
        Initialize the SparkManager class.

        Args:
            logger (Logger): An instance of a logging class to record log messages.
            app_name (str): The name of the Spark application, default is 'FlightRadarETL'.
        """

        self.logger = logger  # Assign the passed logger to the class.
        # Initialize a SparkSession with the given application name.
        self.spark = SparkSession.builder.appName(app_name).getOrCreate()
        # Log the successful creation of the Spark Session.
        self.logger.info("Spark Session Created with app name: {}".format(app_name))

    def create_df(self, data, schema) -> DataFrame:
        """
        Creates a DataFrame from the given data and schema.

        Args:
            data: Data to be loaded into the DataFrame.
            schema: Schema to be applied to the DataFrame.

        Returns:
            DataFrame: The created DataFrame or None in case of an error.
        """

        try:
            self.logger.info("Creating DataFrame.")
            # Create a DataFrame with the given data and schema.
            df = self.spark.createDataFrame(data, schema)
            self.logger.info("DataFrame created successfully.")
            # Show the created DataFrame for verification.
            df.show()
            return df  # Return the created DataFrame.
        except Exception as e:
            # Log any exceptions that occur during DataFrame creation.
            self.logger.error(
                "An error occurred while creating the DataFrame: {}".format(e)
            )
            return None  # Return None in case of an error.

    def clean_df(self, df: DataFrame) -> DataFrame:
        """
        Cleans the given DataFrame by replacing 'N/A' and empty strings with None and dropping rows with null values.

        Args:
            df (DataFrame): The DataFrame to be cleaned.

        Returns:
            DataFrame: The cleaned DataFrame or None in case of an error.
        """

        try:
            self.logger.info("Cleaning DataFrame.")
            # Replace 'N/A' and empty strings with None and drop rows with null values.
            df = df.replace("N/A", None).replace("", None).na.drop()
            self.logger.info("DataFrame cleaned successfully.")
            # Show the cleaned DataFrame for verification.
            df.show()
            return df  # Return the cleaned DataFrame.
        except Exception as e:
            # Log any exceptions that occur during DataFrame cleaning.
            self.logger.error(
                "An error occurred while cleaning the DataFrame: {}".format(e)
            )
            return None  # Return None in case of an error.

    def clean_countries_data(self, df):
        """
        Cleans the DataFrame containing countries data. Specifically, it cleans and renames the 'Numeric code' column.

        Args:
            df (DataFrame): The DataFrame containing countries data.

        Returns:
            DataFrame: The cleaned DataFrame or None in case of an error.
        """

        try:
            # Clean the 'Numeric code' column by removing unwanted characters and rename the column.
            df = df.withColumn(
                "Numeric code", regexp_replace("Numeric code", '" ""', "")
            )
            df = df.withColumn(
                "Numeric code", regexp_replace("Numeric code", '"""', "")
            )
            df = df.withColumnRenamed("Numeric code", "Numeric_code")
            # Call the generic clean_df method to further clean the DataFrame.
            df = self.clean_df(df)
            # Show the cleaned DataFrame for verification.
            df.show()
            self.logger.info("Countries DataFrame cleaned successfully.")
            return df  # Return the cleaned DataFrame.
        except Exception as e:
            # Log any exceptions that occur during the cleaning process.
            self.logger.error(f"Error occurred while cleaning countries data: {e}")
            return None  # Return None in case of an error.

    def clean_regional_df(self, df):
        """
        Cleans the DataFrame containing regional flight data. Specifically, replaces '0' with None and performs further cleaning.

        Args:
            df (DataFrame): The DataFrame containing regional flight data.

        Returns:
            DataFrame: The cleaned DataFrame or None in case of an error.
        """

        try:
            # Log the start of the cleaning process for the regional DataFrame.
            self.logger.info("Replacing '0' with None in the regional DataFrame.")
            # Replace '0' with None in the DataFrame.
            df = df.replace("0", None)

            # Perform further cleaning using the generic clean_df method.
            df = self.clean_df(df)

            # Log the successful completion of cleaning.
            self.logger.info("Successfully cleaned the regional DataFrame.")
            return df  # Return the cleaned DataFrame.
        except Exception:
            # Log any exceptions that occur during the cleaning process.
            self.logger.error(
                "An error occurred while cleaning the regional DataFrame: ",
                exc_info=True,
            )
            return None  # Return None in case of an error.

    def save_df(self, df: DataFrame, base_dir: str, file_prefix: str):
        """
        Saves the given DataFrame as an ORC file in a specified directory with a specific file name format.

        Args:
            df (DataFrame): The DataFrame to be saved.
            base_dir (str): The base directory where the file will be saved.
            file_prefix (str): The prefix for the saved file's name.
        """

        try:
            # Log the start of the DataFrame coalescing process.
            self.logger.info("Coalescing the DataFrame to a single partition.")
            # Coalesce the DataFrame to a single partition for a single output file.
            df_single_partition = df.coalesce(1)

            # Determine the output path and file name based on current date and provided base directory.
            now = datetime.datetime.utcnow()

            output_path = f"results/{base_dir}/rawzone/tech_year={now.year}/tech_month={now.strftime('%Y-%m')}/tech_day={now.strftime('%Y-%m-%d')}/"
            self.logger.info(f"Defined output path: {output_path}")

            # Save the DataFrame as an ORC file in the defined output path.
            self.logger.info("Saving the DataFrame as an ORC file.")
            df_single_partition.write.mode("overwrite").orc(output_path)

            # Log the successful saving of the DataFrame.
            self.logger.info(
                "DataFrame saved successfully in ORC format at " + output_path
            )
            file_path = glob.glob(f"{output_path}/part-*.orc")[0]

            # Create a new file name with the provided file prefix and current timestamp.
            time_string = now.strftime("%Y%m%d%H%M%S%f")[:16]
            new_file_path = f"{output_path}/{file_prefix}{time_string}.orc"
            # Rename the saved file to the new file name.
            self.logger.info("Renaming the saved file.")
            os.rename(file_path, new_file_path)

            # Remove any CRC files generated during the saving process.
            file_path_crc = glob.glob(f"{output_path}/.part-*.orc.crc")[0]
            os.remove(file_path_crc)
            self.logger.info("DataFrame saved and file renamed successfully.")
        except Exception:
            # Log any exceptions that occur during the saving process.
            self.logger.error("An error occurred in save_df function.", exc_info=True)

    def create_view(self, df: DataFrame, view_name: str):
        """
        Creates a temporary view of the DataFrame for SQL-like querying.

        Args:
            df (DataFrame): The DataFrame for which the view will be created.
            view_name (str): The name of the temporary view.
        """

        try:
            # Log the start of the view creation process.
            self.logger.info("Creating a temporary view for {}.".format(view_name))
            # Create or replace a temporary view with the given name.
            df.createOrReplaceTempView(view_name)
            # Log the successful creation of the view.
            self.logger.info(
                "Temporary view for {} created successfully.".format(view_name)
            )
        except Exception as e:
            # Log any exceptions that occur during the view creation process.
            self.logger.error(
                "An error occurred while creating temporary views: {}".format(e)
            )
