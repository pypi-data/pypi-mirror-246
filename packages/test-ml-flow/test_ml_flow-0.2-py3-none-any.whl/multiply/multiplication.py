import mlflow
from sklearn import datasets
from  sklearn.model_selection import  train_test_split
class Multiplication:
    """
    Instantiate a multiplication operation.
    Numbers will be multiplied by the given multiplier.

    :param multiplier: The multiplier.
    :type multiplier: int
    """

    def __init__(self, multiplier):
        self.multiplier = multiplier

    def multiply(self, number):
        """
        Multiply a given number by the multiplier.

        :param number: The number to multiply.
        :type number: int

        :return: The result of the multiplication.
        :rtype: int
        """

        mlflow.start_run()
        mlflow.log_param("my", "param")
        mlflow.log_metric("score", 100)
        dataset = datasets.load_iris()
        print(dataset)
        mlflow.end_run()

        return number * self.multiplier


# Instantiate a Multiplication object
multiplication = Multiplication(2)

# Call the multiply method
print(multiplication.multiply(5))