import unittest
from unittest.mock import patch, MagicMock
from data_mapping.mapping_rules import load_mapping_rules, apply_rules, validate_mapping


class TestMappingRules(unittest.TestCase):

    @patch('data_mapping.mapping_rules.load_mapping_rules')
    def test_load_mapping_rules(self, mock_load):
        # Setup the mock to return predefined rules
        mock_rules = {
            "provider1": {"conditions": ["condition1", "condition2"]},
            "provider2": {"conditions": ["condition3"]}
        }
        mock_load.return_value = mock_rules
        
        # Call the load_mapping_rules function
        rules = load_mapping_rules()
        
        # Assert loading rules is not None and is as expected
        self.assertIsNotNone(rules)
        self.assertDictEqual(rules, mock_rules)
        mock_load.assert_called_once()

    @patch('data_mapping.mapping_rules.load_mapping_rules')
    def test_apply_rules(self, mock_load):
        # Setup the mock to return predefined rules
        mock_rules = {
            "provider1": {"conditions": ["condition1", "condition2"]},
            "provider2": {"conditions": ["condition3"]}
        }
        mock_load.return_value = mock_rules
        
        # Sample claim data points to be matched
        claim_data_1 = {"claimed_condition": "condition1"}
        claim_data_2 = {"claimed_condition": "condition3"}
        
        # Apply rules
        matched_provider_1 = apply_rules(claim_data_1)
        matched_provider_2 = apply_rules(claim_data_2)
        
        # Check if the claims are mapped as per the rules
        self.assertEqual(matched_provider_1, "provider1")
        self.assertEqual(matched_provider_2, "provider2")
        mock_load.assert_called_once()

    def test_validate_mapping(self):
        # Sample claim data points and mappings to be validated
        claim_data = {"claimed_condition": "condition1"}
        provider_mapping = "provider1"

        # Validate correct mapping
        is_valid = validate_mapping(claim_data, provider_mapping)
        self.assertTrue(is_valid)

        # Validate incorrect mapping
        incorrect_provider_mapping = "provider2"
        is_not_valid = validate_mapping(claim_data, incorrect_provider_mapping)
        self.assertFalse(is_not_valid)


if __name__ == "__main__":
    unittest.main()
