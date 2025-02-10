import json
import logging

# Simple logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
RULES_FILE_PATH = 'config/rules.json'  # Path to the JSON file with the mapping rules

def load_mapping_rules():
    """
    Load the predefined rules and mapping data necessary to map claims to providers.
    This includes reading from configuration files or databases to get the mapping criteria.
    
    Returns:
        dict: A dictionary containing the rules and mapping data.
    """
    try:
        with open(RULES_FILE_PATH, 'r') as file:
            rules = json.load(file)
            logger.info("Mapping rules loaded successfully.")
            return rules
    except FileNotFoundError:
        logger.error(f"Rules file not found: {RULES_FILE_PATH}")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from the rules file: {RULES_FILE_PATH}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred while loading rules: {str(e)}")
        raise

def apply_rules(claim_data, rules):
    """
    Apply the loaded mapping rules to the given claim data points to determine the correct provider.
    
    Args:
        claim_data (dict): The claim data points to be mapped.
        rules (dict): The loaded mapping rules.
    
    Returns:
        str: The identifier of the mapped provider.
    """
    try:
        for rule in rules.get('rules', []):
            if all(claim_data.get(key) == value for key, value in rule['criteria'].items()):
                logger.info(f"Claim mapped to provider: {rule['provider']}")
                return rule['provider']
        logger.warning("No matching provider found for claim data.")
        return None
    except Exception as e:
        logger.error(f"Error applying rules to claim data: {str(e)}")
        raise

def validate_mapping(claim_data, provider_data):
    """
    Validate the mapping to ensure the claim is accurately matched to the provider with minimal errors or mismatches.
    It will also log any exceptions or mismatches found.
    
    Args:
        claim_data (dict): The claim data points that were mapped.
        provider_data (dict): The provider data points that claim was mapped to.
    
    Returns:
        bool: True if the mapping is valid, otherwise False.
    """
    try:
        if not provider_data:
            logger.warning("Validation failed: No provider data available.")
            return False
        
        mismatches = []
        for key in claim_data:
            if claim_data.get(key) != provider_data.get(key):
                mismatches.append(key)
        
        if mismatches:
            logger.warning(f"Validation mismatches found in fields: {', '.join(mismatches)}")
            return False
        
        logger.info("Claim mapping validation passed.")
        return True
    except Exception as e:
        logger.error(f"Error validating mapping: {str(e)}")
        raise
