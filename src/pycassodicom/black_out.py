"""
PycassoDicom

Script for de-identifying images with burned in annotation.
Depending on manufacturer and image size, pixel can be blackened.
Some images are of no use for the researcher or have too much identifying information.
They will be deleted (set to None).
"""
from pydicom import Dataset

from .blackout_factory import blackout


def blacken_pixels(dataset: Dataset) -> Dataset:
    """
    Blacken pixel based on manufacturer, modality and image size.

    You can filter out all the secondary image types already in this step.
    """
    try:
        if 'PRIMARY' in (x for x in dataset.ImageType):
            return blackout(dataset)

        return dataset

    except AttributeError:
        return dataset


def delete_dicom(dataset: Dataset) -> bool:
    """
    True if the dicom can be deleted.
    """
    try:
        if 'PRIMARY' not in (x for x in dataset.ImageType) \
                or 'INVALID' in (x for x in dataset.ImageType):
            return True

        if dataset.Modality == 'US' and dataset.NumberOfFrames is None:
            return True

        if 'SECONDARY' in (x for x in dataset.ImageType) \
                or dataset.SOPClassUID == '1.2.840.10008.5.1.4.1.1.7':
            return True

        return False

    except AttributeError:
        return False
