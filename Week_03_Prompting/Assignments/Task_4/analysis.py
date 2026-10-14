import csv, json, sys, math, random, re
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT/"Task_2"/"data")); sys.path.insert(0, str(ROOT/"Task_3"))
from evaluate_retrieval_predictions import load_database, row_multiset
csv.field_size_limit(10**9)
P=["ICIO","RTF","CoT"]
gold=[(r["question"],json.loads(r["result"])) for r in csv.DictReader(open(ROOT/"Task_2/data/restaurants_dataset.csv",encoding="utf-8"))]
f1={p:{} for p in P}
for r in csv.DictReader(open(ROOT/"Task_3/relaxed_f1_scores.csv",encoding="utf-8")):
    f1[r["prompt"]].setdefault(r["question"],[]).append(float(r["relaxed_f1"]))
c=load_database()
acc={p:[] for p in P}; F={p:[] for p in P}; sqls={}
for p in P:
    preds=list(csv.DictReader(open(ROOT/f"Task_2/predictions/{p}.csv",encoding="utf-8")))
    sqls[p]=[x["predicted_sql"] for x in preds]
    idx=Counter()
    for (q,g),x in zip(gold,preds):
        rows=c.execute(x["predicted_sql"]).fetchall()
        acc[p].append(int(row_multiset(rows)==row_multiset(g)))
        F[p].append(f1[p][q][idx[q]]); idx[q]+=1
n=len(gold)
def ci_boot(v,B=5000):
    random.seed(1); m=[sum(random.choice(v) for _ in v)/len(v) for _ in range(B)]; m.sort()
    return m[int(.025*B)],m[int(.975*B)]
print("== summary")
for p in P:
    a=sum(acc[p])/n; lo,hi=ci_boot(acc[p]); fl,fh=ci_boot(F[p])
    print(p,f"acc={a:.4f} CI[{lo:.3f},{hi:.3f}] F1={sum(F[p])/n:.4f} CI[{fl:.3f},{fh:.3f}] F1_perfect={sum(x==1 for x in F[p])} F1_zero={sum(x==0 for x in F[p])} F1_partial={sum(0<x<1 for x in F[p])}")
def mcnemar(a,b):
    b01=sum(1 for x,y in zip(a,b) if x==1 and y==0); b10=sum(1 for x,y in zip(a,b) if x==0 and y==1)
    k=min(b01,b10); m=b01+b10
    pv=min(1,2*sum(math.comb(m,i) for i in range(k+1))/2**m) if m else 1.0
    return b01,b10,pv
def wilcoxon(a,b):
    d=[x-y for x,y in zip(a,b) if x!=y]; m=len(d)
    if m==0: return 0,1.0
    order=sorted(range(m),key=lambda i:abs(d[i])); ranks=[0]*m; i=0
    while i<m:
        j=i
        while j+1<m and abs(d[order[j+1]])==abs(d[order[i]]): j+=1
        for k in range(i,j+1): ranks[order[k]]=(i+j)/2+1
        i=j+1
    wp=sum(r for r,x in zip(ranks,d) if x>0); mu=m*(m+1)/4; sd=math.sqrt(m*(m+1)*(2*m+1)/24)
    z=(wp-mu)/sd; pv=math.erfc(abs(z)/math.sqrt(2))
    return m,pv,z
print("== pairwise")
for a,b in [("ICIO","RTF"),("ICIO","CoT"),("RTF","CoT")]:
    print(a,b,"mcnemar",mcnemar(acc[a],acc[b]),"wilcoxon",wilcoxon(F[a],F[b]))
print("== overlap acc")
print(Counter(tuple(acc[p][i] for p in P) for i in range(n)))
print("== by question type")
def typ(q):
    q=q.lower()
    t=[]
    if "best" in q: t.append("best")
    if " on " in q or "street" in q or " st " in q: t.append("street")
    if "region" in q or "area" in q or "valley" in q: t.append("region?")
    return "+".join(t) or "other"
types=[typ(q) for q,_ in gold]
for t in sorted(set(types)):
    ids=[i for i in range(n) if types[i]==t]
    print(t,len(ids),{p:sum(acc[p][i] for i in ids) for p in P},{p:round(sum(F[p][i] for i in ids)/len(ids),3) for p in P})
