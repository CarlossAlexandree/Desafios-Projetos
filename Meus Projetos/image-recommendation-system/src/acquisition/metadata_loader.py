import pandas as pd

from src.acquisition.paths import METADATA_FILE

def load_metadata():

    if not METADATA_FILE.exists():

        return None

    return pd.read_csv(METADATA_FILE)