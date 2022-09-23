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


class AbstractManufacturer(ABC):
    """Abstract class"""
    @abstractmethod
    def process_image(self):
        """Process dicom image for blackening pixels."""


@dataclass
class Philips(AbstractManufacturer):
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
            except:
                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
            finally:
                self.dataset.PhotometricInterpretation = 'RGB'

        try:
            img[:, 0:round(img.shape[1] * 0.1), :, :] = 0
        except:
            img[0:round(img.shape[0] * 0.1), :] = 0

        self.dataset.PixelData = img
        return update_ds(self.dataset)


@dataclass
class Toshiba(AbstractManufacturer):
    """Toshiba manufacturer"""
    dataset: Dataset

    def process_image(self):
        """Different process for different photometric interpretation and image size."""
        img = self.dataset.pixel_array
        if self.dataset.PhotometricInterpretation == 'YBR_FULL_422':
            try:
                img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
            except:
                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
            finally:
                self.dataset.PhotometricInterpretation = 'RGB'

        try:
            img[:, 0:70, :, :] = 0
        except:
            img[0:70, :] = 0

        self.dataset.PixelData = img
        return update_ds(self.dataset)


@dataclass
class GeneralElectrics(AbstractManufacturer):
    """GE manufacturer"""
    dataset: Dataset

    def process_image(self):
        """Different process for different photometric interpretation and image size."""
        img = self.dataset.pixel_array
        if self.dataset.PhotometricInterpretation == 'RGB':
            try:
                img[:, 0:round(img.shape[1] * 0.072), :, :] = 0
            except:
                img[0:round(img.shape[0] * 0.072), :, :] = 0

        if self.dataset.PhotometricInterpretation == 'YBR_FULL_422':
            try:
                img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
                img[:, 0:50, :, :] = 0
            except:
                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
                img[0:50, :, :] = 0

        self.dataset.PixelData = img
        self.dataset.PhotometricInterpretation = 'RGB'
        return update_ds(self.dataset)


@dataclass
class AbstractModality(ABC):
    """Abstract class"""
    dataset: Dataset

    def blackout_by_manufacturer(self):
        """Different manufacturers need different process."""
        if 'philips'.casefold() in self.dataset.Manufacturer:
            return Philips(self.dataset).process_image()

        if 'toshiba'.casefold() in self.dataset.Manufacturer:
            return Toshiba(self.dataset).process_image()

        if 'GE' in self.dataset.Manufacturer:
            return GeneralElectrics(self.dataset).process_image()



@dataclass
class USModality(AbstractModality):
    """US (ultra sound) modality"""
    dataset: Dataset


@dataclass
class MRModality(AbstractModality):
    """MR (magnet resonance tomography) modality"""
    dataset: Dataset


@dataclass
class CTModality(AbstractModality):
    """CT (computed tomography) modality"""
    dataset: Dataset


@dataclass
class CRModality(AbstractModality):
    """CR (computed radiology) modality"""
    dataset: Dataset


@dataclass
class BlackOutFactory:
    """Black out by modality."""
    dataset: Dataset

    def blackout(self):
        """Different modalities need different processes."""
        if self.dataset.Modality == 'US':
            return USModality(self.dataset).blackout_by_manufacturer()

        if self.dataset.Modality == 'MR':
            return MRModality(self.dataset).blackout_by_manufacturer()

        if self.dataset.Modality == 'CT':
            return CTModality(self.dataset).blackout_by_manufacturer()

        if self.dataset.Modality == 'CR':
            return CRModality(self.dataset).blackout_by_manufacturer()
