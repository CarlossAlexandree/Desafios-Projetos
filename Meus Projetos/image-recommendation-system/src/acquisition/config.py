from dataclasses import dataclass

@dataclass
class DatasetConfig:

    image_size = 224

    batch_size = 32

    max_images = None

    allowed_extensions = (
        ".jpg",
        ".jpeg",
        ".png"
    )