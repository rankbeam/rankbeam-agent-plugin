"""Check actual loopback responses against the committed reference fixture."""
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
from urllib.request import urlopen

class Head(HTMLParser):
    def __init__(self):super().__init__();self.head=False;self.title=False;self.titles=[];self.canonicals=[];self.schema=0;self.description=0
    def handle_starttag(self,tag,attributes):
        attrs=dict(attributes)
        if tag=='head':self.head=True
        if not self.head:return
        if tag=='title':self.title=True;self.titles.append('')
        if tag=='link' and attrs.get('rel')=='canonical':self.canonicals.append(attrs.get('href'))
        if tag=='meta' and attrs.get('name')=='description':self.description+=1
        if tag=='script' and attrs.get('type')=='application/ld+json':self.schema+=1
    def handle_endtag(self,tag):
        if tag=='head':self.head=False
        if tag=='title':self.title=False
    def handle_data(self,text):
        if self.head and self.title:self.titles[-1]+=text

def main():
    if not __debug__:raise RuntimeError('Run without Python optimization (-O/-OO).')
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--lab',type=Path,required=True);p.add_argument('--stack',required=True)
    p.add_argument('--csr',action='store_true');a=p.parse_args();lab=a.lab.resolve()
    if (lab/'.rankbeam-plugin-fixture').read_text().strip()!='disposable':raise SystemExit('Fixture marker required.')
    spec=next(v for v in json.loads((lab/'lab.json').read_text())['apps'] if v['stack']==a.stack)
    base=f"http://127.0.0.1:{spec['port']}"
    fixtures=json.loads((lab/'packages/examples-shared/resources/contract-fixtures.json').read_text())['pages']
    script=Path(__file__).resolve().parents[1]/'plugins/rankbeam-laravel/skills/laravel-seo/scripts/check-head.php'
    output=lab/'evidence'/a.stack/('csr' if a.csr else 'ssr');output.mkdir(parents=True,exist_ok=True)
    results=[]
    for page in fixtures:
        with urlopen(base+page['path'],timeout=20) as response:
            raw=response.read();status=response.status;content_type=response.headers.get_content_type()
        assert status==200 and content_type=='text/html'
        file=output/(page['key']+'.html');file.write_bytes(raw)
        head=Head();head.feed(raw.decode('utf-8'))
        if a.csr:
            assert not head.canonicals and not head.description
        else:
            assert head.titles==[page['expect']['title']],head.titles
            assert head.canonicals==[base+page['expect']['canonical_path']],head.canonicals
            assert head.schema==int(page['expect']['schema']['present'])
        cmd=[shutil.which('php'),str(script),str(file),'--expected-canonical',base+page['expect']['canonical_path']]
        if page['expect']['schema']['present'] and not a.csr:cmd.append('--require-jsonld')
        check=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',check=False)
        data=json.loads(check.stdout);codes=[v['code'] for v in data.get('findings',[])]
        if not a.csr:
            allowed={'no_jsonld','noindex_present'}
            if not page['expect'].get('description_present',True):allowed.add('missing_description')
            assert set(codes)<=allowed,codes
        else:assert 'missing_canonical' in codes
        results.append({'page':page['key'],'http_status':status,'content_type':content_type,'title_count':len(head.titles),'canonical_count':len(head.canonicals),'jsonld_count':head.schema,'checker_codes':codes,'sha256':hashlib.sha256(raw).hexdigest()})
    report={'stack':a.stack,'mode':'csr raw metadata absence' if a.csr else 'server-rendered raw response','pages':results}
    (output/'receipt.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
