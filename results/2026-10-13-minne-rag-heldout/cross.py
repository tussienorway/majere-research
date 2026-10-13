import sys, os, time, json, random, signal, subprocess, tempfile, sqlite3, multiprocessing as mp
sys.path.insert(0, os.getcwd()); sys.path.insert(0, os.path.dirname(__file__)); import data
which=sys.argv[1]; mode=sys.argv[2] if len(sys.argv)>2 else "main"
def open_store(path, emb="e5"):
    if which=="41":
        from memory_rag.store import MemoryStore; from memory_rag.embed import get_embedder
        return MemoryStore(path, get_embedder(emb))
    from memory_rag2.store import MemoryStore; from memory_rag2.embeddings import E5Embedder, DeterministicEmbedder
    return MemoryStore(path, E5Embedder() if emb=="e5" else DeterministicEmbedder())
def add(s,t):
    r=s.add(t, kind="note") if which=="41" else s.add(t, kind="note"); return r.get("id") or r.get("memory_id")
def count(path):
    c=sqlite3.connect(path); ic=c.execute("pragma integrity_check").fetchone()[0]
    n=c.execute("select count(*) from memories").fetchone()[0]; return ic,n
def writer(path,k,n):
    s=open_store(path,"hash" if which=="41" else "det")
    for i in range(n): add(s,f"arbeider {k} skriver minne nummer {i} om {random.random()}")
if mode=="child":
    s=open_store(sys.argv[3],"hash" if which=="41" else "det"); i=0
    while True: add(s,f"drepetest {i} {random.random()} "*5); i+=1
d=tempfile.mkdtemp(); out={}
# concurrency: 4 procs x 250
p=os.path.join(d,"c.db"); open_store(p,"hash" if which=="41" else "det")
t=time.time(); ps=[mp.Process(target=writer,args=(p,k,250)) for k in range(4)]; [x.start() for x in ps]; [x.join() for x in ps]
out["concurrent_4x250"]=dict(zip(["integrity","rows"],count(p)), s=round(time.time()-t,1), exitcodes=[x.exitcode for x in ps])
# kill test: 15 SIGKILLs
p=os.path.join(d,"k.db"); open_store(p,"hash" if which=="41" else "det"); bad=0
for i in range(15):
    c=subprocess.Popen([sys.executable,__file__,which,"child",p]); time.sleep(random.uniform(.5,1.5)); c.send_signal(signal.SIGKILL); c.wait()
    ic,n=count(p); bad+= ic!="ok"
s=open_store(p,"hash" if which=="41" else "det"); ok = len(s.search("drepetest",limit=3) if which=="41" else s.search("drepetest",limit=3)["hits"])>0
out["kill15"]=dict(integrity_failures=bad, rows=n, search_after=ok)
print(json.dumps(out))
