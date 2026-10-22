import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

ROOT = r"C:\agri-sense-x"
DATA_DIR = os.path.join(ROOT, "data", "kaggle", "pest", "images")
MODEL_DIR = os.path.join(ROOT, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE = (224, 224)
BATCH = 16
EPOCHS = 20
SEED = 42

classes = sorted([d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))])
if not classes:
    raise SystemExit(f"No class folders found in {DATA_DIR} — check path.")

print("Found classes:", classes)

train_aug = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.20,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    vertical_flip=False,
    zoom_range=0.15,
    shear_range=0.1,
    fill_mode="reflect"
)

train_gen = train_aug.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH,
    class_mode="categorical",
    subset="training",
    shuffle=True,
    seed=SEED
)

val_gen = train_aug.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH,
    class_mode="categorical",
    subset="validation",
    shuffle=False,
    seed=SEED
)

num_classes = train_gen.num_classes
print("Num classes:", num_classes)
print("Train steps:", train_gen.samples, "Val steps:", val_gen.samples)

backbone = EfficientNetB0(weights="imagenet", include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
backbone.trainable = False

model = models.Sequential([
    backbone,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.3),
    layers.Dense(256, activation="relu"),
    layers.Dropout(0.2),
    layers.Dense(num_classes, activation="softmax")
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
              loss="categorical_crossentropy",
              metrics=["accuracy"])

model.summary()

ckpt = ModelCheckpoint(os.path.join(MODEL_DIR, "pest_model_best.h5"), save_best_only=True, monitor="val_accuracy", verbose=1)
rlr = ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, verbose=1)
es = EarlyStopping(monitor="val_loss", patience=7, restore_best_weights=True, verbose=1)

history = model.fit(
    train_gen,
    epochs=EPOCHS,
    validation_data=val_gen,
    callbacks=[ckpt, rlr, es],
    verbose=1
)

backbone.trainable = True
for layer in backbone.layers[:-20]:
    layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
              loss="categorical_crossentropy",
              metrics=["accuracy"])

model.fit(
    train_gen,
    epochs=8,
    validation_data=val_gen,
    callbacks=[ckpt, rlr, es],
    verbose=1
)

model.save(os.path.join(MODEL_DIR, "pest_model_final.h5"))
print("Saved model to", os.path.join(MODEL_DIR, "pest_model_final.h5"))

label_map = {v: k for k, v in train_gen.class_indices.items()}
with open(os.path.join(MODEL_DIR, "pest_label_map.json"), "w") as f:
    json.dump(label_map, f, indent=2)
print("Saved label map to", os.path.join(MODEL_DIR, "pest_label_map.json"))
