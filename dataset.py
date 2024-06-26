from PIL import Image
import os
import numpy as np
from torch.utils.data import Dataset


class HorseZebraDataset(Dataset):
    def __init__(self, root_zebra, root_horse, transform=None):
        self.root_zebra = root_zebra
        self.root_horse = root_horse
        self.transform = transform

        self.zebra_images = os.listdir(root_zebra)
        self.horse_images = os.listdir(root_horse)
        # datasets may have different lenghts
        self.zebra_len = len(self.zebra_images)
        self.horse_len = len(self.horse_images)
        self.length_dataset = max(self.zebra_len, self.horse_len)

    def __len__(self):
        return self.length_dataset

    def __getitem__(self, index):
        # index could be greater than dataset
        zebra_img = self.zebra_images[index % self.zebra_len]
        horse_img = self.horse_images[index % self.horse_len]

        zebra_path = os.path.join(self.root_zebra, zebra_img)
        horse_path = os.path.join(self.root_horse, horse_img)

        zebra_img = np.array(Image.open(zebra_path).convert("RGB"))
        horse_img = np.array(Image.open(horse_path).convert("RGB"))

        if self.transform:
            augmentations = self.transform(image=zebra_img, image0=horse_img)
            zebra_img = augmentations["image"]
            # image0 since set like this in config
            horse_img = augmentations["image0"]

        return zebra_img, horse_img
