"""
train.py
--------
Script de TREINAMENTO do reconhecedor facial (Rede 2).

Executa duas fases de Transfer Learning com MobileNetV2:
  Fase 1 — Treina apenas a camada Dense (base congelada).
  Fase 2 — Fine-tuning das últimas 30 camadas da base.

Uso
---
    python train.py --dataset dataset/train
    python train.py --dataset dataset/train --epochs1 15 --epochs2 10 --batch 16
    python train.py --dataset dataset/train --debug

Estrutura do dataset esperada:
    dataset/train/
        pessoa_a/    foto1.jpg  foto2.jpg ...
        pessoa_b/    foto1.jpg  ...
        pessoa_c/    foto1.jpg  ...
    (mínimo recomendado: 30 fotos por pessoa)
"""

import argparse
import json
import logging
import sys
from pathlib import Path

from src import build_model, load_dataset, setup_logging, unfreeze_top_layers

try:
    import tensorflow as tf
    from tensorflow import keras
except ImportError:
    print("ERRO: TensorFlow não instalado. Execute: pip install tensorflow>=2.12")
    sys.exit(1)

MODELS_DIR = Path("models")
OUTPUT_DIR = Path("output")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="train",
        description="Treina o reconhecedor facial com MobileNetV2 (Transfer Learning).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--dataset", "-d",
        type=Path,
        default=Path("dataset/train"),
        help="Pasta raiz do dataset (subpastas = identidades).",
    )
    parser.add_argument(
        "--epochs1",
        type=int, default=20,
        help="Épocas da Fase 1 (base congelada).",
    )
    parser.add_argument(
        "--epochs2",
        type=int, default=10,
        help="Épocas da Fase 2 (fine-tuning).",
    )
    parser.add_argument(
        "--batch", "-b",
        type=int, default=32,
        help="Tamanho do batch.",
    )
    parser.add_argument(
        "--dropout",
        type=float, default=0.4,
        help="Taxa de dropout.",
    )
    parser.add_argument(
        "--val-split",
        type=float, default=0.2,
        help="Fração do dataset para validação.",
    )
    parser.add_argument(
        "--threshold",
        type=float, default=0.60,
        help="Confiança mínima para reconhecer (salva no modelo).",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=MODELS_DIR,
        help="Pasta para salvar o modelo treinado.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Ativa logs DEBUG.",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)

    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(level=log_level, log_file=OUTPUT_DIR / "train.log")
    logger = logging.getLogger(__name__)

    # ── Validações ────────────────────────────────────────────
    if not args.dataset.exists():
        logger.error("Dataset não encontrado: %s", args.dataset)
        logger.error(
            "Crie a pasta e adicione subpastas com fotos de cada pessoa.\n"
            "Exemplo:\n"
            "  dataset/train/\n"
            "      joao/    foto1.jpg  foto2.jpg ...\n"
            "      maria/   foto1.jpg  ..."
        )
        return 1

    subdirs = [d for d in args.dataset.iterdir() if d.is_dir()]
    if len(subdirs) < 2:
        logger.error("O dataset precisa ter pelo menos 2 identidades (subpastas).")
        return 1

    logger.info("━" * 60)
    logger.info("TREINAMENTO DO RECONHECEDOR FACIAL")
    logger.info("━" * 60)
    logger.info("Dataset: %s", args.dataset.resolve())
    logger.info("Identidades encontradas: %d", len(subdirs))
    for d in subdirs:
        imgs = list(d.glob("*.jpg")) + list(d.glob("*.jpeg")) + list(d.glob("*.png"))
        logger.info("  %-20s → %d imagem(ns)", d.name, len(imgs))

    # ── Dataset ───────────────────────────────────────────────
    logger.info("\n[1/4] Carregando dataset...")
    try:
        train_ds, val_ds, class_names = load_dataset(
            args.dataset,
            batch_size=args.batch,
            validation_split=args.val_split,
        )
    except Exception as exc:
        logger.error("Erro ao carregar dataset: %s", exc)
        return 1

    num_classes = len(class_names)
    logger.info("Classes: %s", class_names)

    # ── Modelo ────────────────────────────────────────────────
    logger.info("\n[2/4] Construindo modelo MobileNetV2...")
    model = build_model(num_classes=num_classes, dropout=args.dropout)
    model.summary(print_fn=logger.debug)

    # Callbacks
    args.output.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.output / "face_recognizer.keras"

    callbacks = [
        keras.callbacks.ModelCheckpoint(
            str(checkpoint_path),
            monitor="val_accuracy",
            save_best_only=True,
            verbose=1,
        ),
        keras.callbacks.EarlyStopping(
            monitor="val_accuracy",
            patience=5,
            restore_best_weights=True,
            verbose=1,
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=3,
            verbose=1,
        ),
    ]

    # ── Fase 1 — Base congelada ───────────────────────────────
    logger.info("\n[3/4] FASE 1 — Transfer Learning (base congelada)")
    logger.info("Épocas: %d | Batch: %d", args.epochs1, args.batch)
    logger.info("─" * 40)

    history1 = model.fit(
        train_ds,
        epochs=args.epochs1,
        validation_data=val_ds,
        callbacks=callbacks,
    )

    best_val_acc_1 = max(history1.history["val_accuracy"])
    logger.info("Fase 1 concluída. Melhor val_accuracy: %.4f", best_val_acc_1)

    # ── Fase 2 — Fine-Tuning ─────────────────────────────────
    logger.info("\n[4/4] FASE 2 — Fine-Tuning (descongelando últimas 30 camadas)")
    logger.info("Épocas: %d | LR: 1e-5", args.epochs2)
    logger.info("─" * 40)

    model = unfreeze_top_layers(model, num_layers=30)

    history2 = model.fit(
        train_ds,
        epochs=args.epochs2,
        validation_data=val_ds,
        callbacks=callbacks,
    )

    best_val_acc_2 = max(history2.history["val_accuracy"])
    logger.info("Fase 2 concluída. Melhor val_accuracy: %.4f", best_val_acc_2)

    # ── Salvar artefatos ─────────────────────────────────────
    model.save(str(checkpoint_path))
    logger.info("Modelo salvo em: %s", checkpoint_path.resolve())

    # Salvar nomes das classes
    names_path = args.output / "class_names.json"
    with open(names_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)
    logger.info("Classes salvas em: %s", names_path.resolve())

    # Salvar metadados do treino
    meta = {
        "num_classes": num_classes,
        "class_names": class_names,
        "threshold": args.threshold,
        "img_size": [224, 224],
        "best_val_accuracy_phase1": round(best_val_acc_1, 4),
        "best_val_accuracy_phase2": round(best_val_acc_2, 4),
        "epochs_phase1": args.epochs1,
        "epochs_phase2": args.epochs2,
        "batch_size": args.batch,
        "dropout": args.dropout,
    }
    meta_path = args.output / "training_meta.json"
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    logger.info("\n━" * 60)
    logger.info("✓ TREINAMENTO CONCLUÍDO!")
    logger.info("  Modelo        : %s", checkpoint_path)
    logger.info("  Classes       : %s", names_path)
    logger.info("  Metadados     : %s", meta_path)
    logger.info(
        "  Melhor accuracy: %.2f%% (Fase 1) → %.2f%% (Fase 2)",
        best_val_acc_1 * 100, best_val_acc_2 * 100,
    )
    logger.info("\nPróximo passo:")
    logger.info("  python recognize.py --image assets/foto.jpg")
    logger.info("━" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())