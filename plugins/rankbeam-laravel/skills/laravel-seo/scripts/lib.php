<?php

declare(strict_types=1);

// Local-only shared input handling. No application code is loaded.
function rb_output(array $data, int $status = 0): never
{
    echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_INVALID_UTF8_SUBSTITUTE), PHP_EOL;
    exit($status);
}

function rb_error(string $code, string $message): never
{
    rb_output(['schema_version' => 1, 'error' => ['code' => $code, 'message' => $message]], 2);
}

function rb_local_path(string $path): void
{
    if ($path === '' || str_contains($path, "\0") || preg_match('~^[a-z][a-z0-9+.-]*://~i', $path)) {
        rb_error('invalid_path', 'Supply a local filesystem path, not a URL or PHP stream.');
    }
}

function rb_read(string $path, int $limit): string
{
    rb_local_path($path);
    if (is_link($path) || !is_file($path) || !is_readable($path)) {
        rb_error('unreadable_file', 'The requested input must be a readable regular file, not a symbolic link.');
    }
    $handle = @fopen($path, 'rb');
    if ($handle === false) {
        rb_error('unreadable_file', 'Could not open the requested input file.');
    }
    $bytes = stream_get_contents($handle, $limit + 1);
    fclose($handle);
    if ($bytes === false || strlen($bytes) > $limit) {
        rb_error('input_too_large', "Input exceeds the {$limit}-byte limit or could not be read.");
    }
    return $bytes;
}

function rb_json(string $path, int $limit): array
{
    $raw = rb_read($path, $limit);
    if (str_starts_with($raw, "\xEF\xBB\xBF")) {
        $raw = substr($raw, 3);
    }
    try {
        $json = json_decode($raw, true, 128, JSON_THROW_ON_ERROR);
    } catch (JsonException) {
        rb_error('invalid_json', 'A required Composer metadata file contains invalid JSON.');
    }
    if (!is_array($json) || !str_starts_with(ltrim($raw), '{')) {
        rb_error('invalid_json_shape', 'Composer metadata must be a JSON object.');
    }
    return $json;
}
