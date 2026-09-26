# Partition → Nonuniform-cost Unanimous Vote

Category: Complexity open

## Source

The source gives positive binary integer weights. A valid output is a subset whose sum is half the total, or NO-SOLUTION if no such subset exists.

## Target

The target gives independent coins with rational probabilities strictly between zero and one, positive test costs, and a rational bound K. Choose a fixed testing order whose expected cost is at most K, stopping at the first two different outcomes or after all coins.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

Nonuniform costs remove a symmetry exploited in sequential testing and may change the complexity of choosing an order.

## Difficulty

An expensive test alone does not encode subset selection; the expected-cost expression must enforce the partition globally.

## Literature context

Uniform-cost ordering results do not settle the expected-cost problem when each test has its own cost.

Literature checked 2026-09-16. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [An Exact Algorithm for the Unanimous Vote Problem](https://kam.mff.cuni.cz/~spring/media/papers/6/unanimousVote.pdf): Duman Keles, Hellerstein, Marwaha, Musco and Yang, An Exact Algorithm for the Unanimous Vote Problem, SOSA 2026, Theorem 1.1, gives an exact algorithm for unit costs. Section 7, page 167, explicitly asks about extending to nonuniform costs. The full preprint, Section 7, has the same question. This wording leaves an algorithmic extension unresolved; it is not an explicit conjecture of NP-hardness.
- [full preprint](https://arxiv.org/html/2510.16678v1): Duman Keles, Hellerstein, Marwaha, Musco and Yang, An Exact Algorithm for the Unanimous Vote Problem, SOSA 2026, Theorem 1.1, gives an exact algorithm for unit costs. Section 7, page 167, explicitly asks about extending to nonuniform costs. The full preprint, Section 7, has the same question. This wording leaves an algorithmic extension unresolved; it is not an explicit conjecture of NP-hardness.
- [ESA 2018 paper](https://www.sci.brooklyn.cuny.edu/~kletenik/publications/ESA2018.pdf): The earlier ESA 2018 paper, Section 5.4 and Table 1, gives exact adaptive Unanimous Vote algorithms even with arbitrary costs. That does not allow one fixed outcome-independent order. Hardness for general Boolean formulas or weighted linear thresholds does not classify the fixed not-all-equal function here.
- [2025 review](https://arxiv.org/html/2511.15742v1): The same-day follow-up inspected the references in Ünlüyurt's 2025 review, Sections 2 and 4.1, then checked the original results it cites. Gkenosis et al., arXiv:2111.08793v3, Sections 1–2, treats adaptive symmetric-function evaluation and gives approximation guarantees. Ghuge, Gupta and Nagarajan, arXiv:2111.05687v2, Theorem 1.1 and Section 1.1, gives a constant-factor nonadaptive approximation for score classification. Taking unit score weights and classes {0}, {1,...,n-1}, {n} matches the stopping rule here for n>=2, but an approximation does not decide an arbitrary exact threshold. Neither inspected result supplies the proposed hardness reduction or an exact nonuniform-cost algorithm. The 2022 NSF PDF failed to load; its arXiv version was inspected instead. The attempted v4 HTML for the other paper failed; the available PDF identifies itself as v2.
- [arXiv:2111.08793v3](https://arxiv.org/pdf/2111.08793): The same-day follow-up inspected the references in Ünlüyurt's 2025 review, Sections 2 and 4.1, then checked the original results it cites. Gkenosis et al., arXiv:2111.08793v3, Sections 1–2, treats adaptive symmetric-function evaluation and gives approximation guarantees. Ghuge, Gupta and Nagarajan, arXiv:2111.05687v2, Theorem 1.1 and Section 1.1, gives a constant-factor nonadaptive approximation for score classification. Taking unit score weights and classes {0}, {1,...,n-1}, {n} matches the stopping rule here for n>=2, but an approximation does not decide an arbitrary exact threshold. Neither inspected result supplies the proposed hardness reduction or an exact nonuniform-cost algorithm. The 2022 NSF PDF failed to load; its arXiv version was inspected instead. The attempted v4 HTML for the other paper failed; the available PDF identifies itself as v2.
- [arXiv:2111.05687v2](https://arxiv.org/pdf/2111.05687): The same-day follow-up inspected the references in Ünlüyurt's 2025 review, Sections 2 and 4.1, then checked the original results it cites. Gkenosis et al., arXiv:2111.08793v3, Sections 1–2, treats adaptive symmetric-function evaluation and gives approximation guarantees. Ghuge, Gupta and Nagarajan, arXiv:2111.05687v2, Theorem 1.1 and Section 1.1, gives a constant-factor nonadaptive approximation for score classification. Taking unit score weights and classes {0}, {1,...,n-1}, {n} matches the stopping rule here for n>=2, but an approximation does not decide an arbitrary exact threshold. Neither inspected result supplies the proposed hardness reduction or an exact nonuniform-cost algorithm. The 2022 NSF PDF failed to load; its arXiv version was inspected instead. The attempted v4 HTML for the other paper failed; the available PDF identifies itself as v2.

Fixed from board record `website/questions/nonuniform-cost-unanimous-vote.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
