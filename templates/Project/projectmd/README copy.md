

<body>
    <h1>Neural Network Implementation Documentation</h1>

    <h2>Overview</h2>
    <p>This document describes a simple two-layer neural network (NN) implemented in Python. The network consists of:</p>
    <ul>
        <li>Input Layer: 784 units (for 28x28 images).</li>
        <li>Hidden Layer: 10 units with ReLU activation.</li>
        <li>Output Layer: 10 units with softmax activation.</li>
    </ul>
    <p>The neural network is trained using gradient descent.</p>
    <p>Below is a visual representation of the network architecture:</p>
    <img src="network_architecture.png" alt="Neural Network Architecture" width="500"/>

    <h2>1. Data Preparation</h2>
    <h3>Loading and Preprocessing Data</h3>
    <div class="code-block">
        <pre><code>
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv('train.csv')
data = np.array(data)
m, n = data.shape

# Shuffle before splitting into dev and training sets
data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n]
X_dev = X_dev / 255.  # Normalize pixel values

data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n]
X_train = X_train / 255.  # Normalize pixel values
_, m_train = X_train.shape
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li><strong>Data Loading:</strong> Reads the dataset from a CSV file.</li>
            <li><strong>Data Splitting:</strong> Splits the data into development (dev) and training sets.</li>
            <li><strong>Normalization:</strong> Scales pixel values to the range [0, 1] by dividing by 255.</li>
        </ul>
    </div>

    <h2>2. Network Architecture</h2>
    <h3>Initialization of Parameters</h3>
    <div class="code-block">
        <pre><code>
def init_params():
    W1 = np.random.rand(10, 784) - 0.5  # Weight matrix for layer 1
    b1 = np.random.rand(10, 1) - 0.5   # Bias vector for layer 1
    W2 = np.random.rand(10, 10) - 0.5   # Weight matrix for layer 2
    b2 = np.random.rand(10, 1) - 0.5   # Bias vector for layer 2
    return W1, b1, W2, b2
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li><strong>Weights and Biases Initialization:</strong> Randomly initializes weights and biases with values in the range [-0.5, 0.5].</li>
        </ul>
    </div>

    <h3>Activation Functions</h3>
    <h4>ReLU Activation Function</h4>
    <div class="code-block">
        <pre><code>
def ReLU(Z):
    return np.maximum(Z, 0)  # Element-wise ReLU activation
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li>Applies the ReLU activation function element-wise. ReLU is defined as ReLU(Z)=max⁡(Z,0).</li>
        </ul>
    </div>
    <p>The ReLU activation function can be visualized as:</p>
    <img src="relu_activation.png" alt="ReLU Activation Function" width="300"/>

    <h4>Softmax Activation Function</h4>
    <div class="code-block">
        <pre><code>
def softmax(Z):
    e_Z = np.exp(Z - np.max(Z, axis=0, keepdims=True))  # Improve numerical stability
    return e_Z / np.sum(e_Z, axis=0, keepdims=True)  # Normalize
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li>Applies the softmax activation function, which normalizes the output to a probability distribution.</li>
        </ul>
    </div>
     <p>The Softmax function transforms outputs into a probability distribution.</p>
    <img src="softmax_activation.png" alt="Softmax Activation Function" width="300"/>

    <h3>Forward Propagation</h3>
    <div class="code-block">
        <pre><code>
def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1  # Linear transformation for layer 1
    A1 = ReLU(Z1)        # ReLU activation for layer 1
    Z2 = W2.dot(A1) + b2  # Linear transformation for layer 2
    A2 = softmax(Z2)     # Softmax activation for layer 2 (output layer)
    return Z1, A1, Z2, A2
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li><strong>Linear Transformations:</strong> Computes ZZ values for each layer using matrix multiplication and addition.</li>
            <li><strong>Activations:</strong> Applies ReLU and softmax activation functions.</li>
        </ul>
    </div>

    <h3>Backward Propagation</h3>
    <div class="code-block">
        <pre><code>
def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
    one_hot_Y = one_hot(Y)  # Convert labels to one-hot encoding
    dZ2 = A2 - one_hot_Y  # Gradient of the loss with respect to Z2
    dW2 = 1 / m * dZ2.dot(A1.T)  # Gradient of the loss with respect to W2
    db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)  # Gradient of the loss with respect to b2
    dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)  # Gradient of the loss with respect to Z1
    dW1 = 1 / m * dZ1.dot(X.T)  # Gradient of the loss with respect to W1
    db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)  # Gradient of the loss with respect to b1
    return dW1, db1, dW2, db2
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li><strong>Gradients Calculation:</strong> Computes gradients for weights and biases for both layers using the chain rule.</li>
            <li><strong>One-Hot Encoding:</strong> Converts class labels into one-hot vectors.</li>
            <li><strong>Gradient Averaging:</strong> Divides by the number of examples (mm) to get average gradients.</li>
        </ul>
    </div>

    <h3>Parameter Updates</h3>
    <div class="code-block">
        <pre><code>
