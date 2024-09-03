class bitarray(object):
    def __init__(self, data):
        if isinstance(data, int):
            # round up
            bytecount = (data-1) // 8 + 1
            self._bytes = bytearray(bytecount)
            self._bitscount = data
        else:
            self.__init__(len(data))

            dataiter = iter(data)
            for byteindex in range(len(self._bytes)):
                byte = 0
                try:
                    if next(dataiter):
                        byte |= 0b0000_0001
                    if next(dataiter):
                        byte |= 0b0000_0010
                    if next(dataiter):
                        byte |= 0b0000_0100
                    if next(dataiter):
                        byte |= 0b0000_1000
                    if next(dataiter):
                        byte |= 0b0001_0000
                    if next(dataiter):
                        byte |= 0b0010_0000
                    if next(dataiter):
                        byte |= 0b0100_0000
                    if next(dataiter):
                        byte |= 0b1000_0000
                except StopIteration:
                    break
                finally:
                    self._bytes[byteindex] = byte

    def __len__(self) -> int:
        return self._bitscount

    def __repr__(self) -> str:
        return f'bitarray(({','.join(['1' if self[i] else '0' for i in range(len(self))])}))'

    def __getindexandmask(self, index):
        if index < 0 or index >= self._bitscount:
            raise IndexError()
        byteindex = index // 8
        bitmask = 1 << (index % 8)
        return (byteindex, bitmask)

    def __getitem__(self, index: int) -> bool:
        byteindex, bitmask = self.__getindexandmask(index)
        return self._bytes[byteindex] & bitmask != 0

    def __setitem__(self, index: int, value: bool) -> None:
        byteindex, bitmask = self.__getindexandmask(index)
        if value:
            self._bytes[byteindex] |= bitmask
        else:
            self._bytes[byteindex] &= ~bitmask

    def toggle(self, index: int) -> None:
        byteindex, bitmask = self.__getindexandmask(index)
        self._bytes[byteindex] ^= bitmask

    def save(self, data: bytearray, start: int = 0) -> None:
        if start + len(self._bytes) > len(data):
            raise IndexError()
        for i in range(len(self._bytes)):
            data[start + i] = self._bytes[i]

    def load(self, data: bytearray, start: int = 0) -> None:
        if start + len(self._bytes) > len(data):
            raise IndexError()
        for i in range(len(self._bytes)):
            self._bytes[i] = data[start + i]