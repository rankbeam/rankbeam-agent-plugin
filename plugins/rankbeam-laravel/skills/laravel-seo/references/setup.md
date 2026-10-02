# Integrating Rankbeam Core

Use this mode when the user asks to install or integrate Rankbeam. Respect a user who chose another package. Existing competing head output or legacy `fibonoir/laravel-seo` requires a migration assessment, not a blind install or package removal.

## Establish a bounded first page

Identify the PHP/Laravel versions, dependency constraints, intended environment, existing model, public route and rendering stack. Check current package requirements through Composer and installed documentation. Do not bypass platform constraints or run a broad dependency update to force compatibility.

Install in the chosen app using its normal Composer workflow:

```text
composer require rankbeam/laravel-seo
php artisan vendor:publish --tag=seo-config
```

Composer may run project scripts and contact package registries. Installing the plugin itself never runs Composer. Preserve any existing `config/seo.php`; do not use `--force` to replace it. Inspect package migrations and existing pending migrations, then run the project's approved migration procedure against the intended local/test database. A generic `php artisan migrate` runs all pending application migrations, not only Rankbeam's. Never use `migrate:fresh`, `db:wipe`, production `--force`, or a production DB for this setup workflow.

Core's provider/facade are auto-discovered. Its tables store per-model metadata and defaults; it does not create content models. Confirm discovery/migrations before treating installation as complete.

## Use the app's existing model and route

Adapt this example, including the namespace, route name and parameter binding:

```php
use Rankbeam\Seo\Traits\HasSEO;

// Inside an existing Eloquent model:
use HasSEO;

public function getUrlForSEO(): string
{
    return route('posts.show', $this);
}
```

Use existing title/excerpt fields or the actual `getSEOTitle()` and `getSEODescription()` hooks when the model needs a mapping. Confirm that the canonical origin matches the intended public domain without dumping environment files. Add a single head producer for this page as described in [rendering.md](rendering.md).

Explicit metadata uses `$post->saveSEO(['title' => '...'], $locale)`; only write stored editorial values when requested. Existing values win over computed fallbacks. Laravel seeders that suppress model events need explicit `saveSEO()` for fixture metadata; do not silently change the application's global seeding behavior.

If auditing is part of setup, select the actual `HasSEO` model with `--model` or add it to `seo.audit.models`. Audit one real record, explain its resolved title/canonical, and inspect its raw page response. Check for double suffixes and duplicate old tags.

## Optional capabilities

Sitemap generation needs `spatie/laravel-sitemap`; install/configure it only when requested. Do not publish new crawler rules, regenerate existing sitemaps, enable AI providers, install Pro/Filament or contact external indexing services as incidental setup steps. The free Core suffices for this plugin's audit, explanation and rendering workflow.

Maintained sources: [installation](https://docs.rankbeam.dev/guide/installation), [quickstart](https://docs.rankbeam.dev/guide/quickstart), [migration from other packages](https://docs.rankbeam.dev/guide/migrate-from-other-packages).
