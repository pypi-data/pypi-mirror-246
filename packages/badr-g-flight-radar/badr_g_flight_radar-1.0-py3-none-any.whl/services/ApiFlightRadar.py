from FlightRadar24 import FlightRadar24API, errors
import datetime
import time
from typing import List
from FlightRadar24.errors import CloudflareError
from models.DataSchema import Flight, Airline, Airport, Regional
import pandas as pd


class ApiFlightRadar:
    """
    Class for interacting with the FlightRadar24 API to fetch and process flight data.

    Attributes:
        logger (Logger): An instance of a logging class for log messages.
        api (FlightRadar24API): An instance of the FlightRadar24API.
    """

    def __init__(self, logger, flight_tracker_limit=10):
        """
        Initialize the ApiFlightRadar class.

        Args:
            logger (Logger): An instance of a logging class to record log messages.
            flight_tracker_limit (int): Default limit for the number of flights to track.
        """
        self.logger = logger  # Assign the passed logger to the class.
        self.api = FlightRadar24API()  # Initialize the FlightRadar24 API.
        # Call the init_api method to configure the API.
        self.init_api(flight_tracker_limit)

    def init_api(self, flight_tracker_limit):
        """
        Initializes and configures the FlightRadar24 API.

        Args:
            flight_tracker_limit (int): Limit for the number of flights to track.
        """

        try:
            # Retrieve the current flight tracker configuration.
            flight_tracker = self.api.get_flight_tracker_config()
            flight_tracker.limit = flight_tracker_limit  # Set the new limit.
            # Update the API with the new configuration.
            self.api.set_flight_tracker_config(flight_tracker)
            # Log the successful initialization.
            self.logger.info(
                "FlightRadar24 API Initialized with tracker limit: {}".format(
                    flight_tracker_limit
                )
            )
        except Exception as e:
            # Log any exceptions that occur during initialization.
            self.logger.error("Error initializing FlightRadar24 API: {}".format(e))

    def get_flights_data(self) -> List[Flight]:
        """
        Fetches and processes flight data from the FlightRadar24 API.

        Returns:
            List[Flight]: A list of Flight objects with detailed information.
        """
        try:
            # Retrieve the list of current flights.
            flights = self.api.get_flights()
            # Initialize an empty list to store Flight objects.
            data: List[Flight] = []
            now = datetime.datetime.utcnow()  # Get the current UTC time.

            for flight in flights:
                try:
                    # For each flight, retrieve detailed information.
                    flight_details = self.api.get_flight_details(flight)
                    # Set the detailed info to the flight object.
                    flight.set_flight_details(flight_details)

                    # Create a Flight object with the retrieved details.
                    flight_obj = Flight(
                        status=not bool(flight.on_ground),
                        epoch=flight.time,
                        icao_airline=flight.airline_icao,
                        origine=flight.origin_airport_icao,
                        destination=flight.destination_airport_icao,
                        model=flight.aircraft_model,
                        aircraft_code=flight.aircraft_code,
                        country_id=flight.aircraft_country_id,
                        date=now.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                    # Add the Flight object to the list.
                    data.append(flight_obj)
                    # Log the successful retrieval and processing of the flight.
                    self.logger.info(
                        "Successfully retrieved and processed flight: {}".format(flight)
                    )
                except Exception as e:
                    # Log any errors encountered during the processing of a flight.
                    self.logger.error("Error processing flight data: {}".format(e))
                    # Wait for 5 seconds before processing the next flight.
                    time.sleep(5)

            return data  # Return the list of processed Flight objects.
        except Exception as e:
            # Log any errors encountered during the fetching of flights data.
            self.logger.error("Error fetching flights data: {}".format(e))
            return []  # Return an empty list in case of an error.

    def get_airlines_data(self) -> List[Airline]:
        """
        Retrieves and processes airlines data from the FlightRadar24 API.

        Returns:
            List[Airline]: A list of Airline objects.
        """
        try:
            airlines_data = self.api.get_airlines()
            print("qsdfghjkl", airlines_data)
            # Fetch airlines data from the API.
            # Initialize an empty list for Airline objects.
            airlines: List[Airline] = []
            now = datetime.datetime.utcnow()  # Get the current UTC time.

            for airline in airlines_data:
                # Create an Airline object for each entry in the airlines data.
                airline_obj = Airline(
                    airline["Name"], airline["ICAO"], now.strftime("%Y-%m-%d %H:%M:%S")
                )
                # Add the Airline object to the list.
                airlines.append(airline_obj)
            # Log the successful retrieval and update of airlines data.
            self.logger.info("Airlines data retrieved and updated successfully.")
            return airlines  # Return the list of Airline objects.
        except Exception as e:
            # Log any errors encountered during the retrieval of airlines data.
            self.logger.error("Error in get_airlines_data: {}".format(e))
            return []  # Return an empty list in case of an error.

    def get_regional_flights(self) -> List[Regional]:
        """
        Retrieves and processes regional flight data based on different zones.

        Returns:
            List[Regional]: A list of Regional objects.
        """
        try:
            zones = self.api.get_zones()  # Fetch zones data from the API.
            now = datetime.datetime.utcnow()  # Get the current UTC time.
            # Initialize an empty list for Regional objects.
            res: List[Regional] = []

            for zone in zones:
                try:
                    # Get the bounds for the current zone.
                    bounds = self.api.get_bounds(zones[zone])
                    # Fetch flights within these bounds.
                    flights = self.api.get_flights(bounds=bounds)

                    for flight in flights:
                        try:
                            # For each flight, retrieve detailed information.
                            flight_details = self.api.get_flight_details(flight)
                            # Set the detailed info to the flight object.
                            flight.set_flight_details(flight_details)

                            # Create a Regional object with the retrieved details.
                            regional_obj = Regional(
                                not bool(flight.on_ground),
                                flight.time,
                                flight.airline_icao,
                                zone,
                                flight.time_details.get("scheduled").get("departure"),
                                flight.time_details.get("scheduled").get("arrival"),
                                flight.origin_airport_icao,
                                flight.destination_airport_icao,
                                now.strftime("%Y-%m-%d %H:%M:%S"),
                            )
                            # Add the Regional object to the list.
                            res.append(regional_obj)
                        except errors.CloudflareError as e:
                            # Log and handle Cloudflare errors specifically.
                            self.logger.error(
                                "CloudflareError encountered: {}".format(e)
                            )
                            time.sleep(1)  # Wait for 1 second before retrying.
                except Exception as e:
                    # Log any errors encountered during the processing of zone data.
                    self.logger.error("Error processing zone data: {}".format(e))

            return res  # Return the list of Regional objects.
        except Exception as e:
            # Log any errors encountered during the fetching of regional flights data.
            self.logger.error("Error fetching regional flights data: {}".format(e))
            return []  # Return an empty list in case of an error.

    def get_airport_data(self) -> List[Airport]:
        """
        Retrieves and processes airport data from the FlightRadar24 API.

        Returns:
            List[Airport]: A list of Airport objects.
        """
        airports = self.api.get_airports()  # Fetch the list of airports from the API.
        # Initialize an empty list for Airport objects.
        data: List[Airport] = []

        for airport in airports:
            try:
                # Create an Airport object for each entry in the airports data.
                airport_obj = Airport(airport.icao, airport.name)
                data.append(airport_obj)  # Add the Airport object to the list.
                # Log the successful retrieval and processing of the airport.
                self.logger.info(
                    f"Successfully retrieved and processed airport: {airport}"
                )
            except Exception as e:
                # Log any errors encountered during the processing of an airport.
                self.logger.error(f"Error while processing airport data: {e}")

        return data  # Return the list of Airport objects.

    def fetch_countries_data(self):
        """
        Retrieves country data from a given URL and saves it as a CSV file.
        """
        url = "https://gist.githubusercontent.com/tadast/8827699/raw/f5cac3d42d16b78348610fc4ec301e9234f82821/countries_codes_and_coordinates.csv"

        try:
            # Load the CSV file from the URL.
            df_countries_codes = pd.read_csv(url)
            self.logger.info("CSV file loaded successfully.")
            # Save the loaded data to a local CSV file.
            df_countries_codes.to_csv(
                "countries_codes_and_coordinates.csv", index=False
            )
            self.logger.info("CSV file saved successfully.")
        except Exception as e:
            # Log any errors encountered during the loading and saving of the CSV file.
            self.logger.error(f"Error occurred while loading CSV file: {e}")

    def calculate_distance_sql(self, origine, destination):
        """
        Calculates the distance between two airports using SQL.

        Args:
            origine (str): ICAO code of the origin airport.
            destination (str): ICAO code of the destination airport.

        Returns:
            float: The calculated distance or None if the calculation fails.
        """
        retry_count = 0  # Counter for the number of retries.
        max_retries = 5  # Maximum number of retries.
        delay = 2  # Initial delay between retries in seconds.

        while retry_count < max_retries:
            try:
                # Log the attempt to fetch airport details.
                self.logger.info(
                    f"Attempt {retry_count + 1}: Fetching airport details for {origine} and {destination}."
                )
                # Fetch airport details for origin and destination.
                dest = self.api.get_airport(origine)
                origin = self.api.get_airport(destination)
                self.logger.info("Successfully fetched airport details.")
                # Return the calculated distance.
                return dest.get_distance_from(origin)

            except CloudflareError as e:
                # Handle Cloudflare errors specifically, logging the error and retrying after a delay.
                self.logger.warning(
                    f"CloudflareError encountered on attempt {retry_count + 1}: {e}. Retrying after {delay} seconds."
                )
                time.sleep(delay)  # Wait for the specified delay.
                retry_count += 1  # Increment the retry count.
                delay *= 2  # Double the delay for the next retry.

        # Log an error if the distance calculation fails after all retries.
        self.logger.error("Failed to calculate distance after maximum retries.")
        return None
