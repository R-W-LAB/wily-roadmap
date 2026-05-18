# Result

Implemented Phase 03: Korean stage-based DAG status output.

- `wily-status` now renders Korean user-facing headings, progress text, next-phase text, ready/blocked sections, and missing-state labels.
- Phase status labels are translated for display while roadmap status markers remain English in `.wily/roadmap.yaml`.
- The former flat `All phases:` section is now `Phase 흐름:` grouped by dependency stage.
- Parallel phases with the same dependency rank render under the same stage.
- Multi-dependency phases retain explicit `의존:` annotations, for example `의존: 04-1, 04-2`.
- Replacement details now render in Korean, for example `04R 대체: 04`.
- Status skill documentation now describes the Korean stage-based output contract.

Review follow-up completed and verified. The phase is ready for `$wily-complete 03`.
