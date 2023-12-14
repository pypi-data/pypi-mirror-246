from abc import ABC, abstractmethod


class BaseService(ABC):
    """
    Abstract base class for defining common service methods.
    This class serves as a template for other specific service classes.
    """

    @abstractmethod
    def get_data(self):
        """
        Abstract method to get data.
        This method should be implemented by subclasses to define
        how data is retrieved.
        """
        pass

    @abstractmethod
    def process_data(self, data):
        """
        Abstract method to process data.
        This method should be implemented by subclasses to define
        how the retrieved data is processed.
        :param data: The data to be processed.
        """
        pass

    @abstractmethod
    def save_data(self, data):
        """
        Abstract method to save data.
        This method should be implemented by subclasses to define
        how the processed data is saved.
        :param data: The processed data to be saved.
        """
        pass

    @abstractmethod
    def create_view(self, data):
        """
        Abstract method to create a view for the data.
        This method should be implemented by subclasses to define
        how a view for the data is created for easier querying.
        :param data: The data for which the view is to be created.
        """
        pass
