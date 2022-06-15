from clearml import Task, Dataset
import pandas as pd
import os


for i in range(3):
    dataset = Dataset.create(
        dataset_name=f'Example Dataset #{i}',
        dataset_project='Project Bob'
    )
    df_train = pd.read_csv(
        'https://raw.githubusercontent.com/microsoft/LightGBM/master/examples/regression/regression.train',
        header=None, sep='\t'
    )
    df_test = pd.read_csv(
        'https://raw.githubusercontent.com/microsoft/LightGBM/master/examples/regression/regression.test',
        header=None, sep='\t'
    )
    os.makedirs('/tmp/ditlo', exist_ok=True)
    df_test.to_csv('/tmp/ditlo/test.csv')
    df_train.to_csv('/tmp/ditlo/train.csv')
    dataset.add_files('/tmp/ditlo')
    dataset.finalize(auto_upload=True)
