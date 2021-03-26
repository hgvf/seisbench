from torch.utils.data import Dataset


class GenericGenerator(Dataset):
    def __init__(self, dataset):
        """
        A generic data generator which can be used to build preprocessing and data augmentation pipelines.
        The data generator subclasses the pytorch Dataset class and can therefore be used directly with DataLoaders in pytorch.
        The processing pipeline of the generator is defined through a series of processing steps or augmentations.
        For each data sample, the generator calls the augmentations in order.
        Information between the augmentation steps is passed through a state dict.
        The state dict is a python dictionary mapping keys to a tuple (data, metadata).
        In getitem, the generator automatically populates the initial dictionary with the waveforms
        and the corresponding metadata for the row from the underlying data set using the key "X".
        After applying all augmentation, the generator removes all metadata information.
        This means that the output dict only maps keys to the data part.
        Any metadata that should be output needs to explicitly be written to data.

        Augmentation can be either callable classes of functions.
        Functions are usually best suited for simple operations, while callable classes offer more configuration options.
        SeisBench already offers a set of standard augmentations for augmentation and preprocessing,
        e.g., for window selection, data normalization or different label encodings,
        which should cover many common use cases.
        For details on implementing custom augmentations we suggest looking at the examples provided.

        SeisBench augmentations by default always work on the key "X".
        Label generating augmentations by default put labels into the key "y".
        However, for more complex workflows, the augmentations can be adjusted using the key argument.
        This allows in particular none-sequential augmentation sequences.

        :param dataset: The underlying SeisBench data set.
        """
        self._augmentations = []
        self.dataset = dataset
        super().__init__()

    def augmentation(self, f):
        """
        Decorator for augmentations.
        """
        self._augmentations.append(f)

        return f

    def __str__(self):
        summary = f"GenericGenerator with {len(self._augmentations)} augmentations:\n"
        for i, aug in enumerate(self._augmentations):
            summary += f" {i + 1}.\t{str(aug)}\n"
        return summary

    def __len__(self):
        return len(self.dataset)

    def __iter__(self):
        return self

    def __getitem__(self, idx):
        state_dict = {"X": self.dataset.get_sample(idx)}

        # Recursive application of augmentation processing methods
        for func in self._augmentations:
            func(state_dict)

        # Remove all metadata from the output
        state_dict = {k: v[0] for k, v in state_dict.items()}

        return state_dict