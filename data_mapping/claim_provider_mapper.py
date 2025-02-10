# File: data_mapping/claim_provider_mapper.py

import logging
from data_mapping.mapping_rules import load_mapping_rules, apply_rules, validate_mapping

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def map_claim_to_provider(claim_data):
    """
    This function takes insurance claim data points as input and maps them to the respective providers
    based on predefined rules and data mappings. The function uses algorithms to process the input data
    and match claims correctly to their respective providers.

    :param claim_data: dict - Insurance claim data points
    :return: dict - mapping results
    """
    try:
        # Load mapping rules
        mapping_rules = load_mapping_rules()
        logger.info("Mapping rules loaded successfully.")

        # Apply mapping rules to the claim data
        provider_mapping = apply_rules(claim_data, mapping_rules)
        logger.info("Applied mapping rules to claims data.")

        # Validate the provider mapping results
        validation_status = validate_mapping(claim_data, provider_mapping)
        logger.info("Validated mapping results.")

        return {
            'status': 'success',
            'provider_mapping': provider_mapping,
            'validation_status': validation_status
        }

    except Exception as e:
        logger.error(f"Error while mapping claim to provider: {e}")
        return {
            'status': 'failure',
            'error': str(e)
        }
