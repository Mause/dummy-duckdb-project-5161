import fsspec
from fsspec.implementations.memory import MemoryFileSystem
import io

class ModifiedMemoryFileSystem(MemoryFileSystem):
	protocol = ('DUCKDB_INTERNAL_OBJECTSTORE',)
	# defer to the original implementation that doesn't hardcode the protocol
	_strip_protocol = classmethod(AbstractFileSystem._strip_protocol.__func__)
    

print(ModifiedMemoryFileSystem().unstrip_protocol('hello.csv'))
