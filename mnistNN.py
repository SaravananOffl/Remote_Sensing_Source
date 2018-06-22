import mnist
import numpy as np 
train_images = mnist.train_images()
train_labels = mnist.train_labels()
train_images = np.reshape(train_images.flatten(), [47040000,1])
input_nodes = 1
output_nodes = 10 
hidden_layer1_nodes = 1000
hidden_layer2_nodes = 1000
hidden_layer3_nodes = 1000

np.random.seed(1)
w0 =np.rand(input_nodes, hidden_layer1_nodes)
w1 =np.rand(hidden_layer1_nodes, hidden_layer2_nodes)
w2 =np.rand(hidden_layer2_nodes, hidden_layer3_nodes)
w3 =np.rand(hidden_layer3_nodes, output_nodes)

def sigmoid(x, deriv =False):
    if(deriv):
        return x*(1-x)
    
    return 1/(1+np.exp(-x))
#forward

l0 = train_images
l1 = sigmoid(np.dot(lo, w0))
l2 = sigmoid(np.dot(l1, w1))
l3 = sigmoid(np.dot(l2, w2))
l4 = sigmoid(np.dot(l3, w3))
l5 = sigmoi


