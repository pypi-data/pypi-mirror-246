import os as _os

import Bio.SeqIO as _SeqIO
import fileunity as _fu
import seqreads as _sr


class _SeqReadUnit(_fu.BaseUnit):
    @classmethod
    def data_duplicating(data):
        return _sr.SeqRead(**vars(data))
    @classmethod
    def data_loading(cls, file):
        rec = _SeqIO.read(file, cls._format)
        return _sr.SeqRead.by_seqRecord(rec)
    @classmethod
    def data_saving(cls, file, data):
        rec = data.to_record()
        _SeqIO.write(rec, file, cls._format)
    @classmethod
    def get_format(cls):
        return cls._format


class SeqReadPHDUnit(_SeqReadUnit):
    _format = "phd"
class SeqReadABIUnit(_SeqReadUnit):
    _format = "abi"


def load(file, format=None):
    if format is None:
        ext = _os.path.splitext(file)[-1]
        format = _format_by_ext(ext)
    cls = _cls_by_format(format)
    ans = cls.load(file)
    return ans

def _format_by_ext(x, /):
    ans = {
        ".ab1":"abi",
        ".phd":"phd",
    }[x]
    return ans

def _cls_by_format(x, /):
    ans = {
        "abi":SeqReadABIUnit,
        "phd":SeqReadPHDUnit,
    }[x]
    return ans
