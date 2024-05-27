import torch.utils.data
from EnlightenGAN.data.base_data_loader import BaseDataLoader


def CreateDataset(opt):
    dataset = None
    if opt.dataset_mode == 'aligned':
        from EnlightenGAN.data.aligned_dataset import AlignedDataset
        dataset = AlignedDataset()
    elif opt.dataset_mode == 'unaligned':
        from EnlightenGAN.data.unaligned_dataset import UnalignedDataset
        dataset = UnalignedDataset()
    elif opt.dataset_mode == 'unaligned_random_crop':
        from EnlightenGAN.data.unaligned_random_crop import UnalignedDataset
        dataset = UnalignedDataset()
    elif opt.dataset_mode == 'pair':
        from EnlightenGAN.data.pair_dataset import PairDataset
        dataset = PairDataset()
    elif opt.dataset_mode == 'syn':
        from EnlightenGAN.data.syn_dataset import PairDataset
        dataset = PairDataset()
    elif opt.dataset_mode == 'single':
        from EnlightenGAN.data.single_dataset import SingleDataset
        dataset = SingleDataset()
    else:
        raise ValueError("Dataset [%s] not recognized." % opt.dataset_mode)

    print("dataset [%s] was created" % (dataset.name()))
    dataset.initialize(opt)
    return dataset


class CustomDatasetDataLoader(BaseDataLoader):
    def name(self):
        return 'CustomDatasetDataLoader'

    def initialize(self, opt):
        BaseDataLoader.initialize(self, opt)
        self.dataset = CreateDataset(opt)
        self.dataloader = torch.utils.data.DataLoader(
            self.dataset,
            batch_size=opt.batchSize,
            shuffle=not opt.serial_batches,
            num_workers=int(opt.nThreads))

    def load_data(self):
        return self.dataloader

    def __len__(self):
        return min(len(self.dataset), self.opt.max_dataset_size)