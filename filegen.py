import sys
import os
import numpy as np

with open(sys.argv[1], 'wb') as fout:
	#fout.write(os.urandom(int(sys.argv[2])))
	#num = 1024 ** 2
	#col = num
	#row = num
	fout.write(np.random.randint(0x100, size = (int(sys.argv[2]),), dtype=np.int64))
