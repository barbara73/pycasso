"""
PycassoDicom

Script for de-identifying images with burned in annotation.
Depending on manufacturer and image size, pixel can be blackened.
Some images are of no use for the researcher or have too much identifying information.
They will be deleted (set to None).
"""
from typing import Optional

from pydicom import Dataset
from pydicom.uid import ExplicitVRLittleEndian


def blacken_pixels(ds: Dataset) -> Dataset:
    """
    Blacken pixel based on manufacturer, modality and image size.
    """
    try:
        if (ds.Modality == 'CT') \
                and (ds.Manufacturer == 'Agfa') \
                and (ds.Rows == 775) \
                and (ds.Columns == 1024):
            img = ds.pixel_array
            img[0:round(img.shape[0] * 0.07), :] = 0  # ca. 7%

            ds.PixelData = img.tobytes()
            ds.PhotometricInterpretation = 'YBR_FULL'  # important!!
            ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian  # because changed
            return ds

    except AttributeError:
        return ds

    return ds


def delete_dicom(ds: Dataset) -> Optional[Dataset]:
    """
    Return None if the dicom can be deleted.
    """
    try:
        if (ds.Modality == 'CT') \
                and (ds.Manufacturer == 'SIEMENS') \
                and (ds.ImageType[:4] == ['DERIVED', 'SECONDARY', 'OTHER', 'VPCT']) \
                and (ds.Rows == 968) \
                and (ds.Columns == 968):
            return None

    except AttributeError:
        return ds

    return ds
