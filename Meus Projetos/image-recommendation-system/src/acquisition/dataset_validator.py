from src.acquisition.paths import IMAGE_DIR
from src.acquisition.config import DatasetConfig

def get_all_images():

    images = []

    for extension in DatasetConfig.allowed_extensions:

        images.extend(
            IMAGE_DIR.glob(f"*{extension}")
        )

    return sorted(images)