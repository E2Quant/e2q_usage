import mmap
import os
import sys

import pandas as pd

from log_proto import *


class LogBin(object):
    """
    log bin file

    """

    def __init__(self, file=""):
        """Constructor for $"""
        self._file = file

    def read_log(self, start=0, offset=10):
        if len(self._file) == 0:
            logger.error("file error:", self._file)
            return
        fsize = os.path.getsize(self._file)
        if fsize == 0:
            logger.info("file is empty")
            return
        data_list = []
        with open(self._file, "rt") as f:
            mapped = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
            ba = bytearray(mapped)

            ba_len = len(ba)
            while ba_len > 0:
                pl = ParserLog()
                pl.getData(ba)
                data, idx = pl.toClass()
                data_list.append(data)
                # c\c++ '\0'
                idx += 1
                ba = ba[idx:]

                ba_len = len(ba)

        data_df = pd.DataFrame(data_list)

        data_df.ticket_now = pd.to_datetime(data_df.ticket_now, unit='ms', utc=True)
        data_df.ticket_now = data_df.ticket_now.map(lambda x: x.tz_convert('Asia/Shanghai'))

        logger.info("row: %d" % (len(data_df.index)))

        if start > 0:
            data_df = data_df[start:]
        if offset > 0:
            data_df = data_df.head(offset)

        if offset < 0:
            data_df = data_df.tail(abs(offset))

        print(data_df)


def run(f, start=0, offset=10):
    log_bin = LogBin(f)
    log_bin.read_log(start, offset)


if __name__ == '__main__':
    argvs = sys.argv[1:]
    arg_len = len(argvs)
    if arg_len == 0:
        print("help\n python log_bin.py  ./log/3827611_0_.log")
        exit(0)

    start = 0
    offset = 0
    file = ""
    if arg_len > 0:
        file = argvs[0]

    if arg_len > 1:
        start = int(argvs[1])

    if arg_len > 2:
        offset = int(argvs[2])

    if start < 0:
        offset = start
    run(file, start, offset)
