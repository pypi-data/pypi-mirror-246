import numpy as np
from collections import Counter

#euclidian distance
def euclidian_distance(x1, x2):
    return np.sqrt(np.sum((x1-x2)**2))

#Regression
class Regression:
    def __init__(self, learning_rate = 0.0001, iterations = 1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.w = None
        self.b = None
    
    def fit(self, X, y):
        '''takes the training set as parameter and trains the model'''
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0
       
        for _ in range(self.iterations):
            y_predicted = np.dot(X, self.w) + self.b
            dw = (1/n_samples)*np.dot(X.T, (y_predicted - y))
            db = (1/n_samples)*np.sum((y_predicted - y))
            self.w = self.w - self.learning_rate*dw
            self.b = self.b - self.learning_rate*db
    
    def predict(self, X):
       '''takes the argument to predict the results'''
       y_predicted = np.dot(X, self.w) + self.b
       return y_predicted

    def mse(self, y_predicted, y_true):
        '''measures accuracy through mean squared error'''
        return np.mean((y_true - y_predicted)**2)

#Logistic Regression
class LogisticRegression:
    def __init__(self, learning_rate = 0.001, iterations = 1000):
        self.learning_rate = learning_rate
        self.iterations = iterations
        self.w = None
        self.b = None
    
    def fit(self, X, y):
        '''takes the training set as parameter and trains the model'''
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0
        
        for _ in range(self.iterations):
            z = np.dot(X, self.w) + self.b
            y_predicted = 1/(1+np.exp(-z))
            dw = 1/n_samples*np.dot(X.T, (y_predicted - y))
            db = 1/n_samples*np.sum((y_predicted - y))
            self.w = self.w - self.learning_rate*dw
            self.b = self.b - self.learning_rate*db
    
    def predict(self, X):
       '''takes the argument to predict the results'''
       z = np.dot(X, self.w) + self.b
       y_predicted = 1/(1+np.exp(-z))
       y_predicted_class = [1 if i > 0.5 else 0 for i in y_predicted]
       return y_predicted_class
    
    def accuracy(self, y_predicted, y_true):
        return np.sum(y_true == y_predicted)/len(y_true)*100

#K-Nearest-Neighbors
class KNN:
    def __init__(self, k=3):
        self.k = k
    
    def fit(self, X, y):
        '''takes the training set as parameter and trains the model'''
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        '''takes the argument to predict the results'''
        predictions = [self._predict(x) for x in X]
        predictions = np.array(predictions)
        return predictions
    
    def _predict(self, x):
        distances = [euclidian_distance(x, x_train) for x_train in self.X_train]
        min_distances_idx = np.argsort(distances)[:self.k]
        labels = [self.y_train[i] for i in min_distances_idx]
        most_common = Counter(labels).most_common(1)
        return most_common[0][0]

    def accuracy(self, y_predicted, y_true):
        return np.sum(y_true == y_predicted)/len(y_true)*100

#Naive-Bayes
class NaiveBayes:
    
    def fit(self, X, y):
        '''takes the training set as parameter and trains the model'''
        self.X = X
        self.y = y
        n_samples, n_features = X.shape
        self.classes = np.unique(y)
        n_classes = len(self.classes)
        self.mean = np.zeros((n_classes, n_features), dtype=np.float64)
        self.varience = np.zeros((n_classes, n_features), dtype=np.float64)
        self.priors = np.zeros(n_classes, dtype=np.float64)

        for c in self.classes:
            X_c = self.X[c == y]
            self.mean[c, :] = X_c.mean(axis = 0)
            self.varience[c, :] = X_c.var(axis = 0)
            self.priors[c] = X_c.shape[0]/float(n_samples)

    def predict(self, X):
        '''takes the argument to predict the results'''
        prediction = [self._predict(x) for x in X]
        return prediction

    def _predict(self, x):
        posteriors = []

        for idx , c in enumerate(self.classes):
            prior = np.log(self.priors[idx])
            class_conditional = np.sum(np.log(self._pdf(idx, x)))
            posterior = class_conditional + prior
            posteriors.append(posterior)
        
        return self.classes[np.argmax(posteriors)]
    
    def _pdf(self,class_idx, x):

        mean = self.mean[class_idx]
        varience = self.varience[class_idx]
        numerator = np.exp(-(x-mean)**2/(2*varience))
        denominator = np.sqrt(2*np.pi*varience)
        return numerator/denominator
    
    def accuracy(self, y_predicted, y_true):
        return np.sum(y_true == y_predicted)/len(y_true)*100
    
#Support-Vector-Machines
class SVM:
    def __init__(self, learning_rate = 0.001, lambda_param = 0.01, iterations = 1000):
        self.learning_rate = learning_rate
        self.lambda_param = lambda_param
        self.iterations = iterations
        self.w = None
        self.b = None
    
    def fit(self, X, y):
        '''takes the training set as parameter and trains the model'''
        y_ = np.where( y<= 0, -1, 1)
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0

        for i in range(self.iterations):
            for idx, x in enumerate(X):
                if y_[idx]*(np.dot(x, self.w) - self.b) >= 1:
                    self.w -= self.learning_rate*(2*self.lambda_param*self.w)
                else:
                   self.w -= self.learning_rate*(2*self.lambda_param*self.w  - np.dot(y_[idx], x))
                   self.b -= self.learning_rate*y_[idx]
    
    def predict(self, X):
        '''takes the argument to predict the results'''
        linear_model = np.dot(X, self.w) - self.b
        return np.sign(linear_model)

    def accuracy(self, y_predicted, y_true):
        return np.sum(y_true == y_predicted)/len(y_true)*100
