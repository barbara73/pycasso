import pytest

from src.pycassodicom.blackout_factory import MonoChrome2, PhotometricInterpretation
from src.pycassodicom.blackout_factory import blackout, USModality


def test_can_get_image(us_dataset):
    """Test that one can get image as pixel array."""
    assert PhotometricInterpretation(us_dataset).get_image().shape[0] == 775
    assert MonoChrome2(us_dataset).get_image().shape[0] == 775


def test_can_write_dataset(us_dataset):
    """Test can put image back to dataset."""
    photo = PhotometricInterpretation(us_dataset)
    assert photo.write_dataset(photo.get_image()).BitsStored == 16


@pytest.mark.skip('Setup not correct')
def test_can_make_black(transfer_syntax_ds):
    """Test that pixels get black."""
    photo = PhotometricInterpretation(transfer_syntax_ds)
    assert photo.get_image().min() == -2048
    dataset = photo.make_black(50)

    assert MonoChrome2(dataset).get_image() == 0


# --------------------------------------------------------------------------------
# Integration Tests
# ---------------------------------------------------------------------------------

def test_process_by_manufacturer(ge_dataset):
    """Test that correct manufacturer is processed."""
    us = USModality(ge_dataset)
    assert us.process_by_manufacturer().PhotometricInterpretation == 'RGB'


def test_process_by_philips(us_dataset):
    """Test that correct manufacturer is processed."""
    us = USModality(us_dataset)
    assert us.process_by_manufacturer().PhotometricInterpretation == 'MONOCHROME2'


def test_blackout_modality_us(us_dataset):
    """Test that whole process works."""
    changed_ds = blackout(us_dataset)
    assert changed_ds.SOPClassUID == '1.2.840.10008.5.1.4.1.1.6.124'
    assert changed_ds.BurnedInAnnotation == 'NO'
    assert changed_ds.PatientIdentityRemoved == 'YES'


def test_blackout_modality_ct(ct_dataset):
    """Test blackout with CT works."""
    assert ct_dataset.SOPClassUID == '1.2.840.10008.5.1.4.1.1.224'
    assert ct_dataset.BurnedInAnnotation == 'YES'
    changed_ds = blackout(ct_dataset)
    assert changed_ds.PatientIdentityRemoved == 'YES'
