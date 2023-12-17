import os as _os
import tempfile as _tmp

import fileunity as _fu
import openpyxl as _xl


class WorkbookUnit(_fu.BaseUnit):
    @classmethod
    def data_duplicating(cls, data):
        with _tmp.TemporaryDirectory() as directory:
            file = _os.path.join(directory, "a.xlsx")
            cls.data_saving(file, data)
            ans = cls.data_loading(file)
        return ans
    @classmethod
    def data_loading(cls, file):
        return _xl.load_workbook(file)
    @classmethod
    def data_saving(cls, file, data):
        data.save(filename=file)
    @classmethod
    def data_default(cls):
        return _xl.Workbook()
