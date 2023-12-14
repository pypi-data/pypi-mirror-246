import unittest
from unittest.mock import patch
from services.ApiFlightRadar import ApiFlightRadar
from services.utils.LoggerManager import LoggerManager


class TestApiFlightRadar(unittest.TestCase):
    @patch("FlightRadar24.FlightRadar24API.get_airlines")
    def test_get_airlines_data(self, mock_get_airlines):
        mock_airlines_data = [
            {"Name": "Airline A", "ICAO": "ABA"},
            {"Name": "Airline B", "ICAO": "BBB"},
        ]
        mock_get_airlines.return_value = mock_airlines_data

        logger_manager = LoggerManager("my_log.log")
        logger = logger_manager.get_logger()
        api_flight_radar = ApiFlightRadar(logger)

        result = api_flight_radar.get_airlines_data()
        self.assertEqual(len(result), len(mock_airlines_data))
        for airline_obj, expected_data in zip(result, mock_airlines_data):
            self.assertEqual(airline_obj.name, expected_data["Name"])
            self.assertEqual(airline_obj.icao, expected_data["ICAO"])


if __name__ == '__main__':
    unittest.main()
