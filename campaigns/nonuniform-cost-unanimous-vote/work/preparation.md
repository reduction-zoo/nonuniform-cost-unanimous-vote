# Preparation evidence

Prepared on 2026-09-26 before any construction attempt. The fixed corpus has
120 distinct positive-integer Partition instances: 20 hand-labelled edge cases
and 100 seeded random cases. It includes 66 YES and 54 NO instances, with one
to eight weights. The generator and seeds are in `generate_cases.py`; exact
source outputs are in `cases.json`.

The source oracle enumerates all subsets over this finite domain. A separate
subset-sum dynamic program agreed on the decision for all 120 cases. The 20
edge-case statuses were labelled by hand before implementation and checked
against the oracle. Returned subsets are validated by summing the original
weights; NO-SOLUTION is accepted only after the conclusive enumeration.

The target oracle enumerates all fixed orders using exact rational arithmetic
from Python 3.12.14's `fractions.Fraction`. This is a direct textbook algorithm
over small finite test targets; no solver encoding is needed for a permutation
and an exact rational expectation. A second computation enumerates all coin
outcome vectors and simulates the stopping rule. It agreed with the formula for
every order in nine target configurations of zero to four coins. Thresholds at
the minimum expected cost and one-sixth below it yield 18 exact decision
checks. Hand fixtures reject an over-bound order, a repeated index, invalid
probabilities and wrong positive/negative decisions.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/nonuniform-cost-unanimous-vote/work/check.py --self-test
```

The self-test begins with `research/validate_preparation.py`, regenerates all
random sources by seed, recomputes and directly validates stored outputs, and
runs the independent oracle comparisons. `check.py --candidate PATH` runs
forward and recovery in separate processes on each case and examines up to
three distinct qualifying target orders. An injected incorrect candidate was
rejected after its target was solved and recovery failed validation. No actual
reduction candidate exists, so successful end-to-end candidate verification is
untested. The exhaustive target oracle is practical only for small coin counts;
the finite checks do not establish a reduction or settle the open question.
