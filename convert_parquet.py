import os
import json
import pandas as pd
import argparse
from pathlib import Path
from tqdm import tqdm

from huggingface_hub import HfApi
import os


if __name__ == "__main__":
    api = HfApi(token=os.getenv("HF_TOKEN"))
    api.upload_folder(
    folder_path="before-arc-parquet/",
    repo_id="taratataw/before-arc",
    repo_type="dataset",
    commit_message="Upload new version of experiments setting 3",
    ignore_patterns=["*.db"]
)