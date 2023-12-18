import unittest
import pandas as pd
import numpy as np
from scipy.fft import fft

# Import data
# from data_module import data


class data_processing:
    def clean_data(self, data):
        """
        Removes noise or irrelevant information from the data.
        Assumes data is a pandas DataFrame.
        """
        # Example: Remove columns with more than 50% missing values
        cleaned_data = data.dropna(axis=1, thresh=len(data) * 0.5)
        return cleaned_data

    def normalize_data(self, data):
        """
        Normalizes the data using Min-Max scaling.
        Assumes data is a pandas DataFrame.
        """
        normalized_data = (data - data.min()) / (data.max() - data.min())
        return normalized_data

    def transform_data(self, data, method):
        """
        Applies various transformations to the data.
        Currently supports: Fourier transform.
        Assumes data is a pandas DataFrame.
        """
        if method.lower() == "fourier":
            transformed_data = fft(data.values)
            return transformed_data
        else:
            raise NotImplementedError("Transformation method not supported.")


# Example usage
# dp = data_processing()
# cleaned = dp.clean_data(pd.DataFrame(...))
# normalized = dp.normalize_data(pd.DataFrame(...))
# transformed = dp.transform_data(pd.DataFrame(...), 'Fourier')