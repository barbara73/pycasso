"""
Black-out Factory

Depending on Modality and Manufacturer, different amount of pixels must be blackend.
Also, the image size and photometric interpretation is different
for different manufacturers and modalities.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np
from pydicom import Dataset

from .update_dicom_tags import update_ds


@dataclass
class Philips:
    """Philips manufacturer"""
    dataset: Dataset

    def process_image(self):
        """Different process for different photometric interpretation and image size."""
        img = self.dataset.pixel_array

        if self.dataset.PhotometricInterpretation == 'MONOCHROME2':
            self.dataset.PhotometricInterpretation = 'YBR_FULL'

        if self.dataset.PhotometricInterpretation == 'YBR_FULL_422':
            try:
                img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
            except IndexError:
                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
            finally:
                self.dataset.PhotometricInterpretation = 'RGB'

        try:
            img[:, 0:round(img.shape[1] * 0.1), :, :] = 0
        except IndexError:
            img[0:round(img.shape[0] * 0.1), :] = 0

        self.dataset.PixelData = img
        return update_ds(self.dataset)


@dataclass
class Toshiba:
    """Toshiba manufacturer"""
    dataset: Dataset

    def process_image(self):
        """Different process for different photometric interpretation and image size."""
        img = self.dataset.pixel_array
        if self.dataset.PhotometricInterpretation == 'YBR_FULL_422':
            try:
                img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
            except IndexError:
                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
            finally:
                self.dataset.PhotometricInterpretation = 'RGB'

        try:
            img[:, 0:70, :, :] = 0
        except IndexError:
            img[0:70, :] = 0

        self.dataset.PixelData = img
        return update_ds(self.dataset)


@dataclass
class GeneralElectrics:
    """GE manufacturer"""
    dataset: Dataset

    def process_image(self):
        """Different process for different photometric interpretation and image size."""
        img = self.dataset.pixel_array
        if self.dataset.PhotometricInterpretation == 'RGB':
            try:
                img[:, 0:round(img.shape[1] * 0.072), :, :] = 0
            except IndexError:
                img[0:round(img.shape[0] * 0.072), :, :] = 0

        if self.dataset.PhotometricInterpretation == 'YBR_FULL_422':
            try:
                img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
                img[:, 0:50, :, :] = 0
            except IndexError:
                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
                img[0:50, :, :] = 0

        self.dataset.PixelData = img
        self.dataset.PhotometricInterpretation = 'RGB'
        return update_ds(self.dataset)


class AbstractModality(ABC):
    """Abstract class"""

    @staticmethod
    @abstractmethod
    def blackout_by_manufacturer(dataset):
        pass


@dataclass
class USModality(AbstractModality):
    """US (ultra sound) modality"""
    dataset: Dataset

    def blackout_by_manufacturer(self):
        """Different manufacturers need different process."""
        if str(self.dataset.Manufacturer).find('philips'):
            return Philips(self.dataset).process_image()

        if 'toshiba'.casefold() in self.dataset.Manufacturer:
            return Toshiba(self.dataset).process_image()

        if 'GE' in self.dataset.Manufacturer:
            return GeneralElectrics(self.dataset).process_image()


@dataclass
class MRModality(AbstractModality):
    """MR (magnet resonance tomography) modality"""
    dataset: Dataset

    def blackout_by_manufacturer(self):
        raise NotImplementedError


@dataclass
class CTModality(AbstractModality):
    """CT (computed tomography) modality"""
    dataset: Dataset

    def blackout_by_manufacturer(self):
        """Different manufacturers need different process."""
        if 'agfa'.casefold() in self.dataset.Manufacturer:
            return Toshiba(self.dataset).process_image()


@dataclass
class CRModality(AbstractModality):
    """CR (computed radiology) modality"""
    dataset: Dataset

    def blackout_by_manufacturer(self):
        raise NotImplementedError


def blackout(dataset):
    """
    # TODO: check if Modality filter can be removed!
    Different modalities need different processes.
    SOPClassUID is more exact.
    """
    if dataset.Modality == 'US' and dataset.SOPClassUID == '1.2.840.10008.5.1.4.1.1.3.1':
        return USModality(dataset)

    if dataset.Modality == 'MR' and dataset.SOPClassUID == '1.2.840.10008.5.1.4.1.1.4':
        return MRModality(dataset)

    if dataset.Modality == 'CT' and dataset.SOPClassUID == '1.2.840.10008.5.1.4.1.1.2':
        return CTModality(dataset)

    # TODO: include other modalities or rather SOPClassUIDs!
    if dataset.Modality == 'CR':
        return CRModality(dataset)

