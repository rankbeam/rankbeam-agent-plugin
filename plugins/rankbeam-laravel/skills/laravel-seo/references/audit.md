# Auditing and explaining Laravel SEO

## Without Rankbeam

Use source inspection and the saved-HTML checker. Inspect the route/controller, model data and the layout/component responsible for the head. Identify an existing SEO package before suggesting integration changes. A missing Rankbeam dependency is not an SEO defect. Do not remove or replace an existing package as part of an audit.

Start with the user's affected page. Check for duplicate head producers, missing values, relative canonicals, unexpected public origins, conflicting robots directives and invalid JSON-LD. Distinguish an observed defect from a likely issue in source. A cross-domain canonical, a query in an explicitly chosen canonical, omitted robots tag or absent article schema can be intentional.

## With Rankbeam Core

Check the installed package's version and command help before relying on options. These commands are verified against Core 3.21.1; use installed source/help and current documentation for other versions.

```text
php artisan help seo:audit
php artisan seo:audit --model="App\Models\Post" --limit=20 --json
php artisan seo:explain "App\Models\Post" 42 --json
```

Substitute an actual `HasSEO` model and record key. Do not audit every customer record by default. `--limit` applies per model. Add `--locale` when the issue is locale-specific and `--route=posts.show` to `seo:explain` when a real route-default layer is relevant.

The audit returns `pages`, `summary`, `skipped` and `coverage`. Inspect all four, plus `indexing_guard` when present. Zero pages means no coverage. Skipped models or read errors require explanation. An ordinary audit can exit zero with findings; use the JSON statuses or `--strict` when a failure exit code is desired. A strict run may fail on advisory findings too. An active indexing guard is reported separately and can coexist with a passing audit: intentional local `noindex` is not itself a defect.

Core checks resolved metadata in process. It does not fetch served HTML, check live canonical targets, measure browser navigation, validate rich-result eligibility or produce a 0–100 score. Run the saved-HTML check separately where rendering matters.

## Correct the layer that caused the problem

Resolution proceeds from configuration through database defaults (global, model type, route), computed model values, and explicit stored metadata. Post-processing then handles suffixes, derived URLs and the indexing guard. `seo:explain` reports the winning layer, losing layers, final values, notes and the site-level ledger.

- Fix a wrong fallback in configuration or model code when that is the actual source.
- An explicit saved title can override a model fix; show the trace before proposing a stored-value change.
- Derived canonicals strip queries; explicit canonicals are preserved. Do not normalize away a deliberate explicit URL without checking intent.
- A staging/local indexing guard can intentionally force `noindex,nofollow`. Keep it enabled. Verify the guard's environment policy; do not remove protection to silence findings.
- Title/description length advice depends on language and graphemes. Do not impose one English character budget on every language.

After a change, repeat the same bounded target/locale checks. Describe remaining advisory issues rather than hiding them or fabricating content.

Maintained sources: [audit](https://docs.rankbeam.dev/guide/audit), [resolution trace](https://docs.rankbeam.dev/guide/explain), [precedence](https://docs.rankbeam.dev/concepts/resolver-precedence), [indexing guard](https://docs.rankbeam.dev/guide/indexing-guard).
