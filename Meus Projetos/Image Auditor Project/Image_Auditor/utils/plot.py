import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

def plot_before_after(original: Image.Image, processed: Image.Image, title_after: str = "Processada"):
    """Exibe o comparativo Lado a Lado do processamento."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    
    axes[0].imshow(original)
    axes[0].set_title("Original")
    axes[0].axis('off')
    
    axes[1].imshow(processed)
    axes[1].set_title(title_after)
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()