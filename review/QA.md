# Verification record

Executed 2 October 2026 by Codex in the publisher's development environment. These are local automated and operator-executed checks, not independent user testing or OpenAI review.

## Version 1.1.0

- **55 helper/package tests:** all pass on WSL/PHP 8.5.4. Windows/PHP 8.2.33 and 8.4.25 each pass 53 with two symlink privilege skips; Linux executes both cases. Added exact canonical expectations, required-schema absence, argument failures, Unicode, inert comments, hostile page text and undefined/null attribute regressions.
- **Five real rendering stacks:** Blade, Livewire and Inertia Vue/React/Svelte, each with rich, bare and noindex raw HTTP responses. Laravel 12.69.3/Core 3.21.1/PHP 8.4.25; exact frontend versions and response receipts are in [rendering-results.json](rendering-results.json). Bare pages intentionally lack descriptions: that finding is retained, not suppressed in the helper.
- **240 browser assertions:** 64 per Inertia stack over six page states, plus 48 Livewire transition assertions. Tests cover title/canonical, description/robots presence, alternates, schema teardown, repeated visits, unrelated-tag preservation, stale article metadata, duplicate social singletons and escaped JSON. Inertia also checks literal undefined/null attributes; its final runs have no captured console warnings/errors. These are selected assertions, not the complete examples conformance suite.
- **Useful failures reproduced and fixed:** Vue and React's explicit optional props produced literal undefined head attributes. Corrected renderer-object/conditional bindings pass the same tests. The plugin now teaches those patterns and its HTML helper detects the artifacts. Svelte needed no recipe correction.
- **Negative rendering control:** disabling Vue SSR removes title/description/canonical from all three raw responses; the checker detects them. This does not establish crawler behavior or every CSR stack.
- **Seven fresh GPT-6 Astra reasoning evaluations:** supplied skill/source only; manually reviewed findings, scoped proposed diff, noindex preservation, WordPress/unrelated restraint, ambiguity and hostile HTML-comment handling. Original fixture hashes remain unchanged; no synthetic credential sentinel appears in output. The proposed fix was independently applied to a separate synthetic file and passed exact-canonical checking while retaining noindex. See [EVALUATION.md](EVALUATION.md).
- **Package validation:** official manifest schema and skill validator pass; native Codex installs version 1.1.0 and discovers the enabled skill. All 13 installed files match both source and ZIP. The deterministic build inventory is [package-manifest.json](package-manifest.json).

The native installed-plugin execution attempt was **blocked by the host's shell policy**, and an initial plugin configuration warning also invalidated that run. It is not a behavioral pass. No sandbox bypass was used. Supplied-source reasoning is not proof of implicit activation or successful tool use.

The Laravel 12/13 full application integration baseline below remains version 1.0.0. The new rendering fixtures and expanded helper suite are current; do not count the old 28 workflow checks as rerun for 1.1.0.

### Final release and upstream follow-through

The public v1.1.0 checkout rebuilds the exact 31,531-byte ZIP, SHA-256 `c7d295cd7cc81c16f687f424e23597bdd965ca36342d3a52d4021cc36ff0f4fa`; downloading the published release reproduces that hash. Saved Laravel 12/13 successful HTML also passes the final helper with an explicit canonical expectation.

