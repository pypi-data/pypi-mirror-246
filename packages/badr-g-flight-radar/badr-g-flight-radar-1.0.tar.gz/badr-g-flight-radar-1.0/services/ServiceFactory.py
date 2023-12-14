from .ServiceAirline import ServiceAirline
from .ServiceAirport import ServiceAirport
from .ServiceCountries import ServiceCountry
from .ServiceFlight import ServiceFlight
from .ServiceRegionalFlight import ServiceRegional


class ServiceFactory:
    """
    Factory class for creating instances of various service classes.

    This class follows the Factory Design Pattern to create instances of services like
    Flight, Airline, Airport, Regional, and Country services.

    Attributes:
        api_wrapper: Instance to interact with the FlightRadar24 API.
        logger: Logger instance for logging messages.
        spark_manager: Instance of SparkManager for handling Spark operations.
    """

    def __init__(self, api_wrapper, logger, spark_manager):
        """
        Initialize the ServiceFactory with API wrapper, logger, and Spark manager.

        Args:
            api_wrapper: Instance to interact with the FlightRadar24 API.
            logger: Logger instance for logging messages.
            spark_manager: Instance of SparkManager for handling Spark operations.
        """
        self.api_wrapper = api_wrapper
        self.logger = logger
        self.spark_manager = spark_manager

    def get_service(self, service_type):
        """
        Get an instance of a service based on the specified service type.

        Args:
            service_type (str): The type of service to create ('flight', 'airline', 'airport', 'regional', 'country').

        Returns:
            An instance of the requested service.

        Raises:
            ValueError: If the service type is not recognized.
        """
        if service_type == "flight":
            return ServiceFlight(self.api_wrapper, self.logger, self.spark_manager)
        elif service_type == "airline":
            return ServiceAirline(self.api_wrapper, self.logger, self.spark_manager)
        elif service_type == "airport":
            return ServiceAirport(self.api_wrapper, self.logger, self.spark_manager)
        elif service_type == "regional":
            return ServiceRegional(self.api_wrapper, self.logger, self.spark_manager)
        elif service_type == "country":
            return ServiceCountry(self.spark_manager, self.logger)
        else:
            raise ValueError(f"Service type '{service_type}' is not recognized")
