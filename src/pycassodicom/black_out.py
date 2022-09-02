"""
PycassoDicom

Script for de-identifying images with burned in annotation.
Depending on manufacturer and image size, pixel can be blackened.
Some images are of no use for the researcher or have too much identifying information.
They will be deleted (set to None).
"""
import numpy as np
from pydicom import Dataset
from pydicom.uid import ExplicitVRLittleEndian


def update_ds(ds: Dataset) -> Dataset:
    """
    Since the image is changed, the dicom tags have to change, too.
    - no burned-in anymore
    - transfer syntax changes, too
    - add, which method was used
    """
    ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    ds.BurnedInAnnotation = 'NO'
    ds.DeidentificationMethod = '{Per DICOM PS 3.15 AnnexE. Details in 0012,0064, removed burned-in ' \
                                'annotation by blackening pixels}'
    text = ds.DeidentificationMethodCodeSequence
    ds.DeidentificationMethodCodeSequence = f'{text}/113101'
    return ds


def blacken_pixels(ds: Dataset) -> Dataset:
    """
    Blacken pixel based on manufacturer, modality and image size.
    """
    try:
        if 'PRIMARY' in ds.ImageType:
            # if ds.Modality == 'CT':
                ## SECONDARY not included anymore!!
                # if ds.Manufacturer == 'Agfa' \
                #         and ds.Rows == 775 and ds.Columns == 1024:
                #     img = ds.pixel_array
                #     img[0:round(img.shape[0] * 0.07), :, :] = 0  # ca. 7%
                #     ds.PhotometricInterpretation = 'YBR_FULL'
                #     ds.PixelData = img
                #     ds = update_ds(ds)

            if ds.Modality == 'US':
                ## GE
                if 'GE' in (x for x in ds.Manufacturer):
                    print('here')
                    img = ds.pixel_array
                    if ds.PhotometricInterpretation == 'RGB':
                        try:
                            img[:, 0:round(img.shape[1] * 0.072), :, :] = 0
                        except:
                            img[0:round(img.shape[0] * 0.072), :, :] = 0

                    if ds.PhotometricInterpretation == 'YBR_FULL_422':
                        try:
                            img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
                            img[:, 0:50, :, :] = 0
                        except:
                            img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
                            img[0:50, :, :] = 0

                        finally:
                            ds.PixelData = img
                            ds.PhotometricInterpretation = 'RGB'
                            ds = update_ds(ds)

                    ## PHILIPS
                    if 'philips' in (x.casefold() for x in ds.Manufacturer):
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
                            ds = update_ds(ds)

                    if 'toshiba' in (x.casefold() for x in ds.Manufacturer):
                        img = ds.pixel_array
                        if ds.PhotometricInterpretation == 'YBR_FULL_422':
                            try:
                                img = np.repeat(img[:, :, :, 0, np.newaxis], 3, axis=3)
                            except:
                                img = np.repeat(img[:, :, 0, np.newaxis], 3, axis=2)
                            finally:
                                ds.PhotometricInterpretation = 'RGB'

                        try:
                            img[:, 0:70, :, :] = 0
                        except:
                            img[0:70, :] = 0
                        finally:
                            ds.PixelData = img
                            ds = update_ds(ds)

            return ds

    except AttributeError:
        return ds


def delete_dicom(ds: Dataset) -> bool:
    """
    Return None if the dicom can be deleted.
    """
    try:
        if 'PRIMARY' not in (x for x in ds.ImageType) \
                or 'INVALID' in (x for x in ds.ImageType):
            return True

        if ds.Modality == 'US' and ds.NumberOfFrames is None:
            return True

        # if ds.ManufacturerModelName == 'TUS-AI900' \
        #         and 'CARDIOLOGY' not in ds.ImageType:
        #     return True

        return False

    except AttributeError:
        return False

