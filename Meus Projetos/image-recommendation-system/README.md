# 🖼️ Image Recommendation System

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![OpenCLIP](https://img.shields.io/badge/OpenCLIP-Multimodal-blue?style=for-the-badge)
![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-green?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-Interface-FF4B4B?style=for-the-badge&logo=streamlit)

</p>

---

# 📖 Overview

Image Recommendation System is an end-to-end **Computer Vision** project capable of recommending visually similar products using **Multimodal Embeddings**, **Vector Search**, and **Approximate Nearest Neighbor (ANN)** techniques.

The system extracts semantic representations from images using **OpenCLIP**, indexes them with **FAISS**, and performs high-speed similarity searches.

Designed for:

- 🎓 Academic Research
- 💼 Professional Portfolio
- 🚀 Production Deployment

---

# 🎯 Main Features

✅ Image Similarity Search

✅ OpenCLIP Embeddings

✅ FAISS Vector Index

✅ k-Nearest Neighbors (kNN)

✅ FastAPI REST API

✅ Streamlit Web Interface

✅ Modular Architecture

✅ Production Ready

---

# 🏗️ Architecture

```text
                Images
                   │
                   ▼
          Preprocessing Pipeline
                   │
                   ▼
           OpenCLIP Encoder
                   │
                   ▼
           Image Embeddings
                   │
                   ▼
               FAISS Index
                   │
                   ▼
          Similarity Search
                   │
                   ▼
      FastAPI + Streamlit UI
```

---

# 📂 Project Structure

```text
image-recommendation-system/

│

├── configs/

├── data/
│   ├── raw/
│   ├── processed/
│   ├── embeddings/
│   ├── indexes/
│   └── cache/

├── src/
│   ├── acquisition/
│   ├── preprocessing/
│   ├── embedding/
│   ├── indexing/
│   ├── recommendation/
│   ├── api/
│   └── ui/

├── tests/

├── notebooks/

├── requirements.txt

├── README.md

└── LICENSE
```

---

# ⚙️ Tech Stack

| Category | Technologies |
|------------|----------------|
| Language | Python |
| Deep Learning | PyTorch |
| Vision | OpenCLIP |
| Image Processing | Pillow, OpenCV |
| Vector Database | FAISS |
| API | FastAPI |
| Interface | Streamlit |
| Data | Pandas, NumPy |
| Testing | PyTest |

---

# 🚀 Installation

Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/image-recommendation-system.git
```

Enter the project

```bash
cd image-recommendation-system
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
source .venv/Scripts/activate
```

Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Dataset

The project is dataset-agnostic.

Expected structure:

```text
data/

raw/

images/

image001.jpg

image002.jpg

image003.jpg

metadata.csv (optional)
```

---

# ▶️ Running

Dataset Loader

```bash
python -m src.acquisition.dataset_loader
```

Future modules

```bash
python -m src.preprocessing

python -m src.embedding

python -m src.indexing

python -m src.api

streamlit run src/ui/app.py
```

---

# 🔍 Recommendation Pipeline

```text
Load Images

↓

Preprocessing

↓

OpenCLIP Embeddings

↓

FAISS Index

↓

Similarity Search

↓

REST API

↓

Web Interface
```

---

# 📈 Roadmap

- [x] Project Structure
- [x] Dataset Loader
- [ ] Image Preprocessing
- [ ] OpenCLIP Encoder
- [ ] Embedding Generation
- [ ] FAISS Index
- [ ] Similarity Search
- [ ] Re-ranking
- [ ] FastAPI
- [ ] Streamlit
- [ ] Docker
- [ ] AWS Deployment
- [ ] CI/CD

---

# 📊 Performance Goals

- Search time < 100 ms

- Modular architecture

- CPU compatible

- GPU acceleration (optional)

- Low memory consumption

- Scalable for production

---

# 🧠 Future Improvements

- Fine-Tuning OpenCLIP

- DINOv2 Integration

- Milvus Support

- Elasticsearch

- Hybrid Search

- Text-to-Image Search

- Image-to-Text Search

- Batch Processing

---

# 🤝 Contributing

Contributions are welcome.

Feel free to:

- Fork the project

- Open Issues

- Submit Pull Requests

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

## **_Carlos Alexandre_**

Artificial Intelligence Master's Student

Data Science • Computer Vision • Machine Learning • Deep Learning


---

⭐ If you found this project useful, consider giving it a Star.