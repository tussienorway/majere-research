import sys, time, json, tempfile, os, statistics
sys.path.insert(0, os.path.dirname(__file__)); import data
which = sys.argv[1]; T0 = 1.70e9
sys.path.insert(0, os.getcwd())
d = tempfile.mkdtemp()
if which == "41":
    from memory_rag.store import MemoryStore; from memory_rag.embed import get_embedder
    s = MemoryStore(os.path.join(d,"m.db"), get_embedder("e5"))
    def add_many(texts, ts): return [r["id"] for r in s.add_many([dict(text=t, kind="fact", created_at=ts) for t in texts])]
    def sup(old, t): return s.supersede(old, t, created_at=T0+86400*30)["id"]
    def search(q): return [h["id"] for h in s.search(q, limit=5)]
else:
    from memory_rag2.store import MemoryStore; from memory_rag2.embeddings import E5Embedder
    s = MemoryStore(os.path.join(d,"m.db"), E5Embedder())
    def add_many(texts, ts): return [s.add(t, created_at=ts)["memory_id"] for t in texts]
    def sup(old, t): return s.supersede(old, t, created_at=T0+86400*30)["memory_id"]
    def search(q): return [h["memory_id"] for h in s.search(q, limit=5)["hits"]]
t=time.time()
dist = data.distractors(int(os.environ.get("NDIST","2000"))); add_many(dist, T0); add_many(data.NEAR, T0)
labels=list(data.FACTS); ids=dict(zip(labels, add_many([data.FACTS[l] for l in labels], T0)))
olds = add_many([o for o,_,_ in data.SUPER], T0); news=[sup(o,n) for o,(_,n,_) in zip(olds,data.SUPER)]
ins=time.time()-t
lat=[]; r1=r5=mrr=0; cats={}
def rank(q, target):
    t=time.perf_counter(); h=search(q); lat.append((time.perf_counter()-t)*1000)
    return h.index(target)+1 if target in h else None, h
for q,l,c in data.QUERIES:
    rk,_=rank(q, ids[l]); r1+=rk==1; r5+=rk is not None; mrr+= 1/rk if rk else 0
    cats.setdefault(c,[0,0]); cats[c][0]+=rk==1; cats[c][1]+=1
sa=0; sa5=0; fails=[]
for (o,n,q),oid,nid in zip(data.SUPER,olds,news):
    rk,h=rank(q,nid); ok = rk==1 and (oid not in h or h.index(oid)>0); sa+=ok; sa5+=rk is not None
    if not ok: fails.append(q)
N=len(data.QUERIES); lat.sort()
print(json.dumps(dict(pr=which, n=N, r1=round(r1/N,3), r5=round(r5/N,3), mrr=round(mrr/N,3), supersession=f"{sa}/10", super_r5=f"{sa5}/10",
  p50_ms=round(statistics.median(lat),1), p95_ms=round(lat[int(.95*len(lat))],1), insert_s=round(ins,1), memories=len(dist)+len(data.NEAR)+50+10,
  per_cat={k:f"{a}/{b}" for k,(a,b) in cats.items()}, super_fail=fails), ensure_ascii=False))
