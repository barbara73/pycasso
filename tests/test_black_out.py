"""
Test black out
"""
import pytest

from src.pycassodicom.black_out import delete_dicom, blacken_pixels


def test_blacken_pixels_returns_same_ds(transfer_syntax_ds):
    """Same data set returned, if no burned-in annotation suspected."""
    assert blacken_pixels(transfer_syntax_ds) == transfer_syntax_ds


def test_blacken_pixels_returns_changed_photometric_interpretation(us_dataset):
    """Data set changed, when manufacturer is PHILIPS and modality is US."""
    ds = blacken_pixels(us_dataset)
    assert ds.PhotometricInterpretation == 'YBR_FULL'


def test_return_unchanged_ds_if_attribute_is_missing(another_dataset):
    """Return unchanged data set if an attribute (dicom tag) is missing."""
    black_ds = blacken_pixels(another_dataset)
    assert black_ds.PhotometricInterpretation == 'RGB'


def test_delete_dicom_returns_true(a_dataset):
    """Return None if data set has specific image type, size and modality."""
    assert delete_dicom(a_dataset) is True


def test_delete_dicom_returns_true_when_nb_frames_is_none(a_dataset):
    """If one condition is different, then image will not be deleted."""
    a_dataset.NumberOfFrames = None
    assert delete_dicom(a_dataset) is True


def test_delete_dicom_returns_false(a_dataset):
    """Return None if data set has specific image type, size and modality."""
    a_dataset.ImageType = 'DERIVED\PRIMARY\OTHER\VPCT\clablabla'
    assert delete_dicom(a_dataset) is False
