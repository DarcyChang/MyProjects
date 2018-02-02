from cafe.core.exceptions.exceptions import CafeException

class DriverMethodNotImplementError(CafeException):
    code = '000030001'
    description = 'Cafe.App() Driver Method not implement error'