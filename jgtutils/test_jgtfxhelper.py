
import unittest
from unittest.mock import patch
from jgtfxhelper import mkfn_cfxdata_filepath

class TestMkfnCfxdataFilepath(unittest.TestCase):
    @patch('jgtfxhelper.mkfn_cdata_filepath')
    def test_mkfn_cfxdata_filepath_use_local(self, mock_mkfn_cdata_filepath):
        mock_mkfn_cdata_filepath.return_value = '/data/jgt/filename'
        result = mkfn_cfxdata_filepath('filename', use_local=True)
        self.assertEqual(result, '/data/jgt/filename')


    @patch('jgtfxhelper.get_data_path')
    def test_mkfn_cfxdata_filepath_not_use_local(self, mock_get_data_path):
        mock_get_data_path.return_value = '/data/path'
        result = mkfn_cfxdata_filepath('filename', use_local=False)
        self.assertEqual(result, '/data/path/filename')

if __name__ == '__main__':
    unittest.main()