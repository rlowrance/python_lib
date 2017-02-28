import cPickle as pickle
import os.path
import pdb


def unpickle_file(path=None, process_unpickled_object=None, on_EOFError=None, on_ValueError=None, on_FileNotExists=None):
    'unpicckle each object in the file at the path'
    if not os.path.exists(path):
        if on_FileNotExists is None:
            return  # simulate end of file
        else:
            on_FileNotExists('file does not exist: %s' % path)
            return
    with open(path, 'r') as f:
        unpickler = pickle.Unpickler(f)
        try:
            while True:
                obj = unpickler.load()
                process_unpickled_object(obj)
        except EOFError as e:
            if on_EOFError is None:
                raise e
            else:
                on_EOFError(e)
                return
        except ValueError as e:
            if on_ValueError is None:
                raise e
            else:
                on_ValueError(e)
                return
