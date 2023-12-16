# K-Inertia (Kavish Inertia)
![k-inertia logo](https://github.com/KavishTomar4/K-Learn/assets/32963200/58e100a0-dc80-4a31-b169-686f60e3093a)

**K-Inertia: A User-Friendly Machine Learning Library**
K-Inertia or ***Kavish Inertia*** is a Python machine learning library designed for simplicity and ease of use. With a focus on user-friendly interfaces, K-Inertia provides implementations of various machine learning algorithms, including regression, logistic regression, k-nearest neighbors, naive Bayes, support vector machines, and k-means clustering.

**Key Features:**

+ **Diverse Algorithms:**
K-Inertia offers a range of algorithms, covering both supervised and unsupervised learning tasks. Users can seamlessly implement regression, classification (logistic regression, k-nearest neighbors, naive Bayes, support vector machines), and clustering (k-means) with minimal effort.

+ **User-Friendly Interface:**
K-Inertia is designed to be user-friendly, making it accessible for both beginners and experienced users. The library provides clear and intuitive APIs for easy integration into machine learning workflows.

+ **Simplified Usage:**
Users can leverage the library's simplified syntax to perform complex machine learning tasks without extensive coding. K-Inertia aims to streamline the implementation process, reducing the learning curve for users new to machine learning.

+ **Flexibility:**
K-Inertia allows users to experiment with different algorithms and easily switch between them based on their specific needs. The library's flexibility encourages exploration and experimentation with various machine learning techniques.

K-Inertia strives to empower users with a straightforward and accessible machine learning experience. Whether you are building predictive models, classifying data, or clustering patterns, K-Inertia is designed to be a reliable companion for your machine learning endeavors.

***

# Documentation

## Regression
```
class kinertia.supervised.Regression(learning_rate=0.0001, iterations=1000)
```
Ordinary least squares Linear Regression.

LinearRegression fits a linear model with coefficients w = (w1, …, wp) to minimize the residual sum of squares between the observed targets in the dataset, and the targets predicted by the linear approximation.

#### Parameters:
`learning_rate` : This parameter is a hyper-parameter used to govern the pace at which an algorithm updates or learns the values of a parameter estimate.

`iterations` : This parameter, defines the number of times the iterations takes place to train this model.

#### Methods:
`fit(X,y)` : This method takes the training set of data as parameter and trains the model

`predict(X)` : Takes the independent features of data as parameter and predicts the result

`mse(y_predicted, y_true)` : Takes the predicted and actual value of outcomes as parameter and gives the mean squared error for accuracy of Regression. The less the value of mse, the more accurate model is.

``` py
#Reading the data through csv
import pandas as pd
data = pd.read_csv("example.csv")
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

#Splitting the data for training and testing samples 
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

#Applying regression
from kinertia.supervised import Regression
regresion  = Regression(learning_rate=0.005)
regresion.fit(x_train, y_train)
predict = regresion.predict(x_test)
```
***
## Logistic Regression
```
class kinertia.supervised.LogisticRegression(learning_rate=0.0001, iterations=1000)
```
For binary logistic regression, the logistic function (also called the sigmoid function) is employed to map the output of a linear combination of features into a range between 0 and 1.

#### Parameters:
`learning_rate` : This parameter is a hyper-parameter used to govern the pace at which an algorithm updates or learns the values of a parameter estimate.

`iterations` : This parameter, defines the number of times the iterations takes place to train this model.

#### Methods:
`fit(X,y)` : This method takes the training set of data as parameter and trains the model.

`predict(X)` : Takes the independent features of data as parameter and predicts the result.

`accuracy(y_predicted, y_true)` : Takes the predicted and actual value of outcomes as parameter and gives the accuracy percentage.

``` py
#Reading the data through csv
import pandas as pd
data = pd.read_csv("example.csv")
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

#Splitting the data for training and testing samples 
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

#Applying Logistic regression
from kinertia.supervised import LogisticRegression
lr  = LogisitcRegression(learning_rate=0.005)
lr.fit(x_train, y_train)
predict = lr.predict(x_test)
```
***
## K-Nearest Neighbors
```
class kinertia.supervised.KNN(k=3)
```
K-Nearest Neighbors (KNN) is a supervised machine learning algorithm used for both classification and regression tasks. It's a simple and intuitive algorithm that makes predictions based on the majority class (for classification) or the average (for regression) of the k-nearest data points in the feature space. The key idea behind KNN is that instances with similar feature values are likely to belong to the same class or have similar target values.

#### Parameters:
`k` : This parameter defines how many neighbors will be checked to determine the classification of a specific query point.

#### Methods:
`fit(X,y)` : This method takes the training set of data as parameter and trains the model.

`predict(X)` : Takes the independent features of data as parameter and predicts the result.

`accuracy(y_predicted, y_true)` : Takes the predicted and actual value of outcomes as parameter and gives the accuracy percentage.

``` py
#Reading the data through csv
import pandas as pd
data = pd.read_csv("example.csv")
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

#Splitting the data for training and testing samples 
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

#Applying KNN
from kinertia.supervised import KNN
knn  = KNN(k=3)
knn.fit(x_train, y_train)
predict = knn.predict(x_test)
```
***
## Naive Bayes
```
class kinertia.supervised.NaiveBayes()
```
The "naive" part of Naive Bayes comes from the assumption of independence among features, given the class label. This means that the presence or absence of a particular feature is assumed to be unrelated to the presence or absence of any other feature. While this assumption is often not strictly true in real-world data, it simplifies the calculation and makes the algorithm computationally efficient.

#### Methods:
`fit(X,y)` : This method takes the training set of data as parameter and trains the model.

`predict(X)` : Takes the independent features of data as parameter and predicts the result.

`accuracy(y_predicted, y_true)` : Takes the predicted and actual value of outcomes as parameter and gives the accuracy percentage.

``` py
#Reading the data through csv
import pandas as pd
data = pd.read_csv("example.csv")
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

#Splitting the data for training and testing samples 
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

#Applying Naive Bayes
from kinertia.supervised import NaiveBayes
bayes  = NaiveBayes()
bayes.fit(x_train, y_train)
predict = bayes.predict(x_test)
```
***
## Support Vector Machine
```
class kinertia.supervised.SVM(learning_rate = 0.001, lambda_param = 0.01, iterations = 1000)
```
Support Vector Machines (SVMs) are supervised machine learning models used for both classification and regression tasks. SVMs are particularly effective in high-dimensional spaces and are widely used in various applications, including image classification, text categorization, and bioinformatics. The primary objective of SVM is to find a hyperplane that best separates the data into different classes while maximizing the margin between the classes.

#### Parameters:
`learning_rate` : This parameter is a hyper-parameter used to govern the pace at which an algorithm updates or learns the values of a parameter estimate.

`lambda_param` : Thid parameter serves as a degree of importance that is given to miss-classifications.

`iterations` : This parameter, defines the number of times the iterations takes place to train this model.

#### Methods:
`fit(X,y)` : This method takes the training set of data as parameter and trains the model.

`predict(X)` : Takes the independent features of data as parameter and predicts the result.

`accuracy(y_predicted, y_true)` : Takes the predicted and actual value of outcomes as parameter and gives the accuracy percentage.

``` py
#Reading the data through csv
import pandas as pd
data = pd.read_csv("example.csv")
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

#Splitting the data for training and testing samples 
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

#Applying Support Vector Machine
from kinertia.supervised import SVM
svm = SVM(learning_rate = 0.0001, lambda_param = 0.01)
svm.fit(x_train, y_train)
predict = svm.predict(x_test)
```
***
## K-Means Clustering
```
class kinertia.unsupervised.KMeans(k=5, max_iters=100)
```
K-Means Clustering is an unsupervised machine learning algorithm used for partitioning a dataset into K distinct, non-overlapping subsets (clusters). Each data point belongs to the cluster with the nearest mean, and the mean of each cluster serves as a representative or centroid of that cluster. K-Means is commonly used for grouping data points based on similarity and is widely applied in various fields, including image segmentation, customer segmentation, and anomaly detection.

#### Parameters:
'k' : Number of clusters

'max_iters' : This parameter, defines the number of times the iterations takes place to train this model.

#### Methods:
`predict(X)` : Takes the independent features of data as parameter and predicts the result.

``` py
#Reading the data through csv
import pandas as pd
data = pd.read_csv("example.csv")
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

#Applying K-Means Clustering
from kinertia.unsupervised import KMeans
means = KMeans(k = 3)
predict = svm.predict(x)
```
***






