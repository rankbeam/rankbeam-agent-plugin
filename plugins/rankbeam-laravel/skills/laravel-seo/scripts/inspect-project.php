<?php

declare(strict_types=1);

require __DIR__.'/lib.php';

if ($argc !== 2 || in_array($argv[1], ['--help', '-h'], true)) {
    rb_output(['usage' => 'php inspect-project.php <application-directory>', 'requires' => 'PHP 8.2+', 'effects' => 'Read-only bounded metadata and file-name inspection; no app boot, network or database.'], $argc === 2 ? 0 : 2);
}
rb_local_path($argv[1]);
$root = realpath($argv[1]);
if ($root === false || !is_dir($root)) {
    rb_error('missing_directory', 'The application directory does not exist.');
}
$composer = rb_json($root.'/composer.json', 1048576);
$allowed = ['php', 'laravel/framework', 'illuminate/foundation', 'rankbeam/laravel-seo', 'rankbeam/laravel-seo-pro', 'rankbeam/laravel-seo-filament', 'fibonoir/laravel-seo', 'inertiajs/inertia-laravel', 'livewire/livewire', 'filament/filament', 'artesaos/seotools', 'ralphjsmit/laravel-seo', 'spatie/laravel-sitemap'];
$declared = [];
foreach (['require', 'require-dev'] as $section) {
    if (isset($composer[$section]) && !is_array($composer[$section])) {
        rb_error('invalid_json_shape', 'Composer require sections must be objects.');
    }
    foreach ($allowed as $name) {
        if (isset($composer[$section][$name]) && is_string($composer[$section][$name])) {
            $declared[$name] = ['constraint' => substr($composer[$section][$name], 0, 120), 'section' => $section];
        }
    }
}
$locked = [];
if (file_exists($root.'/composer.lock') || is_link($root.'/composer.lock')) {
    $lock = rb_json($root.'/composer.lock', 8388608);
    foreach (['packages', 'packages-dev'] as $section) {
        if (isset($lock[$section]) && !is_array($lock[$section])) {
            rb_error('invalid_json_shape', 'Composer lock package sections must be arrays.');
        }
        foreach ($lock[$section] ?? [] as $package) {
            if (is_array($package) && is_string($package['name'] ?? null) && in_array($package['name'], $allowed, true)) {
                $locked[$package['name']] = is_string($package['version'] ?? null) ? substr($package['version'], 0, 120) : 'unknown';
            }
        }
    }
}
$warnings = [];
$candidates = [];
$visited = 0;
$truncated = false;
$walk = function (string $relative, int $depth = 0) use (&$walk, &$candidates, &$visited, &$truncated, &$warnings, $root): void {
    $dir = $root.'/'.$relative;
    if (is_link($dir)) {
        $warnings[] = 'Skipped linked directory: '.$relative;
        return;
    }
    if (!is_dir($dir)) {
        return;
    }
    if ($depth > 10) {
        $truncated = true;
        return;
    }
    try {
        $items = new FilesystemIterator($dir, FilesystemIterator::SKIP_DOTS);
    } catch (UnexpectedValueException) {
        $warnings[] = 'Could not list directory: '.$relative;
        return;
    }
    foreach ($items as $entry) {
        if (++$visited > 3000 || count($candidates) >= 200) {
            $truncated = true;
            return;
        }
        $item = $entry->getFilename();
        if (str_starts_with($item, '.') || in_array($item, ['node_modules', 'vendor', 'storage', 'cache', 'build', 'dist'], true)) {
            continue;
        }
        $next = $relative.'/'.$item;
        if (is_link($root.'/'.$next)) {
            $warnings[] = 'Skipped linked entry: '.$next;
        } elseif (is_dir($root.'/'.$next)) {
            $walk($next, $depth + 1);
        } elseif (preg_match('/\.(php|vue|jsx|tsx|svelte|js|ts)$/i', $item)) {
            $candidates[] = $next;
        }
    }
};
foreach (['app/Models', 'app/Http/Controllers', 'resources/views', 'resources/js', 'routes'] as $path) {
    // Never cross a linked parent of an inventory root.
    $parent = $root;
    $linked = false;
    foreach (explode('/', $path) as $part) {
        $parent .= '/'.$part;
        if (is_link($parent)) {
            $linked = true;
            break;
        }
    }
    if ($linked) {
        $warnings[] = 'Skipped inventory root with linked parent: '.$path;
    } else {
        $walk($path);
    }
}
$isLaravel = isset($declared['laravel/framework']) || isset($locked['laravel/framework']);
sort($candidates);
rb_output([
    'schema_version' => 1,
    'laravel_detected' => $isLaravel,
    'artisan_present' => is_file($root.'/artisan') && !is_link($root.'/artisan'),
    'vendor_present' => is_file($root.'/vendor/autoload.php'),
    'declared' => (object) $declared,
    'locked' => (object) $locked,
    'composer_scripts_present' => !empty($composer['scripts']),
    'candidates' => $candidates,
    'truncated' => $truncated,
    'warnings' => $warnings,
    'limitations' => ['Static inventory only; no source code executed.', 'Lockfile versions do not establish installed versions.', 'File candidates do not establish rendering behavior.', 'No environment files or application records read; Composer script bodies are not returned or executed.'],
]);
