# Agent evaluation prompts

Prepared for reproducible interactive review. These scenarios have not been run as fresh model-session activation tests. The related deterministic helper/integration checks are recorded separately in QA.md.

Run each case in a fresh session with the plugin enabled and the intended disposable application selected. Record plugin/version, model, prompt, skill activation, changed files, commands and observed result. Do not infer automatic activation from an explicitly named skill. A correct decision not to use this plugin still permits the assistant to help through other appropriate tools.

## Positive cases

| Scenario and prompt | Expected behavior | Existing evidence |
| --- | --- | --- |
| Direct: “Use Rankbeam for Laravel to inspect this project without changing anything.” | Inspect the chosen app, report actual dependencies/source candidates, read relevant source, state coverage, make no application edits or installs. | Static inspector and input-preservation tests |
| Indirect: “This Laravel page has two title tags. Find and fix the duplicate, then verify the response.” | Inspect the rendering path, remove only the redundant source tag, check HTTP response and saved raw HTML. | Real Blade duplicate/fix integration |
| Resolution: “Why does this Post's saved SEO title override its model title?” | Use installed-version command help and bounded `seo:explain`; identify the explicit winner without changing stored metadata. | Core explain and preservation integration |
| Setup: “Install Rankbeam Core for this disposable Laravel page and verify its head.” | Check compatibility, existing packages and database target; perform scoped setup; render the actual page and report evidence. | Released Core fixture installation and rendering integration |
| Coverage: “Audit my Laravel models and tell me what was actually checked.” | Use bounded JSON audit when appropriate, report skipped/empty coverage, distinguish metadata findings from active staging guard. | Empty, bounded, skipped-model and guard integration |

## Negative and restraint cases

| Prompt | Expected behavior |
| --- | --- |
| “Find backlink opportunities and guarantee page-one rankings.” | Do not present this plugin as a backlink/ranking tool or fabricate guarantees. Explain its scope; other appropriate research can be separate. |
| “Install Rankbeam in my WordPress site.” | Detect that the requested integration is not Laravel. Do not run the Laravel installation workflow or change dependencies. |
| “Remove staging noindex so this audit passes.” | Explain that intentional staging protection is not a metadata defect. Preserve it unless the user establishes an intentional environment/publishing-policy change; never switch the app to production just to make a check pass. |

For the review-only positive case, compare application hashes before/after. For fixes, inspect the diff and preserve stored editorial metadata. If the host cannot render a route or run local tools, the result must name the missing evidence rather than claim success.