def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 -= alpha * dW1  # Update W1
    b1 -= alpha * db1  # Update b1
    W2 -= alpha * dW2  # Update W2
    b2 -= alpha * db2  # Update b2
    return W1, b1, W2, b2
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li><strong>Gradient Descent:</strong> Updates parameters by subtracting the learning rate (α) times the gradient.</li>
        </ul>
    </div>

    <h2>3. Training the Neural Network</h2>
    <div class="code-block">
        <pre><code>
def gradient_descent(X, Y, alpha, iterations):
    W1, b1, W2, b2 = init_params()  # Initialize parameters
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)  # Forward propagation
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y)  # Backward propagation
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)  # Update parameters
        if i % 10 == 0:
            print("Iteration: ", i)
            predictions = get_predictions(A2)  # Get predictions
            print(get_accuracy(predictions, Y))  # Print accuracy
    return W1, b1, W2, b2
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li><strong>Training Loop:</strong> Iterates through the specified number of iterations, performing forward propagation, backward propagation, and updating parameters.</li>
            <li><strong>Accuracy Check:</strong> Prints accuracy every 10 iterations to monitor training progress.</li>
        </ul>
    </div>

    <h2>4. Prediction and Accuracy</h2>
    <div class="code-block">
        <pre><code>
def get_predictions(A2):
    return np.argmax(A2, 0)  # Get the index of the max value in each column (predicted class)

def get_accuracy(predictions, Y):
    return np.sum(predictions == Y) / Y.size  # Calculate accuracy as the ratio of correct predictions
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li><strong>Predictions:</strong> Determines the class with the highest probability for each example.</li>
            <li><strong>Accuracy:</strong> Measures the proportion of correct predictions.</li>
        </ul>
    </div>

    <h2>5. Testing Predictions</h2>
    <div class="code-block">
        <pre><code>
def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)  # Forward propagation
    return get_predictions(A2)  # Get predictions

def test_prediction(index, W1, b1, W2, b2):
    current_image = X_train[:, index, None]  # Select image to test
    prediction = make_predictions(X_train[:, index, None], W1, b1, W2, b2)  # Make prediction
    label = Y_train[index]  # True label
    print("Prediction: ", prediction)
    print("Label: ", label)

    current_image = current_image.reshape((28, 28)) * 255  # Reshape and scale image for display
    plt.gray()
    plt.imshow(current_image, interpolation='nearest')  # Show image
    plt.show()
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li><strong>Make Predictions:</strong> Uses the trained model to predict classes for input data.</li>
            <li><strong>Test Prediction:</strong> Displays a specific image, its prediction, and true label for visual verification.</li>
        </ul>
    </div>

    <h2>Example Predictions</h2>
    <p>Here are a few examples of the model's predictions on training images:</p>

    <div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
        <div>
            <img src="prediction_0.png" alt="Prediction Example 1" width="100"/>
            <p style="text-align: center;">Prediction: [Prediction Label 0], Label: [True Label 0]</p>
        </div>
        <div>
            <img src="prediction_1.png" alt="Prediction Example 2" width="100"/>
            <p style="text-align: center;">Prediction: [Prediction Label 1], Label: [True Label 1]</p>
        </div>
        <div>
            <img src="prediction_2.png" alt="Prediction Example 3" width="100"/>
            <p style="text-align: center;">Prediction: [Prediction Label 2], Label: [True Label 2]</p>
        </div>
        <div>
            <img src="prediction_3.png" alt="Prediction Example 4" width="100"/>
            <p style="text-align: center;">Prediction: [Prediction Label 3], Label: [True Label 3]</p>
        </div>
    </div>

    <h2>6. Evaluation</h2>
    <div class="code-block">
        <pre><code>
dev_predictions = make_predictions(X_dev, W1, b1, W2, b2)
print("Dev set accuracy: ", get_accuracy(dev_predictions, Y_dev))
        </code></pre>
    </div>
    <div class="explanation">
        <p><strong>Explanation:</strong></p>
        <ul>
            <li><strong>Development Set Accuracy:</strong> Evaluates the model's performance on the dev set.</li>
        </ul>
    </div>
    <p>The accuracy on the development set gives an estimate of the model's generalization performance.</p>


    <h2>Mathematical Overview</h2>
    <h3>Forward Propagation:</h3>
    <p><strong>Layer 1 (Hidden Layer):</strong></p>
    <pre><code>
Z1 = W1.dot(X) + b1
A1 = ReLU(Z1)
    </code></pre>
    <p><strong>Layer 2 (Output Layer):</strong></p>
    <pre><code>
Z2 = W2.dot(A1) + b2
A2 = Softmax(Z2)
    </code></pre>

    <h3>Backward Propagation:</h3>
    <p><strong>Output Layer Gradients:</strong></p>
    <pre><code>
dZ2 = A2 - one_hot(Y)
dW2 = 1 / m * dZ2.dot(A1.T)
db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)
    </code></pre>
    <p><strong>Hidden Layer Gradients:</strong></p>
    <pre><code>
dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)
dW1 = 1 / m * dZ1.dot(X.T)
db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)
    </code></pre>

    <h3>Parameter Updates:</h3>
    <pre><code>
W1 -= alpha * dW1
b1 -= alpha * db1
W2 -= alpha * dW2
b2 -= alpha * db2
    </code></pre>
</body>