"""Export committed Rankbeam examples into a fresh disposable rendering lab.

Downloads released Core and framework dependencies; never reads source .env or
databases. App ports are fixed here for the local acceptance run, not production.
"""
import argparse
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--examples',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();out=args.output.resolve()
    if out.exists():raise SystemExit('Use a new destination.')
    source=args.examples.resolve()
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=source,text=True).strip()
    archive=subprocess.check_output(['git','archive','--format=zip','HEAD'],cwd=source)
    out.mkdir(parents=True)
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        for item in z.infolist():
            if not (out/item.filename).resolve().is_relative_to(out):raise RuntimeError('Unsafe archive member')
        z.extractall(out)
    (out/'.rankbeam-plugin-fixture').write_text('disposable')
    php=subprocess.check_output([shutil.which('php'),' -v'.strip()],text=True).splitlines()[0]
    composer=shutil.which('composer');npm=shutil.which('npm')
    env=os.environ.copy();env.update(APP_ENV='testing',APP_DEBUG='false',SEO_INDEXING_GUARD='false')
    reports=[]
    for index,stack in enumerate(['blade','inertia-vue','inertia-react','inertia-svelte','livewire']):
        app=out/'apps'/stack
        data=json.loads((app/'composer.json').read_text())
        data['require']['rankbeam/laravel-seo']='3.21.1'
        data['repositories']=[{'type':'path','url':'../../packages/examples-shared','options':{'symlink':False}}]
        (app/'composer.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
        (app/'composer.lock').unlink(missing_ok=True)
        db=app/'database/plugin-rendering.sqlite';db.touch()
        (app/'.env').write_text('\n'.join(['APP_NAME=Rankbeam','APP_ENV=testing','APP_DEBUG=false',
            'APP_KEY=base64:QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE=',f'APP_URL=http://127.0.0.1:{8310+index}',
            'DB_CONNECTION=sqlite',f'DB_DATABASE="{db.as_posix()}"','CACHE_STORE=array','SESSION_DRIVER=array',
            'QUEUE_CONNECTION=sync','MAIL_MAILER=array','SEO_INDEXING_GUARD=false','APP_LOCALE=en-US',
            'SEO_TWITTER_SITE=@rankbeam','SEO_DEFAULT_OG_IMAGE=/images/og-default.jpg',
            'SEO_DEFAULT_ROBOTS=index,follow','SEO_AUTO_CREATE_META=false'])+'\n',encoding='utf-8')
        with (out/f'{stack}-setup.log').open('w',encoding='utf-8') as log:
            def run(cmd):subprocess.run(cmd,cwd=app,env=env,stdout=log,stderr=log,check=True,timeout=600)
            run([composer,'update','--no-dev','--no-scripts','--no-plugins','--no-interaction','--prefer-dist'])
            run([shutil.which('php'),'artisan','package:discover'])
            run([shutil.which('php'),'artisan','migrate','--seed','--no-interaction'])
            if stack.startswith('inertia'):
                run([npm,'ci','--ignore-scripts','--no-audit','--no-fund'])
                run([npm,'run','build'])
        lock=json.loads((app/'composer.lock').read_text(encoding='utf-8'))
        names=['laravel/framework','rankbeam/laravel-seo','livewire/livewire','inertiajs/inertia-laravel']
        report={'stack':stack,'port':8310+index,'packages':{v['name']:v['version'] for v in lock['packages'] if v['name'] in names}}
        reports.append(report);print(json.dumps(report),flush=True)
    (out/'lab.json').write_text(json.dumps({'examples_commit':revision,'php':php,'apps':reports},indent=2)+'\n')

if __name__=='__main__':main()
