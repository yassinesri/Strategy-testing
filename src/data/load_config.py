import yaml
from pathlib import Path

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
        
    return config