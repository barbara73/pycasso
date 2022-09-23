"""
PycassoDicom

Script for de-identifying images with burned in annotation.
Depending on manufacturer and image size, pixel can be blackened.
Some images are of no use for the researcher or have too much identifying information.
They will be deleted (set to None).
"""
from pydicom import Dataset

from .blackout_factory import BlackOutFactory


def blacken_pixels(dataset: Dataset) -> Dataset:
    """
    Blacken pixel based on manufacturer, modality and image size.
    """
    try:
        if 'PRIMARY' in (x for x in dataset.ImageType):
            BlackOutFactory(dataset).blackout()

        return dataset

    except AttributeError:
        return dataset


def delete_dicom(dataset: Dataset) -> bool:
    """
    Return None if the dicom can be deleted.
    """
    try:
        if 'PRIMARY' not in (x for x in dataset.ImageType) \
                or 'INVALID' in (x for x in dataset.ImageType):
            return True

        if dataset.Modality == 'US' and dataset.NumberOfFrames is None:
            return True

        # if ds.ManufacturerModelName == 'TUS-AI900' \
        #         and 'CARDIOLOGY' not in ds.ImageType:
        #     return True

        return False

    except AttributeError:
        return False
