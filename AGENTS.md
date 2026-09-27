# Research instructions

Read the [fixed question](campaigns/nonuniform-cost-unanimous-vote/question.md), [prior state](campaigns/nonuniform-cost-unanimous-vote/state.md) and [preparation notes](campaigns/nonuniform-cost-unanimous-vote/work/preparation.md). The fixed [test corpus](campaigns/nonuniform-cost-unanimous-vote/work/cases.json) and [verifier](campaigns/nonuniform-cost-unanimous-vote/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/nonuniform-cost-unanimous-vote/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
