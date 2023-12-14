import os
from pathlib import Path
import logging

project_name = "Image_AutoTrainer"



list_of_dirs = [
    ".github/workflows/.gitkeep",
    f"{project_name}/__init__.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/info/__init__.py",
    f"{project_name}/utils/config.py",
    f"{project_name}/utils/model.py",
    f"{project_name}/utils/data_manager.py",
    f"{project_name}/utils/model_configure.py",
    f"{project_name}/utils/callbacks.py",
    f"{project_name}/utils/info/exception.py",
    f"{project_name}/utils/info/logger.py",
    f"{project_name}/main.py",
    f"{project_name}/predict_engine.py",
    f"{project_name}/train_engine.py",
    f"{project_name}/requirements.txt",
    f"{project_name}/test.txt",
    "setup.py",
]

for filepath in list_of_dirs:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    print(f"Filedir: {filedir}, filename : {filename}")

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory {filedir} for filename {filename}")


    if (not os.path.exists(filedir)) or (os.path.getsize(filedir) ==0):
        with open(filepath, 'w') as f:
            pass

        logging.info(f"file path created {filepath}")

    else:
        logging.info(f"File Exists {filepath}")
