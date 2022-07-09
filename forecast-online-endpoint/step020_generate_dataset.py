import pandas as pd
import numpy as np

data_length = 36
TIME_COLUMN_NAME = "DateCreated"
TARGET_COLUMN_NAME = "TotalOrderedQty"
freq: str = "H"
i: int = 1

pandas_df = pd.DataFrame(
    {
        TIME_COLUMN_NAME: pd.date_range(
            start="2000-01-01", periods=data_length, freq=freq
        ),
        TARGET_COLUMN_NAME: np.arange(data_length).astype(float)
        + np.random.rand(data_length)
        + i * 5,
    }
)

from azureml.core import Workspace, Datastore, Dataset
import pandas as pd

ws = Workspace.from_config()
datastore = ws.get_default_datastore()
dataset = Dataset.Tabular.register_pandas_dataframe(
    pandas_df, (datastore, "samples/timeseries"), "timeseries_ds", show_progress=True
)
