from __future__ import print_function

from cafe.core.utils import SingletonClass

class OutputGroup(object):
    def __init__(self):
        self.__group = []

    def __call(self, method, args=(), kwargs={}):
        for i in self.__group:
            getattr(i, method)(*args, **kwargs)

    def new_section(self):
        self.__call('new_section')

    def section_output_started(self):
        self.__call('section_output_started')

    def register(self, stream_object):
        if stream_object not in self.__group:
            self.__group.append(stream_object)

    def unregister(self, stream_object):
        self.__group.remove(stream_object)

    def write(self, str):
        self.__call('write', (str,))

    def flush(self):
        self.__call('flush')

    def writelines(self, sequence):
        self.__call('writelines', (sequence,))


@SingletonClass
class _OutputManager(object):
    def __init__(self):
        self.__streams = {}

    # def __setitem__(self, key, value):
    #     try:
    #         self.__stream[key]
    #     except KeyError:
    #         self.__stream[key] = OutputGroup()
    #     finally:
    #         self.__stream[key].register(value)

    def register(self, key, stream):
        try:
            self.__streams[key]
        except KeyError:
            self.__streams[key] = OutputGroup()
        finally:
            self.__streams[key].register(stream)

    def unregister(self, key, stream):
        try:
            self.__streams[key]
        except KeyError:
            pass
        else:
            self.__streams[key].unregister(stream)

    def __getitem__(self, item):
        return self.__streams[item]

    def __getattr__(self, item):
        try:
            return self.__streams[item]
        except:
            raise Exception("Could not find '%s' in output_manager" % item)

output_manager = _OutputManager()

if __name__ == "__main__":
    import outputstream
    import sys

    class FunTransform(outputstream.OutputStream):
        def write(self, str):
            self.get_stream().write(">>> %s" % str)

    class FunTransform2(outputstream.OutputStream):
        def write(self, str):
            self.get_stream().write("!!! %s" % str)

    output_manager.register("stdout", FunTransform(sys.stdout))
    output_manager.register("stdout", FunTransform2(sys.stdout))

    print("Hello World!!!", file=output_manager['stdout'])


