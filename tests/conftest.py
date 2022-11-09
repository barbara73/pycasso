"""
Conftest
Fixtures for testing
"""
import numpy as np
import pytest
from dicomgenerator.factory import DataElementFactory, CTDatasetFactory
from pydicom import Dataset
from pydicom.uid import ExplicitVRLittleEndian


@pytest.fixture
def ct_dataset() -> Dataset:
    """Tiny Dataset that can be used with some_rules and a_core_with_some_rules"""
    dataset = Dataset()
    dataset.add(DataElementFactory(tag='PatientID', value='12345'))
    dataset.add(DataElementFactory(tag='Modality', value='CT'))
    dataset.add(DataElementFactory(tag='ImageType', value='DERIVED\INVALID\OTHER\VPCT\clablabla'))
    dataset.add(DataElementFactory(tag='Rows', value=968))
    dataset.add(DataElementFactory(tag='Columns', value=968))
    dataset.add(DataElementFactory(tag='PatientName', value='Martha'))
    dataset.add(DataElementFactory(tag=(0x5010, 0x3000), value=b'Sensitive data'))
    dataset.add(DataElementFactory(tag=(0x1013, 0x0001), value=b'private tag'))
    block = dataset.private_block(0x00B1, 'TestCreator', create=True)
    block.add_new(0x01, 'SH', 'my testvalue')

    dataset.file_meta = Dataset()
    img = np.ones(shape=(dataset.Rows, dataset.Columns, 3), dtype=np.uint16) * 255
    dataset.PixelData = img.tobytes()
    dataset.SOPClassUID = '1.2.840.10008.5.1.4.1.1.224'
    dataset.Manufacturer = 'PHILIPS'

    dataset.BurnedInAnnotation = 'YES'
    dataset.PatientIdentityRemoved = 'NO'
    dataset.DeidentificationMethodCodeSequence = []
    dataset.PhotometricInterpretation = 'RGB'
    dataset.BitsAllocated = 16
    dataset.SamplesPerPixel = 1
    dataset.BitsStored = 16
    dataset.PixelRepresentation = 1
    dataset.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    return dataset


@pytest.fixture
def us_dataset() -> Dataset:
    """Tiny Dataset that can be used with some_rules and a_core_with_some_rules"""
    dataset = Dataset()
    dataset.add(DataElementFactory(tag='Modality', value='US'))
    dataset.add(DataElementFactory(tag='Columns', value=1024))
    dataset.add(DataElementFactory(tag='Rows', value=775))
    block = dataset.private_block(0x00B1, 'TestCreator', create=True)
    block.add_new(0x01, 'SH', 'my testvalue')

    dataset.file_meta = Dataset()
    img = np.ones(shape=(dataset.Rows, dataset.Columns, 3), dtype=np.uint16) * 255
    dataset.PixelData = img.tobytes()
    dataset.SOPClassUID = '1.2.840.10008.5.1.4.1.1.3.124'
    dataset.Manufacturer = 'PHILIPS'
    dataset.ImageType = 'DERIVED\PRIMARY\OTHER\VPCT\clablabla'
    dataset.BurnedInAnnotation = 'YES'
    dataset.PatientIdentityRemoved = 'NO'
    dataset.DeidentificationMethodCodeSequence = []

    dataset.PhotometricInterpretation = 'MONOCHROME2'
    dataset.BitsAllocated = 16
    dataset.SamplesPerPixel = 1
    dataset.BitsStored = 16
    dataset.PixelRepresentation = 1
    dataset.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    return dataset


@pytest.fixture
def ge_dataset() -> Dataset:
    """Tiny Dataset that can be used with some_rules and a_core_with_some_rules"""
    dataset = Dataset()
    dataset.add(DataElementFactory(tag='Modality', value='US'))
    dataset.add(DataElementFactory(tag='Columns', value=1024))
    dataset.add(DataElementFactory(tag='Rows', value=775))
    block = dataset.private_block(0x00B1, 'TestCreator', create=True)
    block.add_new(0x01, 'SH', 'my testvalue')

    dataset.DeidentificationMethodCodeSequence = []
    dataset.Manufacturer = 'GE blabla'
    dataset.file_meta = Dataset()
    img = np.ones(shape=(dataset.Rows, dataset.Columns, 3), dtype=np.uint16) * 255
    dataset.PixelData = img.tobytes()
    dataset.PhotometricInterpretation = 'RGB'
    dataset.BitsAllocated = 16
    dataset.SamplesPerPixel = 1
    dataset.BitsStored = 16
    dataset.PixelRepresentation = 1
    dataset.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    return dataset


@pytest.fixture
def transfer_syntax_ds() -> Dataset:
    """Transfer Syntax is needed for interpreting PixelData."""
    dataset = CTDatasetFactory()
    dataset.file_meta = Dataset()
    dataset.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    dataset.ImageType = 'DERIVED\SECONDARY\OTHER\VPCT\clablabla'
    ds_sq = Dataset()
    ds_sq.CodeValue = ''
    dataset.DeidentificationMethodCodeSequence.append(ds_sq)
    return dataset
