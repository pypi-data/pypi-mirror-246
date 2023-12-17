from contextlib import suppress as _suppress
from itertools import (
    count,
    cycle,
    repeat,
    accumulate,
    chain,
    compress,
    dropwhile,
    filterfalse,
    groupby,
    islice,
    starmap,
    takewhile,
    tee,
    zip_longest,
    product,
    permutations,
    combinations,
    combinations_with_replacement,
    pairwise,
    batched,
)

from .applier import smart_partial

count @= smart_partial
cycle @= smart_partial
repeat @= smart_partial
accumulate @= smart_partial
chain @= smart_partial
compress @= smart_partial
dropwhile @= smart_partial
filterfalse @= smart_partial
groupby @= smart_partial
islice @= smart_partial
starmap @= smart_partial
takewhile @= smart_partial
tee @= smart_partial
zip_longest @= smart_partial
product @= smart_partial
permutations @= smart_partial
combinations @= smart_partial
combinations_with_replacement @= smart_partial
pairwise @= smart_partial
batched @= smart_partial
