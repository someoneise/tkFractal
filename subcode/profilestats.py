import pstats
from pstats import SortKey

p = pstats.Stats('subcode\\output.pstats')
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(20)
