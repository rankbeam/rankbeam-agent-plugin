"""Exercise released Core in an explicitly marked, disposable Laravel fixture.

The caller creates a fresh Laravel application, installs rankbeam/laravel-seo
3.21.1, and writes .rankbeam-plugin-fixture containing `disposable`. No real
application or existing database is accepted. No external HTTP is used here.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time
from urllib.request import urlopen

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'plugins/rankbeam-laravel/skills/laravel-seo/scripts'

def main():
    if not __debug__:
        raise RuntimeError('Run without -O: fixture guards and checks require assertions.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    app=args.app.resolve();output=args.output.resolve()
    assert (app/'.rankbeam-plugin-fixture').read_text(encoding='utf-8').strip()=='disposable', 'Fixture marker required'
    assert not (app/'.env').exists(), 'Do not use a configured application'
    assert not (app/'database/plugin-fixture.sqlite').exists(), 'Use a fresh fixture database'
    assert (app/'vendor/rankbeam/laravel-seo/composer.json').exists(), 'Install released Core first'
    output.mkdir(parents=True,exist_ok=True)
    php=subprocess.check_output([shutil.which('php') or 'php','-r','echo PHP_BINARY;'],text=True).strip()
    env=os.environ.copy()
    env.update(APP_ENV='testing',APP_KEY='base64:QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUE=',APP_DEBUG='false',APP_URL='https://plugin-fixture.test',DB_CONNECTION='sqlite',DB_DATABASE=str(app/'database/plugin-fixture.sqlite'),CACHE_STORE='array',SESSION_DRIVER='array',QUEUE_CONNECTION='sync',MAIL_MAILER='array',SEO_INDEXING_GUARD='false')
    receipts=[]
    def run(arguments,expected=0):
        proc=subprocess.run([php,*map(str,arguments)],cwd=app,env=env,capture_output=True,text=True,encoding='utf-8',timeout=40)
        assert proc.returncode==expected, proc.stdout+proc.stderr
        return proc.stdout
    def artisan(*arguments,expected=0):return run(['artisan',*arguments],expected)
    def check(name,condition,detail):
        assert condition, name+': '+str(detail)
        receipts.append({'case':name,'status':'pass','observed':detail})
    def write(relative,text):
        target=app/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8')
    write('app/Models/Post.php',r'''<?php
namespace App\Models;
use Illuminate\Database\Eloquent\Model;
use Rankbeam\Seo\Traits\HasSEO;
class Post extends Model {
    use HasSEO;
    protected $guarded = [];
    public function getUrlForSEO(): string { return route('posts.show', $this); }
    public function getSEOTitle(): ?string { return $this->title; }
    public function getSEODescription(): ?string { return $this->excerpt; }
}
''')
    write('database/migrations/2026_10_02_000000_create_posts_table.php',r'''<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;
return new class extends Migration {
    public function up(): void { Schema::create('posts', function (Blueprint $table) {
        $table->id(); $table->string('title'); $table->text('excerpt'); $table->timestamps();
    }); }
    public function down(): void { Schema::dropIfExists('posts'); }
};
''')
    write('app/Providers/AppServiceProvider.php',r'''<?php
namespace App\Providers;
use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\URL;
class AppServiceProvider extends ServiceProvider {
    public function register(): void {}
    public function boot(): void {
        URL::forceRootUrl('https://plugin-fixture.test'); URL::forceScheme('https');
        config(['seo.title_suffix' => '', 'seo.default_og_image' => 'https://plugin-fixture.test/og.png',
            'seo.audit.models' => [\App\Models\Post::class], 'seo.cache.store' => 'array']);
    }
}
''')
    write('routes/web.php',r'''<?php
use Illuminate\Support\Facades\Route;
use App\Models\Post;
Route::get('/posts/{post}', fn (Post $post) => view('post', compact('post')))->name('posts.show');
''')
    duplicate='<!doctype html><html><head><title>Old manual title</title>@seo($post)</head><body><h1>{{ $post->title }}</h1><p>{{ $post->excerpt }}</p></body></html>'
    fixed=duplicate.replace('<title>Old manual title</title>','')
    write('resources/views/post.blade.php',duplicate)
    (app/'database/plugin-fixture.sqlite').touch()
    artisan('package:discover','--ansi')
    artisan('vendor:publish','--tag=seo-config','--no-interaction')
    artisan('migrate','--no-interaction')
    empty=json.loads(artisan('seo:audit','--json','--limit=20'))
    check('empty audit is zero coverage',empty['summary']['pages']==0,empty['summary'])
    write('seed-plugin-fixture.php',r'''<?php
require __DIR__.'/vendor/autoload.php';
$app=require __DIR__.'/bootstrap/app.php';
$app->make(\Illuminate\Contracts\Console\Kernel::class)->bootstrap();
$post=\App\Models\Post::create([
    'title'=>'A practical Laravel metadata verification example',
    'excerpt'=>'This synthetic article supplies enough descriptive context to exercise the released metadata audit without using any real customer or production data.'
]);
$post->saveSEO(['title'=>'An explicit editorial title for the Laravel example']);
echo $post->getKey();
''')
    key=run(['seed-plugin-fixture.php']).strip();check('seed one synthetic record',key=='1',{'key':key})
    audit=json.loads(artisan('seo:audit','--model=App\\Models\\Post','--limit=20','--json'))
    (output/'audit.json').write_text(json.dumps(audit,indent=2))
    check('bounded Core audit',audit['summary']['pages']==1 and not audit['skipped'],audit['summary'])
    trace=json.loads(artisan('seo:explain','App\\Models\\Post','1','--json'))
    (output/'explain.json').write_text(json.dumps(trace,indent=2))
    check('explicit value overrides computed title','explicit' in json.dumps(trace['fields']['title']['winner']).lower() and trace['fields']['title']['final']=='An explicit editorial title for the Laravel example',trace['fields']['title'])
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    log=open(output/'server.log','w',encoding='utf-8')
    server=subprocess.Popen([php,'-S',f'127.0.0.1:{port}',str(app/'vendor/laravel/framework/src/Illuminate/Foundation/resources/server.php')],cwd=app/'public',env=env,stdout=log,stderr=log)
    try:
        for attempt in range(50):
            try:
                with urlopen(f'http://127.0.0.1:{port}/posts/1',timeout=2) as response:
                    html=response.read();status=response.status;contenttype=response.headers.get_content_type()
                break
            except OSError:
                if server.poll() is not None:raise RuntimeError('Fixture server exited')
                time.sleep(.1)
        else:raise RuntimeError('Fixture server did not become ready')
        check('real HTTP response',status==200 and contenttype=='text/html',{'status':status,'content_type':contenttype})
        before=output/'before.html';before.write_bytes(html)
        result=json.loads(run([SCRIPTS/'check-head.php',before],1))
        check('duplicate head detected',any(f['code']=='duplicate_title' for f in result['findings']),result['findings'])
        write('resources/views/post.blade.php',fixed)
        artisan('view:clear')
        with urlopen(f'http://127.0.0.1:{port}/posts/1',timeout=5) as response:html=response.read()
        after=output/'after.html';after.write_bytes(html)
        result=json.loads(run([SCRIPTS/'check-head.php',after]))
        check('fixed raw head passes',result['status']=='pass',result['counts'])
        check('correct public canonical',b'https://plugin-fixture.test/posts/1' in html,{'canonical':'https://plugin-fixture.test/posts/1'})
        check('stored editorial title preserved',b'An explicit editorial title for the Laravel example' in html,{'stored_title_unchanged':True})
    finally:
        server.terminate()
        try:server.wait(timeout=5)
        except subprocess.TimeoutExpired:server.kill();server.wait(timeout=5)
        log.close()
    env['SEO_INDEXING_GUARD']='true'
    guard=json.loads(artisan('seo:explain','App\\Models\\Post','1','--json'))
    check('local indexing guard preserved','noindex' in guard['fields']['robots']['final'],guard['fields']['robots'])
    guarded=json.loads(artisan('seo:audit','--model=App\\Models\\Post','--limit=20','--json','--strict'))
    check('intentional guard is separate from audit defects',guarded['indexing_guard']['active'] and guarded['summary']['issues']==0,{'guard':guarded['indexing_guard'],'summary':guarded['summary']})
    write('mutate-plugin-fixture.php',r'''<?php
require __DIR__.'/vendor/autoload.php';
$app=require __DIR__.'/bootstrap/app.php';
$app->make(\Illuminate\Contracts\Console\Kernel::class)->bootstrap();
\App\Models\Post::findOrFail(1)->saveSEO(['title'=>'x']);
''')
    run(['mutate-plugin-fixture.php'])
    strict=json.loads(artisan('seo:audit','--model=App\\Models\\Post','--limit=20','--json','--strict',expected=1))
    check('strict audit fails on actual metadata defects',strict['summary']['issues']>0,strict['summary'])
    skipped=json.loads(artisan('seo:audit','--model=App\\Models\\User','--limit=20','--json'))
    check('non-HasSEO model is a coverage gap',bool(skipped['skipped']) and skipped['summary']['pages']==0,{'skipped':skipped['skipped'],'pages':skipped['summary']['pages']})
    check('fixture server stopped',server.poll() is not None,{'server_running':False})
    lock=json.loads((app/'composer.lock').read_text(encoding='utf-8'))
    versions={p['name']:p['version'] for p in lock['packages'] if p['name'] in ['laravel/framework','rankbeam/laravel-seo']}
    report={'type':'operator-executed workflow integration; not model activation evaluation','runtime':run(['-r','echo PHP_VERSION;']).strip(),'packages':versions,'cases':receipts,'fixture_only':True,'external_http_requests':0,'html_sha256':hashlib.sha256((output/'after.html').read_bytes()).hexdigest()}
    (output/'result.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'packages':versions,'passed':len(receipts),'report':str(output/'result.json')},indent=2))

if __name__=='__main__':main()
