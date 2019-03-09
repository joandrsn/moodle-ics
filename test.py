from cal import getModifiedCalendar
import timeit

print(timeit.timeit(getModifiedCalendar, number=1))