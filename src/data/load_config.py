import yaml
from pathlib import Path

REQUIRED_SCHEMA = {
    "simulation": ["ticker", "interval", "start_date", "end_date"],
    "portfolio": ["monthly_investment"],
    "strategies": ["user_strategy"],
    "analytics": ["volatility_clustering"]
}

def validate_config(config: dict) -> None:
    """
    Validate the configuration dictionary against the required schema.
    Args:
        config (dict): The configuration dictionary to validate.
    Raises:
        ValueError: If the configuration is missing required sections or keys.
    """
    for section, keys in REQUIRED_SCHEMA.items():
        if section not in config:
            raise ValueError(f"Missing required section '{section}' in configuration.")
        for key in keys:
            if key not in config[section]:
                raise ValueError(f"Missing required key '{key}' in section '{section}' of configuration.")

def load_config(filename: str = "config.yaml") -> dict:
    """
    Load settings from a YAML file located at the project root.
    Args:
        filename (str): The name of the configuration file.
    Returns:
        dict: A dictionary containing the full configuration.
    """
    # __file__ is the path to this script (src/data/load_config.py)
    # .resolve().parent.parent.parent goes up to the project root
    project_root = Path(__file__).resolve().parent.parent.parent
    config_path = project_root / filename

    if not config_path.exists():
        raise FileNotFoundError(f"The configuration file could not be found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
        validate_config(config)
    return config