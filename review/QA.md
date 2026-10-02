# Verification record

Executed 2 October 2026 by Codex in the publisher's development environment. These are local automated and operator-executed checks, not independent user testing or OpenAI review.

Version 1.0.1: all 44 helper/package tests pass on WSL/PHP 8.5.4; Windows/PHP 8.2.33 passes 42 with the same two symlink privilege skips. Added regression cases first reproduced accepted malformed URLs and network-share paths reaching filesystem inspection. Both are now rejected; valid encoded URLs still pass. Saved successful Laravel 12/13 responses were checked again with 1.0.1. Native installation/discovery, final installed/archive/source equality and official manifest validation were repeated. The original full application integration baseline below remains version 1.0.0; those 28 checks were not rerun for this helper-only patch.

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

- Native discovery was checked without invoking another model. Automatic selection, negative-prompt restraint and conversational task completion have not been measured in fresh model sessions. EVALUATION.md is a prepared test set, not a pass report.
- The application integrations use Blade and a synthetic SQLite fixture. Inertia SSR, Livewire navigation, existing customer applications and production hosting were not exercised.
- The HTML helper uses PHP's DOM parser, not a browser. It checks selected saved-HTML signals. It does not validate HTTP headers, redirects, canonical destinations, rich-result eligibility or search-engine behavior.
- Application/service-provider side effects depend on the user's code. Only the two bundled helpers are designed to avoid booting the application.
- There are no user acquisition, recommendation, conversion or ranking measurements. The plugin provides no telemetry for those metrics.
- Portal scans, verified publisher identity, directory eligibility, review approval and publication are not covered by local tests.

The release manifest records the exact upload archive and each packaged file's SHA-256. A changed ZIP needs a new receipt and the checks relevant to that change.
