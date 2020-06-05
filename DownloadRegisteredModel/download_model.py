from azureml.core.model import Model
from pathlib import Path

original_model_path = Model.get_model_path('seer')
print(original_model_path)

raw_path = Path(original_model_path)

for path in raw_path.rglob('*'):
    print(path.name)
