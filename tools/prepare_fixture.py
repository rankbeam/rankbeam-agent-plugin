"""Download a fresh, disposable Laravel app for the integration harness.

Requires PHP, Composer and network access. The destination must not exist.
Composer scripts/plugins are disabled during installation. No app is booted.
"""
import argparse
import json
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--laravel', choices=['12', '13'], required=True)
    parser.add_argument('--app', type=Path, required=True)
    args = parser.parse_args()
    app = args.app.resolve()
    if app.exists():
        raise SystemExit('Destination already exists; choose a fresh disposable path.')
    composer = shutil.which('composer')
    if not composer:
        raise SystemExit('Composer must be on PATH.')
    subprocess.run([composer, 'create-project', 'laravel/laravel', str(app),
                    args.laravel+'.*', '--no-install', '--no-scripts', '--no-plugins',
                    '--no-interaction', '--prefer-dist'], check=True)
    manifest = app/'composer.json'
    data = json.loads(manifest.read_text(encoding='utf-8'))
    data['require']['rankbeam/laravel-seo'] = '3.21.1'
    data['require-dev'] = {}
    data['scripts'] = {}
    manifest.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    subprocess.run([composer, 'update', '--no-dev', '--no-scripts', '--no-plugins',
                    '--no-interaction', '--prefer-dist'], cwd=app, check=True)
    (app/'.rankbeam-plugin-fixture').write_text('disposable', encoding='utf-8')
    print('Prepared fresh fixture: '+str(app))


if __name__ == '__main__':
    main()
