"""Generate the two documented manifest formats from one maintained definition."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/rankbeam-laravel'
REPO = 'https://github.com/rankbeam/rankbeam-agent-plugin'
identity = {
    'name': 'rankbeam-laravel',
    'version': '1.0.0',
    'description': 'Inspect Laravel SEO, integrate Rankbeam Core, explain resolved metadata and verify saved page HTML in a local project.',
    'author': {'name': 'Valentin Goxhaj', 'email': 'hello@rankbeam.dev', 'url': 'https://rankbeam.dev'},
    'homepage': REPO,
    'repository': REPO,
    'license': 'MIT',
    'keywords': ['laravel', 'seo', 'rankbeam', 'canonical', 'metadata', 'json-ld'],
}
interface = {
    'displayName': 'Rankbeam for Laravel',
    'shortDescription': 'Inspect and fix Laravel SEO',
    'longDescription': 'Inspect technical SEO in a local Laravel application, identify missing or duplicate head tags, and trace unexpected Rankbeam metadata to its source. Set up Rankbeam Core when requested and verify the affected page after a fix. Includes local PHP helpers for project inspection and saved-HTML checks. Requires access to the Laravel project and PHP 8.2 or later; HTML checks require the PHP DOM extension. No Rankbeam account is needed. This version contains skills and local helpers, with no hosted service or MCP connection. It does not measure rankings, guarantee indexing or crawl websites.',
    'developerName': 'Valentin Goxhaj',
    'category': 'Developer Tools',
    'capabilities': ['Inspect Laravel projects', 'Explain SEO metadata', 'Check saved HTML', 'Integrate Rankbeam Core'],
    'websiteURL': REPO,
    'supportURL': REPO + '/blob/main/SUPPORT.md',
    'privacyPolicyURL': REPO + '/blob/main/PRIVACY.md',
    'termsOfServiceURL': REPO + '/blob/main/LICENSE',
    'defaultPrompt': [
        'Inspect this Laravel project for technical SEO problems without changing files.',
        'Set up Rankbeam Core for an existing page and verify its rendered head.',
        'Explain why this page has the wrong canonical URL and fix the source of the problem.',
    ],
    'brandColor': '#2457D6',
    'composerIcon': './assets/icon.png',
    'logo': './assets/icon.png',
}
extra = {'publication': {'release_notes': 'Initial release with Laravel project inspection, Core setup and diagnostics, and saved-HTML verification.'}}
portable = {'$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json', **identity, 'extensions': {'com.openai': {'interface': interface, **extra}}}
compat = {**identity, 'skills': './skills/', 'interface': interface, 'extensions': {'com.openai': extra}}
for path, data in [(PLUGIN/'plugin.json', portable), (PLUGIN/'.codex-plugin/plugin.json', compat)]:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8', newline='\n')
marketplace = {
    'name': 'rankbeam', 'interface': {'displayName': 'Rankbeam'},
    'plugins': [{'name': identity['name'], 'source': {'source': 'local', 'path': './plugins/rankbeam-laravel'},
                 'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Developer Tools'}],
}
market = ROOT/'.agents/plugins/marketplace.json'
market.parent.mkdir(parents=True, exist_ok=True)
market.write_text(json.dumps(marketplace, indent=2)+'\n', encoding='utf-8', newline='\n')
