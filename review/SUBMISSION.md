# Submission handoff: Rankbeam for Laravel 1.1.0

Prepared 2 October 2026. The package is ready for an initial upload and portal validation. It has not been submitted to or approved by OpenAI. Developer identity verification, account eligibility, automated portal findings and policy attestations remain pending.

## Package and purpose

Download `rankbeam-laravel-1.1.0.zip` and its SHA-256 inventory from the [1.1.0 release](https://github.com/rankbeam/rankbeam-agent-plugin/releases/tag/v1.1.0). Upload the plugin ZIP, not GitHub's source-code ZIP. It contains one top-level plugin directory, portable and Codex compatibility manifests, one skill, three workflow references, three PHP helper files, the existing Rankbeam icon, an MIT license and a data-handling notice.

The plugin helps users inspect a local Laravel application, diagnose metadata resolution, set up Rankbeam Core when requested, and verify a scoped repair against served HTML. Initial inspection works without Core. There is no Rankbeam account, paid dependency, MCP server, background hook, telemetry or hosted service. PHP 8.2+ and `ext-dom` are needed for the helpers; the host must provide local file/shell access. Application commands require an appropriate local/test environment.

Publisher: Valentin Goxhaj, Rankbeam. Contact: hello@rankbeam.dev. The verified developer identity selected in the portal must match the actual publisher; it has not been checked during this preparation.

- [Source and installation](https://github.com/rankbeam/rankbeam-agent-plugin)
- [Privacy and data handling](https://github.com/rankbeam/rankbeam-agent-plugin/blob/main/PRIVACY.md)
- [Support](https://github.com/rankbeam/rankbeam-agent-plugin/blob/main/SUPPORT.md)
- [MIT license](https://github.com/rankbeam/rankbeam-agent-plugin/blob/main/LICENSE)
- [Recorded QA](QA.md)
- [Agent evaluation evidence and prompts](EVALUATION.md)

## Reviewer setup

No credentials or private data are needed. Clone the source repository and use a disposable application. Python 3.11+, PHP, Composer and network access to package hosts are needed to reproduce the fixture setup. Laravel 13 requires an appropriate PHP version; our integration runs used PHP 8.4.25.

From the repository root:

```text
python -m unittest discover -s tests -v
python tools/prepare_fixture.py --laravel 12 --app work/laravel12
python tests/integration.py --app work/laravel12 --output work/results12
python tools/prepare_fixture.py --laravel 13 --app work/laravel13
python tests/integration.py --app work/laravel13 --output work/results13
python tools/build.py --output dist
```

The preparation command requires a new destination. It downloads a fresh Laravel skeleton, installs released Core 3.21.1 with Composer scripts/plugins disabled, and marks the fixture. Framework patch versions resolve at reproduction time; exact versions used for our evidence are in QA.md. Preserve generated Composer locks if you need to repeat an identical dependency resolution.

The integration harness refuses an unmarked/configured application or an existing fixture database. It writes synthetic models, routes and records, runs migrations against its own SQLite file, serves an ephemeral loopback HTTP route and stops its own server. It leaves the fixture and evidence for inspection. Use a new destination for another run. Do not run it against an existing application or use Python's `-O` flag.

For an interactive review, use the repository installation commands in README.md, start a new Codex session with the disposable application selected, and try EVALUATION.md. The automatic integration harness exercises helper/package behavior; it does not replace model-level prompt evaluation.

For a quick credential-free demonstration, run `python tools/demo.py`. It checks an intentionally duplicated title/relative canonical, then the minimal corrected HTML. The second result passes while retaining the informational staging noindex. This demonstration is deterministic helper execution, not a recording of agent activation.

The rendering lab can be reproduced from a checkout of [rankbeam-examples](https://github.com/rankbeam/rankbeam-examples): run `python tools/prepare_rendering.py --examples /path/to/rankbeam-examples --output work/rendering`, then `python tools/serve_rendering.py --lab work/rendering --stack inertia-vue --ssr` in an interactive terminal. Run `python tools/capture_rendering.py --lab work/rendering --stack inertia-vue` separately. The five stack names and ports are recorded in `lab.json`. Type `stop` to terminate the lab server; run only one SSR stack at a time. The preparation downloads dependencies and builds frontend assets; it uses a new marked fixture with synthetic data. Browser navigation checks are separate from raw capture.

## Portal steps

1. Open [Plugins](https://platform.openai.com/plugins) in the intended organization/project. Confirm publishing permissions and complete developer identity verification if required.
2. Upload the release ZIP and review the imported metadata and skills. Resolve required scan findings and rebuild/re-upload if necessary.
3. Confirm that the publisher and public URLs are accurate. This package has no MCP connection or reviewer login to configure.
4. Submit the validated draft after completing the portal's attestations. Review acceptance and publication are separate steps.

Current [submission documentation](https://developers.openai.com/plugins/deploy/submission) describes credentials, five positive/three negative cases and a video for MCP integrations. This skills-only package includes review scenarios, seven executed source-supplied reasoning cases and a reproducible CLI demonstration. Native end-to-end activation remains unverified because of the recorded host-policy block. Any additional portal requirement still applies. The [plugin guidelines](https://developers.openai.com/plugins/plugin-guidelines) allow additional eligibility requirements for skills-only publication; local validation does not establish eligibility or approval.

The initial scope is intentionally skills-only. Current submission documentation says an MCP server cannot be added to an existing skills-only plugin. A future Pro MCP integration therefore needs a separate distribution decision.

## Release notes

Version 1.1.0 adds optional exact canonical and required JSON-LD checks, catches undefined/null structural head attributes, and corrects Vue/React optional bindings. Five-stack raw rendering, selected browser navigation assertions and source-supplied model reasoning checks are documented with their limits. Version 1.0.1 hardened local paths and URL syntax. No version claims ranking, indexing, citation or discovery-volume outcomes.