[Examples PR 3](https://github.com/rankbeam/rankbeam-examples/pull/3) ships the Vue/React correction and shared attribute regression assertion. [PR 4](https://github.com/rankbeam/rankbeam-examples/pull/4) enables previously skipped CSR controls for all three Inertia stacks and corrects the control's JSON-LD expectation: root-view schema remains even when client metadata is absent. The final [public browser matrix](https://github.com/rankbeam/rankbeam-examples/actions/runs/37070171270) passes **35 tests, no skips**: Blade 6, Livewire 5, each Inertia stack 8. The independent fixture oracle also passes locally. This suite is additional upstream evidence, separate from the 240 local selected assertions and the released-Core fixture matrix.

[Core docs PR 128](https://github.com/rankbeam/laravel-seo/pull/128) applies the same code correction to all 15 guide editions. Local docs build and localization checks pass (602 localized pages, 3,948 identical code blocks, 645 sitemap URLs); the production deployment check succeeds. The direct automated HTTP content verification received a 403, so it is not claimed as a successful live-content read. All owned local rendering servers were stopped.

## Version 1.0.1 baseline

All 44 helper/package tests passed on Linux; Windows/PHP 8.2 passed 42 with the same two skips. Network-share inputs and malformed canonical/hreflang URL regressions were fixed. Saved Laravel 12/13 HTML, native installation/discovery, archive/source/install equality and official manifest validation were repeated.

## Version 1.0.0 baseline

| Check | Environment | Observed result |
| --- | --- | --- |
| Helpers and packaging | Windows, PHP 8.2.33 | 41 tests: 39 passed, 2 symlink cases skipped because Windows required extra privileges |
| Helpers and packaging | Windows, PHP 8.4.25 | 41 tests: 39 passed, the same 2 cases skipped |
| Helpers and packaging | WSL Linux, PHP 8.5.4 | All 41 tests passed, including both symlink cases |
| Real application workflow | Laravel 12.69.3, Core 3.21.1, PHP 8.4.25, SQLite | 14/14 checks passed |
| Real application workflow | Laravel 13.34.0, Core 3.21.1, PHP 8.4.25, SQLite | 14/14 checks passed |
| Portable manifest | Published agent-plugins.org 1.0.0 JSON schema | Valid |
| Skill structure | OpenAI skill-creator quick validator | Valid |
| Native installation | Codex CLI 0.153.4, local repository marketplace | Installed and enabled; app-server `skills/list` discovers `rankbeam-laravel:laravel-seo` |
| Archive | Allowlisted builder | Reproducible ZIP; extraction matches source; installed package matches source |

The application checks cover empty-audit coverage, one synthetic record, bounded audit, explicit title precedence, real HTTP 200/text-html, duplicate-title detection, repaired raw HTML, intended public canonical, preserved editorial title, staging noindex, guard-vs-defect distinction, strict failure on an actual defect, skipped-model coverage and server cleanup. Sanitized receipts are in [laravel12-result.json](laravel12-result.json) and [laravel13-result.json](laravel13-result.json).

The helper suite covers valid/missing/duplicate tags, canonical syntax, robots conflicts and intentional noindex, JSON-LD syntax/shape, hreflang, malformed/oversized inputs, remote/wrapper rejection, inventory limits, symlinks, omission of secrets/script bodies from output, no script execution and unchanged input hashes. Packaging tests check both manifests, local references, deterministic archives and rejection of unexpected files.

Two harness assumptions were corrected while developing the integration test: an active indexing guard is separate from metadata defects and can accompany a passing strict audit; Composer metadata must be read as UTF-8 on Windows. Neither was a package regression.

## Limits of this evidence

- Automatic selection and end-to-end native tool execution remain unverified. Seven source-supplied fresh model sessions test reasoning and restraint only; native discovery is a separate metadata check.
- All application evidence uses synthetic local SQLite fixtures. Existing customer applications, production hosting and framework versions outside the recorded matrix were not exercised.
- The HTML helper uses PHP's DOM parser, not a browser. It checks selected saved-HTML signals. It does not validate HTTP headers, redirects, canonical destinations, rich-result eligibility or search-engine behavior.
- Application/service-provider side effects depend on the user's code. Only the two bundled helpers are designed to avoid booting the application.
- There are no user acquisition, recommendation, conversion or ranking measurements. The plugin provides no telemetry for those metrics.
- Portal scans, verified publisher identity, directory eligibility, review approval and publication are not covered by local tests.

The release manifest records the exact upload archive and each packaged file's SHA-256. A changed ZIP needs a new receipt and the checks relevant to that change.
