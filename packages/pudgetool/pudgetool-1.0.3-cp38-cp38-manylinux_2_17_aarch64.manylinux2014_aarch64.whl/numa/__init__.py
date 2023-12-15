__name__ = "numa"

import platform
from ctypes import *

libnuma = CDLL("libnuma" + (".dylib" if platform.system() == "Darwin" else ".so"), use_errno=True)

libnuma.numa_available.argtypes = []
libnuma.numa_available.restype = c_int

libnuma.numa_max_node.argtypes = []
libnuma.numa_max_node.restype = c_int

libnuma.numa_node_size64.argtypes = [c_int, POINTER(c_longlong)]
libnuma.numa_node_size64.restype = c_longlong

libnuma.numa_preferred.argtypes = []
libnuma.numa_preferred.restype = c_int

libnuma.numa_node_to_cpus.argtypes = [c_int, POINTER(c_ulong)]
libnuma.numa_node_to_cpus.restype = c_int

libnuma.numa_set_interleave_mask.argtypes = [POINTER(c_int)]
libnuma.numa_set_interleave_mask.restype = c_void_p

libnuma.numa_get_interleave_mask.argtypes = []
libnuma.numa_get_interleave_mask.restype = POINTER(c_int)

libnuma.numa_bitmask_clearall.argtypes = [POINTER(c_int)]
libnuma.numa_bitmask_clearall.restype = POINTER(c_int)

libnuma.copy_bitmask_to_nodemask.argtypes = [POINTER(c_int), POINTER(c_int)]
libnuma.copy_bitmask_to_nodemask.restype = c_void_p

libnuma.copy_nodemask_to_bitmask.argtypes = [POINTER(c_int), POINTER(c_int)]
libnuma.copy_nodemask_to_bitmask.restype = c_void_p

libnuma.numa_bitmask_free.argtypes = [POINTER(c_int)]
libnuma.numa_bitmask_free.restype = c_void_p

libnuma.numa_allocate_nodemask.argtypes = []
libnuma.numa_allocate_nodemask.restype = POINTER(c_int)

libnuma.numa_bind.argtypes = [POINTER(c_int)]
libnuma.numa_bind.restype = c_void_p

libnuma.numa_set_membind.argtypes = [POINTER(c_int)]
libnuma.numa_set_membind.restype = c_void_p

libnuma.numa_get_membind.argtypes = []
libnuma.numa_get_membind.restype = POINTER(c_int)

libnuma.numa_set_preferred.argtypes = [c_int]
libnuma.numa_set_preferred.restype = c_void_p

libnuma.numa_set_localalloc.argtypes = []
libnuma.numa_set_localalloc.restype = c_void_p

libnuma.numa_get_run_node_mask.argtypes = []
libnuma.numa_get_run_node_mask.restype = POINTER(c_int)

libnuma.numa_run_on_node_mask.argtypes = [POINTER(c_int)]
libnuma.numa_run_on_node_mask.restype = c_int

libnuma.numa_distance.argtypes = [c_int, c_int]
libnuma.numa_distance.restype = c_int