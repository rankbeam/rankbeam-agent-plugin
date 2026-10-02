"""Run a credential-free before/after HTML demonstration in a temporary directory."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

script=Path(__file__).resolve().parents[1]/'plugins/rankbeam-laravel/skills/laravel-seo/scripts/check-head.php'
before='<!doctype html><html><head><title>Editorial title</title><title>Old layout</title><meta name="description" content="Useful summary"><link rel="canonical" href="/article"><meta name="robots" content="noindex,nofollow"></head><body>Unchanged content</body></html>'
after=before.replace('<title>Old layout</title>','').replace('href="/article"','href="https://example.test/article"')
with tempfile.TemporaryDirectory(prefix='rankbeam-demo-') as directory:
    for label,html,expected in [('before',before,1),('after',after,0)]:
        file=Path(directory)/(label+'.html');file.write_text(html,encoding='utf-8')
        result=subprocess.run([shutil.which('php') or 'php',str(script),str(file),'--expected-canonical','https://example.test/article'],capture_output=True,text=True,timeout=15)
        if result.returncode!=expected:raise RuntimeError(result.stdout+result.stderr)
        data=json.loads(result.stdout)
        print(json.dumps({'stage':label,'status':data['status'],'counts':data['counts'],'findings':data['findings']},indent=2))
