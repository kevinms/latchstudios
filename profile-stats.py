import pstats
import sys

p = pstats.Stats(sys.argv[1])

# General Stats
#print "::General Stats::"
#p.print_stats()

# Cumulative Stats
print "::Cumulative::"
p.sort_stats('cumulative').print_stats(10)

# Time consumption:
# sort according to time spent within each function, and then print the statistics for the top ten functions.
print "::Time Consumption::"
p.sort_stats('time').print_stats(10)
#p.sort_stats('time').print_callees(.9, 'init')
#p.sort_stats('time').print_callers(.1, 'init')
