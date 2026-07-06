from src.acquisition.dataset_validator import get_all_images
from src.acquisition.metadata_loader import load_metadata
from src.acquisition.config import DatasetConfig

def load_dataset():

    images = get_all_images()

    metadata = load_metadata()

    if DatasetConfig.max_images:

        images = images[:DatasetConfig.max_images]

    print("=" * 50)

    print(f"Imagens : {len(images)}")

    if metadata is not None:

        print(f"Metadata : {len(metadata)}")

    else:

        print("Metadata : Não encontrado")

    print("=" * 50)

    return images, metadata

if __name__ == "__main__":

    load_dataset()