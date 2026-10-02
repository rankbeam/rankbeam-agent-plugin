# Quality plan — 2 October 2026

Baseline: plugin 1.0.1, commit 8f183b4. Owner requested an autonomous, thorough test-and-improve pass before submission. Success means demonstrated utility and accurate boundaries, not an unsupported claim of market leadership.

1. **Contracts and scope.** Trace each workflow against released Core and current official plugin/framework documentation. Identify omissions that cause incorrect actions or false verification.
2. **Helper reliability.** Test HTML parser behavior, multilingual input, canonical/hreflang edge cases, malformed and bounded inputs, Composer shapes, linked paths, deterministic packaging and runtime compatibility. New fixes need reproducing cases.
3. **Workflow behavior.** Exercise direct, indirect, negative, ambiguous and adversarial requests against isolated fixtures; retain command traces and before/after artifacts where actual model runs are available. Distinguish automated checks, operator execution and fresh-model evaluation.
4. **Actual rendering.** Exercise Blade and real Livewire/Inertia integrations. Check raw initial responses separately from browser navigation, rich/bare transitions, repeat visits, escaped schema and preserved noindex/editorial metadata.
5. **Release proof.** Verify final manifests, archive/source/install equality, a clean public rebuild and relevant tests. Publish the new version with measured coverage, reproducible fixtures and a concise reviewer demonstration.

All application changes are restricted to marked disposable fixtures. Existing product checkouts are read-only unless a concrete plugin-blocking product defect requires a separate scoped change. No new hosting, purchases, production data, customer messages or identity/terms submission. Preserve unrelated work. Use local tests first. The portal's existing developer-verification gate does not block independent quality work.

Exit criteria: every demonstrated defect resolved or explicitly narrowed out of supported scope; no fabricated activation/browser/review claims; public release and submission archive agree; owned test processes stopped; memory updated. Remaining external or unavailable checks must be named precisely.

Execution: all five workstreams completed to the available local boundary. Concrete fixes and measured evidence are in [QA.md](QA.md), [EVALUATION.md](EVALUATION.md) and [rendering-results.json](rendering-results.json). Native shell-policy restrictions and developer identity verification remain external gates; neither is represented as passed.
