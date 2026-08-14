import pandas as pd
import torch
from torch.utils.data import Dataset


class HMInteractionDataset(Dataset):

    def __init__(self, interactions_path: str):

        self.df = pd.read_parquet(interactions_path)

        required_columns = {
            "user_id",
            "item_id",
        }

        missing = required_columns - set(self.df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

        self.df = self.df[
            ["user_id", "item_id"]
        ].dropna()

        self.df["user_id"] = self.df["user_id"].astype(int)
        self.df["item_id"] = self.df["item_id"].astype(int)

        self.users = self.df["user_id"].values
        self.items = self.df["item_id"].values

    def __len__(self):
        return len(self.df)

    def __getitem__(self, index):

        return (
            torch.tensor(
                self.users[index],
                dtype=torch.long,
            ),
            torch.tensor(
                self.items[index],
                dtype=torch.long,
            ),
        )