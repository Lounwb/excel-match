class FileError(Exception):
    
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg
    
class ConcatError(FileError):

    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg

class ColumnKeyError(FileError):
    
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg

class FileTypeError(FileError):

    def __init__(self, msg, file_path):
        self.msg = msg
        self.file_path = file_path
    
    def __str__(self):
        return self.msg


