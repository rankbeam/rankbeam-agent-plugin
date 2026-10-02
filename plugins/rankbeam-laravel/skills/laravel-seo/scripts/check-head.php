<?php

declare(strict_types=1);

require __DIR__.'/lib.php';

if ($argc !== 2 || in_array($argv[1], ['--help', '-h'], true)) {
    rb_output(['usage' => 'php check-head.php <saved-response.html>', 'requires' => 'PHP 8.2+ and ext-dom', 'exit_codes' => ['0' => 'No errors or warnings in checked signals', '1' => 'Findings', '2' => 'Input/runtime error']], $argc === 2 ? 0 : 2);
}
rb_local_path($argv[1]);
if (!in_array(strtolower(pathinfo($argv[1], PATHINFO_EXTENSION)), ['html', 'htm'], true)) {
    rb_error('unsupported_extension', 'Save the response as an .html or .htm file.');
}
if (!class_exists(DOMDocument::class)) {
    rb_error('missing_dom', 'Enable the PHP DOM extension to inspect saved HTML.');
}
$html = rb_read($argv[1], 2097152);
if (trim($html) === '') {
    rb_error('empty_html', 'The HTML input is empty.');
}
// External entities are never expanded; network access is explicitly disabled.
$previousErrors = libxml_use_internal_errors(true);
$dom = new DOMDocument();
$loaded = $dom->loadHTML('<?xml encoding="UTF-8">'.$html, LIBXML_NONET | LIBXML_NOERROR | LIBXML_NOWARNING);
libxml_clear_errors();
libxml_use_internal_errors($previousErrors);
if (!$loaded) {
    rb_error('unparseable_html', 'The file could not be parsed as HTML.');
}
$xpath = new DOMXPath($dom);
$findings = [];
$add = function (string $code, string $severity, string $message) use (&$findings): void {
    $findings[] = compact('code', 'severity', 'message');
};
$query = function (string $expression) use ($xpath): array {
    return iterator_to_array($xpath->query($expression));
};
$asciiLower = "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'";
$titles = $query('//head/title');
$descriptions = $query("//head/meta[translate(@name, {$asciiLower})='description']");
$canonicals = $query("//head/link[contains(concat(' ', normalize-space(translate(@rel, {$asciiLower})), ' '), ' canonical ')]");
$values = [];
foreach (['title' => [$titles, null], 'description' => [$descriptions, 'content'], 'canonical' => [$canonicals, 'href']] as $field => [$nodes, $attribute]) {
    $values[$field] = array_map(static fn (DOMNode $node): string => trim($attribute === null ? $node->textContent : $node->getAttribute($attribute)), $nodes);
    if (count($nodes) === 0 || in_array('', $values[$field], true)) {
        $add('missing_'.$field, 'error', "A nonempty {$field} is missing from the head.");
    }
    if (count($nodes) > 1) {
        $add('duplicate_'.$field, 'error', "The head contains multiple {$field} elements.");
    }
}
$absolute = static function (string $url): bool {
    $parts = parse_url($url);
    return is_array($parts) && in_array(strtolower($parts['scheme'] ?? ''), ['http', 'https'], true) && !empty($parts['host']) && !isset($parts['user']) && !isset($parts['pass']) && !preg_match('/[\x00-\x20\x7f]/', $url);
};
foreach ($values['canonical'] as $url) {
    if ($url !== '' && !$absolute($url)) {
        $add('invalid_canonical', 'error', 'A canonical must be an absolute HTTP(S) URL without credentials or whitespace.');
    }
}
$robots = [];
foreach ($query("//head/meta[translate(@name, {$asciiLower})='robots' or translate(@name, {$asciiLower})='googlebot']") as $node) {
    $scope = strtolower($node->getAttribute('name'));
    $tokens = preg_split('/[\s,]+/', strtolower(trim($node->getAttribute('content'))), -1, PREG_SPLIT_NO_EMPTY);
    $robots[$scope] = array_values(array_unique(array_merge($robots[$scope] ?? [], $tokens)));
}
// Generic robots applies to Googlebot too, but do not merge unrelated agents.
$robotScopes = $robots;
if (isset($robots['googlebot'])) {
    $robotScopes['googlebot'] = array_unique(array_merge($robots['robots'] ?? [], $robots['googlebot']));
}
foreach ($robotScopes as $scope => $tokens) {
    if (in_array('none', $tokens, true)) {
        $tokens = array_merge($tokens, ['noindex', 'nofollow']);
    }
    if (in_array('all', $tokens, true)) {
        $tokens = array_merge($tokens, ['index', 'follow']);
    }
    foreach ([['index', 'noindex'], ['follow', 'nofollow']] as [$yes, $no]) {
        if (in_array($yes, $tokens, true) && in_array($no, $tokens, true)) {
            $add('robots_conflict', 'warning', "{$scope} contains both {$yes} and {$no}; inspect the intended policy.");
        }
    }
    if (in_array('noindex', $tokens, true)) {
        $add('noindex_present', 'info', "{$scope} requests noindex. This can be intentional; preserve staging and private-page protection.");
    }
}
$jsonld = $query("//script[translate(@type, {$asciiLower})='application/ld+json']");
$jsonldValid = 0;
foreach ($jsonld as $node) {
    try {
        $data = json_decode($node->textContent, false, 128, JSON_THROW_ON_ERROR);
        if (!is_object($data) && !is_array($data)) {
            $add('jsonld_not_object_or_array', 'error', 'A JSON-LD block is a scalar rather than an object or array.');
        } else {
            ++$jsonldValid;
        }
    } catch (JsonException) {
        $add('invalid_jsonld', 'error', 'A JSON-LD block is empty or contains invalid JSON.');
    }
}
if ($jsonld === []) {
    $add('no_jsonld', 'info', 'No JSON-LD found; whether it is needed depends on the page.');
}
$alternates = [];
foreach ($query("//head/link[@hreflang and contains(concat(' ', normalize-space(translate(@rel, {$asciiLower})), ' '), ' alternate ')]") as $node) {
    $code = strtolower(trim($node->getAttribute('hreflang')));
    if ($code === '') {
        $add('empty_hreflang', 'warning', 'An alternate has an empty language code.');
    } elseif (isset($alternates[$code])) {
        $add('duplicate_hreflang', 'warning', 'The head repeats a language code in hreflang alternates.');
    }
    $alternates[$code] = true;
    if (!$absolute($node->getAttribute('href'))) {
        $add('invalid_hreflang_url', 'warning', 'An alternate URL is not an absolute HTTP(S) URL.');
    }
}
$blocking = array_filter($findings, static fn (array $finding): bool => $finding['severity'] !== 'info');
rb_output([
    'schema_version' => 1,
    'status' => $blocking === [] ? 'pass' : 'findings',
    'counts' => ['title' => count($titles), 'description' => count($descriptions), 'canonical' => count($canonicals), 'jsonld' => count($jsonld), 'jsonld_syntax_valid' => $jsonldValid, 'hreflang_languages' => count($alternates)],
    'findings' => $findings,
    'limitations' => ['Saved HTML only; HTTP status, headers and redirects are not checked.', 'No JavaScript execution or browser navigation.', 'Canonical destination, public origin and reachability are not verified.', 'JSON-LD syntax/shape only, not Schema.org or rich-result validation.', 'No social preview, ranking, indexing or AI-citation guarantee.'],
], $blocking === [] ? 0 : 1);
