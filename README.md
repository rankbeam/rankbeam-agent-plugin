# Rankbeam for Laravel

Inspect a Laravel project's SEO, trace an unexpected canonical or title, and verify the page after a fix. This plugin packages Rankbeam-specific workflows with two local PHP helpers. It can inspect a project before Rankbeam is installed and set up Core when you ask for it.

## What you can ask

- “Inspect this Laravel project for technical SEO problems without changing files.”
- “Set up Rankbeam Core for an existing page and verify its rendered head.”
- “Explain why this page has the wrong canonical URL and fix the source of the problem.”

The plugin inspects the actual application before choosing a workflow. It preserves other SEO packages during a review and distinguishes resolved metadata from served HTML. An empty audit or a page it cannot render is a coverage gap.

## Requirements

Use Codex or another compatible agent with file and shell access to your local Laravel application. PHP 8.2+ is required for the helpers; saved-HTML checks also require `ext-dom`. Your application's own PHP and Laravel requirements still apply. Composer and a working local/test database are needed if you ask to install Core or run its commands.

No Rankbeam account or Pro license is required. The plugin has no hosted endpoint, bundled MCP server, background hooks or telemetry. Installing the plugin does not install Composer dependencies or change an application. Application commands run only as part of an authorized task.

## Install from this repository

In a Codex CLI version with plugin support:

```text
codex plugin marketplace add https://github.com/rankbeam/rankbeam-agent-plugin --ref main
codex plugin add rankbeam-laravel@rankbeam
```

Start a new session in your application. Ask for one of the tasks above, or invoke the `laravel-seo` skill explicitly. In the desktop app, use the plugin directory after adding the repository marketplace; a restart may be needed to refresh local plugins. Repository installation is separate from OpenAI's public directory review.

For a local checkout, use `codex plugin marketplace add /absolute/path/to/rankbeam-agent-plugin` instead. Do not confuse the plugin repository with the application you want to inspect.

## Local helpers

```text
php plugins/rankbeam-laravel/skills/laravel-seo/scripts/inspect-project.php /path/to/laravel-app
php plugins/rankbeam-laravel/skills/laravel-seo/scripts/check-head.php /path/to/saved-response.html
```

The inspector reads Composer metadata and candidate file names without booting Laravel. The HTML helper checks missing/duplicate titles, descriptions and canonicals, canonical URL syntax, robots conflicts, hreflang duplicates and JSON-LD syntax. It never fetches a URL or runs JavaScript. Neither helper reads `.env` or sends results to Rankbeam.

For a known page contract, add `--expected-canonical https://example.com/page` and, only when schema is required, `--require-jsonld`. The helper also reports literal undefined/null metadata attributes caused by frontend bindings. [Quality evidence](review/QA.md) separates helper tests, real rendering and model reasoning evaluations.

## Limits

These are technical checks on the supplied project and HTML. They do not measure rankings, guarantee indexing or AI citations, validate rich-result eligibility or replace a full crawl. Intentional staging `noindex` is preserved. Inertia SSR and Livewire navigation need separate rendering checks; the static HTML helper cannot prove them.

## Development

Python 3.11+ runs the tests and builder; it is not a plugin runtime requirement.

```text
python tools/configure.py
python -m unittest discover -s tests -v
python tools/build.py --output dist
```

`tools/configure.py` generates the portable manifest and a matching Codex compatibility manifest. The builder validates packaged paths and metadata, then writes a reproducible ZIP and SHA-256 inventory. The `tests` and `review` directories are outside the installed plugin. See [review preparation](review/SUBMISSION.md) for the directory handoff and test evidence.

[Documentation](https://docs.rankbeam.dev) · [Support](SUPPORT.md) · [Privacy](PRIVACY.md) · [MIT license](LICENSE)
