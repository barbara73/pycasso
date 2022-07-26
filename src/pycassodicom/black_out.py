"""
Pycasso

"""
from typing import Optional

from pydicom import Dataset
from pydicom.uid import ExplicitVRLittleEndian


def blacken_pixels(ds: Dataset) -> Dataset:
    """
    Blacken pixel based on manufacturer and image size.
    """
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
    return ds


def delete_dicom(ds: Dataset) -> Optional[Dataset]:
    if (ds.Modality == 'CT') \
            and (ds.Manufacturer == 'SIEMENS') \
            and (ds.ImageType[:4] == ['DERIVED', 'SECONDARY', 'OTHER', 'VPCT']) \
            and (ds.Rows == 968) \
            and (ds.Columns == 968):
        return None
    return ds
