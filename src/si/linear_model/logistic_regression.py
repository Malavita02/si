import numpy as np
from src.si.data.dataset import Dataset
from src.si.statistics.sigmoid_function import sigmoid_function
from src.si.metrics.accuracy import accuracy

class LogisticRegression:
    """
    The LogisticRegression is a logistic model using the L2 regularization.
    This model solves the logistic regression problem using an adapted Gradient Descent technique
    Parameters
    ----------
    l2_penalty: float
        The L2 regularization parameter
    alpha: float
        The learning rate
    max_iter: int
        The maximum number of iterations
    Attributes
    ----------
    theta: np.array
        The model parameters, namely the coefficients of the logistic model.
        For example, sigmoid(x0 * theta[0] + x1 * theta[1] + ...)
    theta_zero: float
        The intercept of the logistic model
    cost_history: dict
        Stores the output of the cost function
    """
    def __init__(self, l2_penalty: float = 1, alpha: float = 0.001, max_iter: int = 1000) -> None:
        """

        Parameters
        ----------
        l2_penalty: float
            The L2 regularization parameter
        alpha: float
            The learning rate
        max_iter: int
            The maximum number of iterations
        """
        # parameters
        self.l2_penalty = l2_penalty
        self.alpha = alpha
        self.max_iter = max_iter

        # attributes
        self.theta = None
        self.theta_zero = None
        self.cost_history = {}
    
    def fit(self, dataset: Dataset) -> 'LogisticRegression':
        """
        Fit the model to the dataset
        Parameters
        ----------
        dataset: Dataset
            The dataset to fit the model to
        Returns
        -------
        self: LogisticRegression
            The fitted model
        """
        m, n = dataset.get_shape()
        # initialize the model parameters
        self.theta = np.zeros(n)
        self.theta_zero = 0

        # gradient descent
        for i in range(self.max_iter):
            # predicted y
            y_pred = np.dot(dataset.X, self.theta) + self.theta_zero

            # computing and updating the gradient with the learning rate
            gradient = (self.alpha * (1 / m)) * np.dot(y_pred - dataset.y, dataset.X)

            # computing the penalty
            penalization_term = self.alpha * (self.l2_penalty / m) * self.theta

            # updating the model parameters
            self.theta = self.theta - gradient - penalization_term
            self.theta_zero = self.theta_zero - (self.alpha * (1 / m)) * np.sum(y_pred - dataset.y)
            self.cost_history[i] = self.cost(dataset)
            # exercicio 6.3)
            if i > 0:
                if (self.cost_history[i-1] - self.cost_history[i]) < 0.0001:
                    return self
        return self
    
    def predict(self, dataset: Dataset) -> np.array:
        """
        Predict the output of the dataset
        Parameters
        ----------
        dataset: Dataset
            The dataset to predict the output of
        Returns
        -------
        predictions: np.array
            The predictions of the dataset
        """
        predictions = sigmoid_function(np.dot(dataset.X, self.theta) + self.theta_zero)

        # convert the predictions to 0 or 1 (binarization)
        mask = predictions >= 0.5
        predictions[mask] = 1
        predictions[~mask] = 0
        return predictions
    
    def score(self, dataset: Dataset) -> float:
        """
        Compute the Mean Square Error of the model on the dataset
        Parameters
        ----------
        dataset: Dataset
            The dataset to compute the MSE on
        Returns
        -------
        mse: float
            The Mean Square Error of the model
        """
        y_pred = self.predict(dataset)
        return accuracy(dataset.y, y_pred)
    
    def cost(self, dataset: Dataset) -> float:
        """
        Compute the cost function (J function) of the model on the dataset using L2 regularization
        Parameters
        ----------
        dataset: Dataset
            The dataset to compute the cost function on
        Returns
        -------
        cost: float
            The cost function of the model
        """
        predictions = sigmoid_function(np.dot(dataset.X, self.theta) + self.theta_zero)
        cost = (-dataset.y * np.log(predictions)) - ((1 - dataset.y) * np.log(1 - predictions))
        cost = np.sum(cost) / dataset.get_shape()[0]
        cost = cost + (self.l2_penalty * np.sum(self.theta ** 2) / (2 * dataset.get_shape()[0]))
        return cost

if __name__ == '__main__':

    from src.si.model_selection.split import train_test_split
    # Exercicio 6.1)
    # load and split the dataset
    #dataset_ = Dataset.from_random(600, 100, 2)
    from src.si.io.csv import read_csv
    dataset_ = read_csv(r"C:\Users\Tiago\GitHub\Repositorio de Sistemas\Repositorio-Sistemas\datasets\breast-bin.csv", features=True, label= True)
    dataset_train, dataset_test = train_test_split(dataset_, test_size=0.2)


    # fit the model
    model = LogisticRegression(l2_penalty=1, alpha=0.001, max_iter=2000)
    model.fit(dataset_train)

    # compute the score
    score = model.score(dataset_test)
    print(f"Score: {score}")

    # cost history
    print(model.cost_history)

    # Exercicio 6.2)
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-whitegrid')
    fig = plt.figure()
    ax = plt.axes()
    y = model.cost_history.values()
    x = range(len(model.cost_history))
    ax.plot(x,y)
    plt.show()


