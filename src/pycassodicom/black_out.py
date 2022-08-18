"""
PycassoDicom

Script for de-identifying images with burned in annotation.
Depending on manufacturer and image size, pixel can be blackened.
Some images are of no use for the researcher or have too much identifying information.
They will be deleted (set to None).
"""
from typing import Optional

import numpy as np
from pydicom import Dataset
from pydicom.uid import ExplicitVRLittleEndian


def blacken_pixels(ds: Dataset) -> Dataset:
    """
    Blacken pixel based on manufacturer, modality and image size.
    """
    try:
        ## Modality CT and Agfa
        if ds.Modality == 'CT' and ds.Manufacturer == 'Agfa' \
                and ds.Rows == 775 and ds.Columns == 1024:
            img = ds.pixel_array
            img[0:round(img.shape[0] * 0.07), :, :] = 0  # ca. 7%

            ds.PixelData = img
            ds.PhotometricInterpretation = 'YBR_FULL'                   # important!!
            ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian     # because changed

        ## Modality US and PHILIPS
        if ds.Modality == 'US' and 'philips' in (x.casefold() for x in ds.Manufacturer) \
                and ds.Rows == 600 and ds.Columns == 800:
            img = ds.pixel_array

            if ds.PhotometricInterpretation == 'MONOCHROME2':
                ds.PhotometricInterpretation = 'YBR_FULL'

            if ds.PhotometricInterpretation == 'YBR_FULL_422':
                try:
                    img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
                except:
                    img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
                finally:
                    ds.PhotometricInterpretation = 'RGB'

            try:
                img[:, 0:round(img.shape[1] * 0.1), :, :] = 0
            except:
                img[0:round(img.shape[0] * 0.1), :] = 0
            finally:
                ds.PixelData = img
                ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

        # if ds.ManufacturerModelName in ('EPIQ 7C', 'iE33') and ds.Rows == 768 and ds.Columns == 1024:
        #     img = ds.pixel_array
        #
        #     if ds.PhotometricInterpretation == 'MONOCHROME2':
        #         ds.PhotometricInterpretation = 'YBR_FULL'
        #
        #     img[0:round(img.shape[0] * 0.1), :] = 0
        #     ds.PixelData = img
        #     ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian  # because changed

        ## Modality US and GE
        if ds.ManufacturerModelName == 'Vivid E95' and ds.Rows == 708:
            img = ds.pixel_array
            try:
                img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
                img[:, 0:round(img.shape[1] * 0.072), :, :] = 0
            except:
                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
                img[0:round(img.shape[1] * 0.03), :, :] = 0

            finally:
                ds.PixelData = img
                ds.PhotometricInterpretation = 'RGB'
                ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian  # because changed

        if ds.ManufacturerModelName == 'Vivid E95' and ds.Rows == 758:
            img = ds.pixel_array
            try:
                img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
                img[:, 0:round(img.shape[1] * 0.065), :, :] = 0
            except:
                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
                img[0:round(img.shape[0] * 0.065), :, :] = 0
            finally:
                ds.PixelData = img
                ds.PhotometricInterpretation = 'RGB'  # important!!
                ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian  # because changed

        if ds.ManufacturerModelName == 'Vivid E9':
            img = ds.pixel_array
            try:
                img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
                img[:, 0:round(img.shape[1] * 0.1), :, :] = 0
            except:
                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
                img[0:round(img.shape[0] * 0.1), :, :] = 0
            finally:
                ds.PixelData = img
                ds.PhotometricInterpretation = 'RGB'  # important!!
                ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian  # because changed

        if ds.ManufacturerModelName == 'TUS-AI900' and 'CARDIOLOGY' in ds.ImageType:
            img = ds.pixel_array
            if ds.PhotometricInterpretation == 'RGB':
                try:
                    img[:, 0:round(img.shape[1] * 0.072), :, :] = 0
                except:
                    img[0:round(img.shape[0] * 0.072), :, :] = 0
            else:
                try:
                    img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
                    img[:, 0:round(img.shape[1] * 0.072), :, :] = 0
                except:
                    img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
                    img[0:round(img.shape[0] * 0.072), :, :] = 0
                finally:
                    ds.PhotometricInterpretation = 'RGB'

            ds.PixelData = img
            ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian  # because changed

        return ds

    except AttributeError:
        return ds


def delete_dicom(ds: Dataset) -> Optional[Dataset]:
    """
    Return None if the dicom can be deleted.
    """
    try:
        if ds.Modality == 'CT' \
                and ds.Manufacturer == 'SIEMENS' \
                and ds.ImageType[:4] == ['DERIVED', 'SECONDARY', 'OTHER', 'VPCT'] \
                and ds.Rows == 968 \
                and ds.Columns == 968:
            return None

        if ds.Modality == 'US' and ds.NumberOfFrames is None:
            return None

        # if (ds.ManufacturerModelName == 'iE33') \
        #         and (ds.ImageType == ['ORIGINAL', 'PRIMARY', 'INVALID']):
        #     return None

        if ds.ManufacturerModelName == 'Vivid E95' \
                and ds.Rows == 708 \
                and ds.NumberOfFrames is None \
                and ds.BurnedInAnnotation is None:
            return None

        if ds.ManufacturerModelName == 'TUS-AI900' \
                and 'CARDIOLOGY' not in ds.ImageType:
            return None

        return ds

    except AttributeError:
        return ds

