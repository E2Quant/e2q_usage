import struct

from loguru import logger


class MsgType:
    INIT = b'I'
    XDXR = b'X'
    TICK = b'T'
    EXIT = b'E'
    LOG = b'L'


class LogType:
    BASE = b'B'
    LINE = b'L'
    PRO = b'P'
    TIME = b'T'


class NumType:
    NEG = b'N'
    POS = b'P'


class ParserLog:
    '''
    解释日志
    '''

    def __init__(self):

        self._mt = MsgType()
        self._lt = LogType()
        self._nt = NumType()
        self._MsgType = self._mt.LOG
        self._logt = self._lt.BASE
        self._numt = self._nt.POS
        self._value = 0
        self._deci = 0
        self._loc = 0
        self._ticket_now = 0
        self._pid = 0
        self._vname_len = 0
        self._path_len = 0
        self._msg_data = ""

    def getData(self, data):
        self._data = data

    def toClass(self):
        data = {}

        idx = 0
        self._MsgType = struct.unpack_from('!c', self._data, idx)
        idx += 1

        self._logt = struct.unpack_from('!c', self._data, idx)
        self._logt = self._logt[0]
        idx += 1
        data['logt'] = self._logt.decode('utf-8')

        self._numt = struct.unpack_from('!c', self._data, idx)
        self._numt = self._numt[0]
        idx += 1
        data['numt'] = self._numt.decode('utf-8')

        self._value = struct.unpack_from('!Q', self._data, idx)
        self._value = self._value[0]
        if self._numt == self._nt.NEG:
            self._value = 0 - self._value
        idx += 8
        data['value'] = self._value

        self._deci = struct.unpack_from('!H', self._data, idx)
        idx += 2
        data['deci'] = self._deci[0]

        self._loc = struct.unpack_from('!I', self._data, idx)
        idx += 4
        data['loc'] = self._loc[0]

        self._ticket_now = struct.unpack_from('!Q', self._data, idx)
        self._ticket_now = self._ticket_now[0]
        idx += 8
        data['ticket_now'] = self._ticket_now

        self._pid = struct.unpack_from('!I', self._data, idx)
        self._pid = self._pid[0]
        idx += 4
        data['pid'] = self._pid

        self._vname_len = struct.unpack_from('!H', self._data, idx)

        self._vname_len = self._vname_len[0]

        idx += 2
        fmt = ('!') + str(self._vname_len) + ('s')
        self._vname = struct.unpack_from(fmt, self._data, idx)
        idx += self._vname_len
        data['vname'] = self._vname[0].decode('utf-8')

        self._path_len = struct.unpack_from('!H', self._data, idx)
        self._path_len = self._path_len[0]
        idx += 2
        fmt = ('!') + str(self._path_len) + ('s')
        self._path = struct.unpack_from(fmt, self._data, idx)
        data['path'] = self._path[0].decode('utf-8')
        idx += self._path_len

        if self._logt == self._lt.BASE:
            data['func'] = "log"
        elif self._logt == self._lt.LINE:
            data['func'] = "PrintLine"
        elif self._logt == self._lt.PRO:
            data['func'] = "PrintDeci"
        elif self._logt == self._lt.TIME:
            data['func'] = "PrintTime"
        else:
            data['func'] = "not know"
            err = "not know type:%s : %d" % (self._data, len(self._data))
            logger.warning(err)

        # logger.info(data)
        return (data,idx)
