# Prepared input and output contract

The source is Partition. Its JSON input is `{"weights": [w0, ...]}` with a
finite list of positive integers. A source output is `{"subset": [indices]}`
with distinct valid indices summing to half the total, or
`{"status": "NO-SOLUTION"}` precisely when no such subset exists. The empty
list has the valid empty subset.

The target input is `{"probabilities": [[numerator, denominator], ...],
"costs": [[numerator, denominator], ...], "bound": [numerator, denominator]}`.
All pairs represent exact rationals with positive denominators. Probabilities
lie strictly between zero and one, costs are positive, and the two lists have
equal length. A target output is `{"order": [indices]}`, a permutation of all
coin indices with expected stopped-test cost at most the bound. The alternative
`{"status": "NO-SOLUTION"}` is valid precisely when no order qualifies. The
empty order has cost zero.

The expected cost of an order is the sum of each coin's cost times the
probability that it is reached: the first coin is always reached; coin at
position `j > 0` is reached exactly when all prior outcomes are heads or all
are tails. Both events are disjoint for `j > 0`.

A candidate `algorithm.py` reads one source JSON object from stdin and writes
one legal target JSON object to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes one valid source
output. Both commands exit nonzero on errors and send diagnostics to stderr.
Recovery cannot rely on memory retained by the forward subprocess. The
candidate must run in deterministic polynomial time, and recovery must work
for every valid target output, including alternate orders and NO-SOLUTION.

`check.py --candidate PATH` injects the fixed source corpus, solves each actual
constructed target independently, and validates every recovered source output.
