import torch
import torch.nn as nn
import torch.nn.functional as F


class UserTower(nn.Module):
    """
    Converts a user ID into a dense user embedding.
    """

    def __init__(
        self,
        num_users: int,
        embedding_dim: int = 128,
        hidden_dim: int = 256,
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=num_users,
            embedding_dim=embedding_dim,
        )

        self.network = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, embedding_dim),
        )

    def forward(self, user_ids):
        x = self.embedding(user_ids)
        x = self.network(x)

        # Normalize for cosine similarity
        return F.normalize(x, p=2, dim=1)


class ItemTower(nn.Module):
    """
    Converts an item/article ID into a dense item embedding.
    """

    def __init__(
        self,
        num_items: int,
        embedding_dim: int = 128,
        hidden_dim: int = 256,
    ):
        super().__init__()

        self.embedding = nn.Embedding(
            num_embeddings=num_items,
            embedding_dim=embedding_dim,
        )

        self.network = nn.Sequential(
            nn.Linear(embedding_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, embedding_dim),
        )

    def forward(self, item_ids):
        x = self.embedding(item_ids)
        x = self.network(x)

        # Normalize for cosine similarity
        return F.normalize(x, p=2, dim=1)


class TwoTowerModel(nn.Module):
    """
    Two-Tower Neural Recommendation Model.

    User Tower:
        user_id -> user embedding

    Item Tower:
        item_id -> item embedding

    Training objective:
        maximize similarity between positive user-item pairs
        while minimizing similarity to negative items.
    """

    def __init__(
        self,
        num_users: int,
        num_items: int,
        embedding_dim: int = 128,
        hidden_dim: int = 256,
    ):
        super().__init__()

        self.user_tower = UserTower(
            num_users=num_users,
            embedding_dim=embedding_dim,
            hidden_dim=hidden_dim,
        )

        self.item_tower = ItemTower(
            num_items=num_items,
            embedding_dim=embedding_dim,
            hidden_dim=hidden_dim,
        )

    def encode_users(self, user_ids):
        return self.user_tower(user_ids)

    def encode_items(self, item_ids):
        return self.item_tower(item_ids)

    def forward(self, user_ids, item_ids):
        user_embeddings = self.encode_users(user_ids)
        item_embeddings = self.encode_items(item_ids)

        # Cosine similarity because embeddings are normalized
        similarity = torch.sum(
            user_embeddings * item_embeddings,
            dim=1,
        )

        return similarity

    def full_item_scores(self, user_ids):
        """
        Calculate similarity between users and every item.

        Used later for recommendation generation.
        """

        user_embeddings = self.encode_users(user_ids)

        all_item_ids = torch.arange(
            self.item_tower.embedding.num_embeddings,
            device=user_ids.device,
        )

        item_embeddings = self.encode_items(all_item_ids)

        return torch.matmul(
            user_embeddings,
            item_embeddings.T,
        )