from nose import tools

from wfc3tools import calwf3

@tools.raises(OSError)
def test_raises_oserror():
    exec_path = 'IamNOTanEXECUTABLE'

    input_file = 'IamNOTaFILE'

    calwfc3.calwf3(input_file, exec_path=exec_path)


@tools.raises(IOError)
def test_raises_ioerror():
    input_file = 'IamNOTaFILE'

    calwf3.calwf3(input_file)
