import pandas as pd
from dataset import Dataset

import unittest

class YFinDataset(Dataset):
    def __init__(self):
        pass
    
    def __getitem__(self, index):
        pass

    def to_pandas(self):
        pass

    def from_csv(self):
        pass

class TestYFinDataset(unittest.TestCase):
    
    # If not all abstract methods have been implemented, this will fail
    def test_constructor(self):
        _ = YFinDataset()

if __name__ == "__main__":
    unittest.main()
