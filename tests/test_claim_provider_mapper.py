import unittest
from unittest.mock import patch, MagicMock
from data_mapping.claim_provider_mapper import map_claim_to_provider

class TestClaimProviderMapper(unittest.TestCase):

    @patch('data_mapping.claim_provider_mapper.load_mapping_rules')
    @patch('data_mapping.claim_provider_mapper.apply_rules')
    def test_map_claim_to_provider(self, mock_apply_rules, mock_load_mapping_rules):
        # Sample input data points
        sample_claim_data = {
            "claim_id": "12345",
            "patient_id": "98765",
            "provider_id": None,  # This will be populated by the mapper
            "diagnosis_code": "A00",
            "treatment_code": "001"
        }

        # Expected provider data to be returned by apply_rules function
        expected_provider = {
            "provider_id": "prov123",
            "name": "Provider One",
            "specialty": "General Practice"
        }

        # Mock implementations
        mock_load_mapping_rules.return_value = {'A00': 'prov123'}
        mock_apply_rules.return_value = expected_provider

        # Call function under test
        result = map_claim_to_provider(sample_claim_data)

        # Check that the rules were loaded
        mock_load_mapping_rules.assert_called_once()

        # Check that apply_rules was called with the loaded rules and sample claim data
        mock_apply_rules.assert_called_once_with(sample_claim_data, {'A00': 'prov123'})

        # Verify the mapping result
        self.assertEqual(result['provider_id'], expected_provider['provider_id'])
        self.assertEqual(result['name'], expected_provider['name'])
        self.assertEqual(result['specialty'], expected_provider['specialty'])

if __name__ == '__main__':
    unittest.main()
