"""Serve one marked rendering fixture on loopback; type stop to clean up."""
import argparse
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess

def available(port):
    with socket.socket() as s:s.bind(('127.0.0.1',port))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lab',type=Path,required=True)
    p.add_argument('--stack',required=True,choices=['blade','livewire','inertia-vue','inertia-react','inertia-svelte'])
    p.add_argument('--ssr',action='store_true')
    a=p.parse_args();lab=a.lab.resolve()
    if (lab/'.rankbeam-plugin-fixture').read_text().strip()!='disposable':raise SystemExit('Fixture marker required.')
    spec=next(v for v in json.loads((lab/'lab.json').read_text())['apps'] if v['stack']==a.stack)
    app=lab/'apps'/a.stack;available(spec['port'])
    php=subprocess.check_output([shutil.which('php'),'-r','echo PHP_BINARY;'],text=True).strip()
    env=os.environ.copy();env.update(APP_ENV='testing',APP_DEBUG='false',SEO_INDEXING_GUARD='false',INERTIA_SSR_ENABLED='true' if a.ssr else 'false')
    processes=[];logs=[]
    try:
        if a.ssr:
            available(13714)
            # The upstream helper defaults to all interfaces. Bind only this
            # disposable runtime's helper to loopback; rendering is unchanged.
            for relative in ['server.esm.js','server.js']:
                file=app/'node_modules/@inertiajs/core/dist'/relative
                if file.exists():
                    text=file.read_text(encoding='utf-8')
                    file.write_text(text.replace('.listen(_port, () =>','.listen(_port, "127.0.0.1", () =>'),encoding='utf-8')
            bundles=list((app/'bootstrap/ssr').glob('ssr.*'))
            bundle=next(v for v in bundles if v.suffix in ['.js','.mjs'])
            log=open(lab/f'{a.stack}-ssr.log','w',encoding='utf-8');logs.append(log)
            processes.append(subprocess.Popen([shutil.which('node'),str(bundle)],cwd=app,env=env,stdout=log,stderr=log))
        log=open(lab/f'{a.stack}-server.log','w',encoding='utf-8');logs.append(log)
        processes.append(subprocess.Popen([php,'-S',f"127.0.0.1:{spec['port']}",str(app/'vendor/laravel/framework/src/Illuminate/Foundation/resources/server.php')],cwd=app/'public',env=env,stdout=log,stderr=log))
        print(json.dumps({'stack':a.stack,'port':spec['port'],'ssr':a.ssr,'owned_pids':[v.pid for v in processes]}),flush=True)
        while input().strip()!='stop':pass
    except (EOFError,KeyboardInterrupt):pass
    finally:
        for process in processes:
            process.terminate()
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait(timeout=5)
        for log in logs:log.close()
        print(json.dumps({'owned_processes_stopped':all(v.poll() is not None for v in processes)}),flush=True)

if __name__=='__main__':main()
