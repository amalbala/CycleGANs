# @title

import cv2
import os
from matplotlib.pyplot import imread
from glob import glob

import numpy as np

dataset_path = '/media/antonio/Data/DataSets/Projects/Stickerizer/FaceToSticker'


class DataLoader():
    def __init__(self, dataset_name, img_res=(128, 128, 3)):
        self.dataset_name = dataset_name
        self.img_res = img_res

    def load_data(self, domain, batch_size=1, is_testing=False):
        data_type = "train" if not is_testing else "test"
        dataset_name = self.dataset_name + "_{}".format(domain)
        path = glob('%s/%s/%s/*' %
                    (dataset_path, dataset_name, data_type))

        batch_images = np.random.choice(path, size=batch_size)

        imgs = []
        for img_path in batch_images:
            img = self.imread(img_path)
            if not is_testing:
                img = cv2.resize(img, self.img_res)

                if np.random.random() > 0.5:
                    img = np.fliplr(img)
            else:
                img = cv2.resize(img, self.img_res)

            imgs.append(img)

        imgs = np.array(imgs)/127.5 - 1.

        return imgs

    def load_batch(self, batch_size=1, is_testing=False):
        data_type = "train" if not is_testing else "validation"
        path_A_wc = '%s/%s_A/%s/*' % (dataset_path,
                                      self.dataset_name, data_type)
        path_A = glob(path_A_wc)

        path_B_wc = '%s/%s_B/%s/*' % (dataset_path,
                                      self.dataset_name, data_type)
        path_B = glob(path_B_wc)

        self.n_batches = int(min(len(path_A), len(path_B)) / batch_size)
        total_samples = self.n_batches * batch_size

        # Sample n_batches * batch_size from each path list so that model sees all
        # samples from both domains
        path_A = np.random.choice(path_A, total_samples, replace=False)
        path_B = np.random.choice(path_B, total_samples, replace=False)

        for i in range(self.n_batches-1):
            batch_A = path_A[i*batch_size:(i+1)*batch_size]
            batch_B = path_B[i*batch_size:(i+1)*batch_size]
            imgs_A, imgs_B = [], []
            for img_A, img_B in zip(batch_A, batch_B):
                img_A = self.imread(img_A)
                img_B = self.imread(img_B)

                img_A = cv2.resize(img_A, self.img_res)
                img_B = cv2.resize(img_B, self.img_res)

                if not is_testing and np.random.random() > 0.5:
                    img_A = np.fliplr(img_A)
                    img_B = np.fliplr(img_B)

                imgs_A.append(img_A)
                imgs_B.append(img_B)

            imgs_A = np.array(imgs_A)/127.5 - 1.
            imgs_B = np.array(imgs_B) * 2 - 1.

            yield imgs_A, imgs_B

    def imread(self, path):
        im = cv2.imread(path)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        return im