print("empty gold",sum(1 for _,g in gold if not g), {p:sum(acc[p][i] for i in range(n) if not gold[i][1]) for p in P})
print("== sql features")
for p in P:
    s=sqls[p]
    print(p,{"select*":sum("SELECT r.*" in x or "SELECT *" in x for x in s),"LIMIT":sum("LIMIT" in x.upper() for x in s),"HOUSE_NUMBER in select":sum(bool(re.search(r"SELECT[^F]*HOUSE_NUMBER",x,re.I)) for x in s),"JOIN LOCATION":sum("LOCATION" in x.upper() for x in s),"GEOGRAPHIC":sum("GEOGRAPHIC" in x.upper() for x in s),"DISTINCT":sum("DISTINCT" in x.upper() for x in s),"MAX":sum("MAX(" in x.upper() for x in s)})
print("== CoT miss");
for i in range(n):
    if not acc["CoT"][i]: print(gold[i][0],"|",sqls["CoT"][i],"| gold rows",len(gold[i][1]))
print("== ICIO/RTF correct but which")
for p in ["ICIO","RTF"]:
    ok=[i for i in range(n) if acc[p][i]]; print(p,"correct with empty gold",sum(1 for i in ok if not gold[i][1]))
json.dump({"acc":acc,"F":F},open(Path(__file__).parent/"per_question.json","w"))

# --- grafy a rozdelenie podľa prázdneho / neprázdneho výsledku
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
empty=[not g for _,g in gold]
for name,sel in [("prazdny",True),("neprazdny",False)]:
    ids=[i for i in range(n) if empty[i]==sel]
    print(name,len(ids),{p:(sum(acc[p][i] for i in ids),round(sum(F[p][i] for i in ids)/len(ids),3)) for p in P})
col={"ICIO":"#4C72B0","RTF":"#DD8452","CoT":"#55A868"}
fig,ax=plt.subplots(figsize=(7,4)); w=.38; x=range(3)
ax.bar([i-w/2 for i in x],[sum(acc[p])/n*100 for p in P],w,label="Accuracy",color="#8da0cb")
ax.bar([i+w/2 for i in x],[sum(F[p])/n*100 for p in P],w,label="Relaxed Result F1",color="#66c2a5")
for i,p in enumerate(P):
    ax.text(i-w/2,sum(acc[p])/n*100+1,f"{sum(acc[p])/n*100:.1f}",ha="center",fontsize=9)
    ax.text(i+w/2,sum(F[p])/n*100+1,f"{sum(F[p])/n*100:.1f}",ha="center",fontsize=9)
ax.set_xticks(list(x)); ax.set_xticklabels(P); ax.set_ylim(0,110); ax.set_ylabel("%"); ax.legend(); ax.set_title("Accuracy a Relaxed Result F1 podľa promptu")
fig.tight_layout(); fig.savefig(Path(__file__).parent/"graf_metriky.png",dpi=150)
fig,ax=plt.subplots(figsize=(7,4)); ne=[i for i in range(n) if not empty[i]]; e=[i for i in range(n) if empty[i]]
ax.bar([i-w/2 for i in x],[sum(acc[p][i] for i in e) for p in P],w,label=f"prázdny výsledok ({len(e)})",color="#bbbbbb")
ax.bar([i+w/2 for i in x],[sum(acc[p][i] for i in ne) for p in P],w,label=f"neprázdny výsledok ({len(ne)})",color="#e78ac3")
ax.set_xticks(list(x)); ax.set_xticklabels(P); ax.set_ylabel("počet správnych otázok"); ax.legend(); ax.set_title("Správne otázky podľa typu očakávaného výsledku")
fig.tight_layout(); fig.savefig(Path(__file__).parent/"graf_prazdne_vysledky.png",dpi=150)
fig,ax=plt.subplots(figsize=(7,4))
cats=[("0",lambda v:v==0),("0–1",lambda v:0<v<1),("1",lambda v:v==1)]
bottom=[0,0,0]
for (lab,fn),cc in zip(cats,["#e15759","#f1ce63","#59a14f"]):
    vals=[sum(fn(v) for v in F[p]) for p in P]; ax.bar(P,vals,bottom=bottom,label=f"F1 = {lab}",color=cc); bottom=[b+v for b,v in zip(bottom,vals)]
ax.set_ylabel("počet otázok"); ax.legend(); ax.set_title("Rozdelenie Relaxed Result F1 po otázkach")
fig.tight_layout(); fig.savefig(Path(__file__).parent/"graf_rozdelenie_f1.png",dpi=150)
