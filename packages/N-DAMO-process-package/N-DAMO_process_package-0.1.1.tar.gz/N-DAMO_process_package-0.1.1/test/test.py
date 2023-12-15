import unittest
import os
import pandas as pd
import numpy as np
import tellurium as te
from unittest.mock import patch, MagicMock, call
from function import get_data, methane_production, get_data_for_Bunsen_coefficient, Temperature_conversion, Bunsen_coefficient, dissolved_methane, molar_dissolved_methane, check_N_DAMO_process, plot_model, process_and_plot

class TestDataFunctions(unittest.TestCase):
    def test_get_data(self):
        # Test get_data function for COD and BOD
        excel_file = "test_data.xlsx"
        sample_data = {'COD': [1.0, 2.0, 3.0], 'BOD': [3000, 5.0, 6.0]}
        pd.DataFrame(sample_data).to_excel(excel_file, index=False)
        self.assertTrue(os.path.isfile(excel_file), f"File '{excel_file}' does not exist.")
        COD, BOD = get_data(excel_file)
        self.assertEqual(list(COD), [1.0, 2.0, 3.0])
        self.assertEqual(list(BOD), [3000, 5.0, 6.0])

    def test_methane_production(self):
        # Test methane_production function
        BOD_values = np.array([5.0, 2.0, 3.0])
        expected_result = np.array([bod * 0.35 for bod in BOD_values])
        result = methane_production(BOD_values)
        np.testing.assert_array_equal(result, expected_result)

    def test_get_data_for_Bunsen_coefficient(self):
        # Provide a sample Excel file for testing
        excel_file = "test_data2.xlsx"

        # Create a DataFrame with sample data
        sample_data = {'temperature ave': [17, 28, 14], 'Salinity %': [0.08, 0.3, 0.24]}
        pd.DataFrame(sample_data).to_excel(excel_file, index=False)

        # Check if the file exists after creating it
        self.assertTrue(os.path.isfile(excel_file), f"File '{excel_file}' does not exist.")

        # Test the get_data_for_Bunsen_coefficient function
        Temperature, Salinity = get_data_for_Bunsen_coefficient(excel_file)

        # Assert that the returned values match the expected values
        self.assertEqual(list(Temperature), [17, 28, 14])
        self.assertEqual(list(Salinity), [0.08, 0.3, 0.24])
    
   
    def test_Temperature_conversion(self):
        # Test temperature conversion function
        sample_temperature_values = np.array([12, 11, 6])
        temperature_expected_result = np.array([temperature + 273.15 for temperature in sample_temperature_values])
        temperature_result = Temperature_conversion(sample_temperature_values)
        np.testing.assert_array_equal(temperature_result, temperature_expected_result)

    def test_Bunsen_coefficient(self):
        # Sample data for testing
        sample_salinity = np.array([0.05, 0.13, 0.40])
        sample_temperature = np.array([307.5, 318.2, 293])

        # Expected result based on the function's calculation
        Bunseon_coefficient_expected_result= np.exp(
            -67.1962 + 99.1624 * (100 / sample_temperature) +
            27.9015 * np.log(sample_temperature / 100) +
            sample_salinity * (-0.072909 + 0.041674 * (sample_temperature / 100) - 0.0064603 * ((sample_temperature / 100) ** 2))
        )

        # Call the function and compare the result
        result = Bunsen_coefficient(sample_salinity, sample_temperature)
        np.testing.assert_array_equal(result, Bunseon_coefficient_expected_result)

    def test_dissolved_methane(self):
        # Sample data for testing
        sample_Bunsen_coefficient = np.array([0.03, 0.4, 0.27])
        sample_methane_production = np.array([1.0, 0.3, 9.2])

        # Expected result based on the function's calculation
        dissolved_methane_expected_result = sample_Bunsen_coefficient * sample_methane_production

        # Call the function and compare the result
        result = dissolved_methane(sample_Bunsen_coefficient, sample_methane_production)
        np.testing.assert_array_equal(result, dissolved_methane_expected_result)

    def test_molar_dissolved_methane(self):
        # Sample data for testing
        sample_dissolved_methane = np.array([34, 12, 5])
        sample_converted_temperature = np.array([331, 320, 298.5])

        # Expected result based on the function's calculation
        molar_dissolved_methane_expected_result = sample_dissolved_methane / (0.082 * sample_converted_temperature)

        # Call the function and compare the result
        result = molar_dissolved_methane(sample_dissolved_methane, sample_converted_temperature)
        np.testing.assert_array_equal(result, molar_dissolved_methane_expected_result)
        
    def test_check_N_DAMO_process(self):
        # Test when N-DAMO process exists (molar_dissolved_methane > 1)
        molar_dissolved_methane_exists = np.array([1.5, 0.8, 1.2])
        result_exists = check_N_DAMO_process(molar_dissolved_methane_exists)
        self.assertEqual(result_exists, "N-DAMO process exists.")

        # Test when N-DAMO process does not exist (molar_dissolved_methane <= 1)
        molar_dissolved_methane_does_not_exist = np.array([0.5, 0.8, 1.0])
        result_does_not_exist = check_N_DAMO_process(molar_dissolved_methane_does_not_exist)
        self.assertEqual(result_does_not_exist, "N-DAMO process does not exist.")

class TestYourModule(unittest.TestCase):
    @patch('function.te.loada')
    def test_plot_model(self, mock_loada):
        # Mocking loada to return a MagicMock object
        mock_loada.return_value = MagicMock()

        # Define a model string for testing
        model_str = "test_model_string"

        # Ensure the function does not raise any exceptions
        try:
            plot_model(model_str, backend="test_backend")
        except Exception as e:
            self.fail(f"plot_model raised an exception: {e}")

        # Verify that loada was called with the correct argument
        mock_loada.assert_called_once_with(model_str)

        # Verify that the simulate and plot functions were called on the MagicMock object
        mock_loada.return_value.simulate.assert_called_once_with(0, 24, 200)
        mock_loada.return_value.plot.assert_called_once_with(
            mock_loada.return_value.simulate.return_value,
            title="N-DAMO process",
            show=True,
            backend="test_backend"
        )

    def test_process_and_plot(self):
        # Define molar_dissolved_methane_values for testing
        molar_dissolved_methane_values = np.array([0.5])

        # Mock the print function to capture printed output
        with patch('builtins.print') as mock_print:
            process_and_plot(molar_dissolved_methane_values, ratio=0.3)

        # Verify that the print function was called with the correct message
        calls = [call[0] for call in mock_print.call_args_list]
        expected_message = "N-DAMO process does not exist. Ending the process."
        self.assertIn(expected_message, calls[0])  # Access the first element of the tuple
if __name__ == '__main__':
    unittest.main()


