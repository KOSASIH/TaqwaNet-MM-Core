import unittest
from src.ai import AIComponent  # Adjust the import based on your project structure

class TestAIComponent(unittest.TestCase):
    def setUp(self):
        self.ai = AIComponent()

    def test_prediction(self):
        result = self.ai.predict(input_data=[1, 2, 3])
        self.assertIsNotNone(result)

    def test_training(self):
        training_data = [[1, 2], [2, 3]]
        self.ai.train(training_data)
        self.assertTrue(self.ai.is_trained)

if __name__ == '__main__':
    unittest.main()
