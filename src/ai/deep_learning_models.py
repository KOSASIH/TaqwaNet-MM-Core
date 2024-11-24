# src/ai/deep_learning_models.py

import tensorflow as tf
from tensorflow.keras import layers, models

class FeedforwardNN:
    def __init__(self, input_shape, num_classes):
        self.model = self.build_model(input_shape, num_classes)

    def build_model(self, input_shape, num_classes):
        model = models.Sequential()
        model.add(layers.Input(shape=input_shape))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(num_classes, activation='softmax'))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self, x_train, y_train, epochs=10, batch_size=32, validation_data=None):
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=validation_data)

    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test)

    def predict(self, x):
        return self.model.predict(x)

class ConvolutionalNN:
    def __init__(self, input_shape, num_classes):
        self.model = self.build_model(input_shape, num_classes)

    def build_model(self, input_shape, num_classes):
        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.Flatten())
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(num_classes, activation='softmax'))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def train(self, x_train, y_train, epochs=10, batch_size=32, validation_data=None):
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=validation_data)

    def evaluate(self, x_test, y_test):
        return self.model.evaluate(x_test, y_test)

    def predict(self, x):
        return self.model.predict(x)

if __name__ == "__main__":
    # Example usage
    import numpy as np

    # Generate dummy data
    x_train = np.random.rand(1000, 28, 28, 1)  # 1000 samples of 28x28 grayscale images
    y_train = np.random.randint(0, 10, 1000)   # 1000 labels for 10 classes
    x_test = np.random.rand(200, 28, 28, 1)     # 200 test samples
    y_test = np.random.randint(0, 10, 200)      # 200 test labels

    # Create and train a Feedforward Neural Network
    ff_nn = FeedforwardNN(input_shape=(784,), num_classes=10)
    ff_nn.train(x_train.reshape(1000, -1), y_train, epochs=5)

    # Evaluate the Feedforward Neural Network
    ff_nn.evaluate(x_test.reshape(200, -1), y_test)

    # Create and train a Convolutional Neural Network
    cnn = ConvolutionalNN(input_shape=(28, 28, 1), num_classes=10)
    cnn.train(x_train, y_train, epochs=5)

    # Evaluate the Convolutional Neural Network
    cnn.evaluate(x_test, y_test)
