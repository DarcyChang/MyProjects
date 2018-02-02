import weakref


class BreakPoint(object):
    _BreakPointPool = weakref.WeakValueDictionary()

    def __new__(cls, line, file_path):
        primary_key = '{}{}'.format(line, file_path)
        obj = BreakPoint._BreakPointPool.get(primary_key)
        if not obj:
            obj = object.__new__(cls)
            BreakPoint._BreakPointPool[primary_key] = obj
            obj.line, obj.location = line, file_path
        return obj

    def __repr__(self):
        return repr((self.location, self.line))


class BreakPointRecoder(object):
    def __init__(self):
        self.bps = []

    def add_breakpoint(self, line, file_path):
        bp = BreakPoint(line, file_path)
        if bp not in self.bps:
            self.bps.append(bp)

    def del_breakpoint(self, line, file_path):
        bp = BreakPoint(line, file_path)
        for bp_tmp in self.bps:
            if bp == bp_tmp:
                self.bps.remove(bp_tmp)

    def get_breakpoints(self):
        return sorted(self.bps, key=lambda bp: bp.line)

    @property
    def breakpoint_count(self):
        return len(self.bps)


if __name__ == '__main__':
    bpr = BreakPointRecoder()
    bpr.add_breakpoint(4, 'a')
    bpr.add_breakpoint(1, 'b')
    bpr.add_breakpoint(2, 'a')
    for bp in bpr.get_breakpoints():
        print bp
    print '--------------'
    bpr.del_breakpoint(1, 'b')
    for bp in bpr.get_breakpoints():
        print bp
