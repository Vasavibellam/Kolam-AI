import tensorflow as tf
from tensorflow.keras import layers, models

IMG_SIZE = (128, 128)
BATCH_SIZE = 32
NUM_CLASSES = 4

def build_kolam_cnn():
    model = models.Sequential([
        layers.Input(shape=(128, 128, 3)),

        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),

        layers.Conv2D(128, 3, activation='relu'),
        layers.MaxPooling2D(),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.4),

        layers.Dense(NUM_CLASSES, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model
