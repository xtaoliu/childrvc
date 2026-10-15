import pandas as pd, re, numpy as np
U='/root/.claude/uploads/0f117633-58b8-57b3-997d-b44c96103ee0/'
# ---------------- comprehension ----------------
c=pd.read_excel(U+'848e94bc-Comprehension_2026.xlsx',sheet_name='critical')
c=c.rename(columns={'VideoContent (targetVP)':'video'})
c['pair']=c['object'].map({k:i+1 for i,k in enumerate('ABCDEFGHIJ')})
c['assoc']=np.where(c.V1==0,'stronger','weaker')
c['form']=np.where(c.sentence_type==1,'RVC','V1')
c['result']=np.where(c.realization=='realized','full','zero')
c['age']=c.age_group.map({0:'adult',1:'4yo',2:'5yo'})
c['accept']=(c.response.str.upper()=='YES').astype(int)
c['item']='P'+c.pair.astype(str)+'_'+c.assoc
c['subj']='C'+c.ID.astype(str)
c['retained']=~c.pair.isin([7,8])
c[['subj','age','gender','month','list','pair','assoc','item','form','result','accept','retained','sentence','video']].to_csv('comp.csv',index=False)
# fillers accuracy
s=pd.read_excel(U+'848e94bc-Comprehension_2026.xlsx',sheet_name='Sheet1')
f=s[s.sentence_type==2]
print('filler acc by age:',f.groupby('age_group').accuracy.mean().round(3).to_dict(), 'n filler',len(f))
# participants
pp=c.groupby('subj').agg(age=('age','first'),g=('gender','first'),m=('month','first'))
def ym(m): return f"{int(m//12)};{int(round(m%12))}"
for a,d in pp.groupby('age'):
    print('EXP1',a,len(d),'female',int((d.g==1).sum()),'range',ym(d.m.min()),ym(d.m.max()),'M',ym(d.m.mean()), round(d.m.mean()/12,2))
# ---------------- production ----------------
X=U+'daa02b98-Production_2026.xlsx'
p=pd.read_excel(X,sheet_name='Critical').rename(columns={'Video content (target VP)':'video','Participant description':'desc'})
vmap={'剥荔枝':(1,'stronger'),'捏荔枝':(1,'weaker'),'掀凳子':(2,'stronger'),'拍凳子':(2,'weaker'),'掰手指':(3,'stronger'),'按食指':(3,'weaker'),
 '撕纸':(4,'stronger'),'扯卫生纸':(4,'weaker'),'吹蜡烛':(5,'stronger'),'挥蜡烛':(5,'weaker'),'踢瓶子':(6,'stronger'),'推瓶子':(6,'weaker'),
 '掐人':(7,'stronger'),'叫醒人':(7,'weaker'),'涂手掌':(8,'stronger'),'挠手掌':(8,'weaker'),'擦镜子':(9,'stronger'),'冲镜子':(9,'weaker'),
 '夹核桃':(10,'stronger'),'锤核桃':(10,'weaker')}
p['pair']=p.video.map(lambda v:vmap[v][0]); p['assoc']=p.video.map(lambda v:vmap[v][1])
p['desc']=p.desc.astype(str)
RES={1:r'开|破|烂',2:r'翻|倒',3:r'弯|曲|折',4:r'开|破|烂|断|碎|两半|两份|坏',5:r'灭|熄|掉',6:r'倒|翻',7:r'醒|起来|起床|坐起',8:r'红|血',
     9:r'干净|净|掉',10:r'开|碎|裂|烂|破'}
STOP=r'开始|离开|开心|开着|开水|打开水|倒水|倒是|起来看'
V=r'剥捏掀拍掰按撕扯拽吹挥踢推掐叫喊唤吵涂挠擦冲夹锤打弄搞砸敲摇晃甩抠抹扳摁压折拉拧钳洗刷扒薅揭抓碰摸剪割捶抽取掀翻扭掐放撬抬举'
COMP=r'(?:得|不)?(?:开|翻|弯|破|烂|断|碎|灭|熄|倒|醒|红|干净|掉|坏|裂|动|下来|起来|出来|成)'
RVC_RE=re.compile(f'[{V}]|mie'+'') 
rvc_re=re.compile(f'(?:[{V}]|mie){COMP}')
act_re=re.compile(f'[{V}]|mie|动了|弄|搞|揉|按|压')
NEG=re.compile(r'(没|不|未|别(?!人))[^，。,]{0,4}$')
ATT=re.compile(r'(想|试图|尝试|企图|打算|准备|试探着想|试着|要)[^，。,；]{0,10}$')
FAIL=re.compile(r'失败|没成功|没有成功|未果|放弃|未成功|不成功|没能|没弄|弄不')
P7CALL=re.compile(r'(叫|喊)[^，。,；]{0,6}(起来|起床)')
def code(desc,pair):
    t=re.sub(STOP,'',desc)
    if pair==7: t=P7CALL.sub(lambda m:m.group(1)+'某人', t)
    if pair==8: t=re.sub(r'红色的?(颜料|东西|印泥|印章|墨|水彩|笔|液体|)','颜色',t)
    rvc=bool(rvc_re.search(t))
    res=[m for m in re.finditer(RES[pair],t)]
    res_m=len(res)>0
    status=''
    if res_m:
        m=res[0]; pre=t[:m.start()]
        if NEG.search(pre) or pre.endswith('不'): status='negated'
        elif ATT.search(pre): status='negated' if FAIL.search(t) else 'goal'
        else: status='affirmed'
    in_rvc=any(m.start()>0 and (re.match(f'[{V}]',t[m.start()-1]) or t[max(0,m.start()-3):m.start()].endswith('mie') or (m.start()>1 and t[m.start()-1] in '得不' and re.match(f'[{V}]',t[m.start()-2]))) for m in res)
    spans=[mm.span() for mm in rvc_re.finditer(t)]
    in_rvc = in_rvc or any(a<=m.start()<=b+2 for m in res for a,b in spans)
    act=bool(act_re.search(t))
    return rvc,res_m,status,in_rvc,act
rows=[]
for (sid,video),d in p.groupby(['ID','video'],sort=False):
    desc='；'.join(d.desc)
    pair=vmap[video][0]
    rvc,res_m,status,in_rvc,act=code(desc,pair)
    ev=d.Event.iloc[0]
    if res_m and in_rvc: cat='RVC'
    elif res_m and act: cat='separate'
    elif res_m: cat='result_only'
    elif act: cat='action_only'
    else: cat='neither'
    rows.append(dict(subj='P'+str(sid),age={0:'adult',1:'4yo',2:'5yo'}[d.AgeGroup.iloc[0]],list=d.List.iloc[0],video=video,pair=pair,assoc=vmap[video][1],
        result='full' if ev==0 else 'zero',desc=desc,rvc=int(rvc),target=int(res_m),target_neg=int(status=='negated'),target_aff=int(status=='affirmed'),target_goal=int(status=='goal'),target_status=status,action=int(act),category=cat,
        old_predicate_rvc=int((d.Predicate==1).any())))
pr=pd.DataFrame(rows); pr['item']='P'+pr.pair.astype(str)+'_'+pr.assoc
pr.to_csv('prod.csv',index=False)
print('prod trials',len(pr), pr.groupby('age').subj.nunique().to_dict())
print(pd.crosstab([pr.age,pr.result],pr.category))
print(pr.groupby(['age','result'])[['rvc','target','target_aff','target_neg','target_goal','old_predicate_rvc']].mean().round(3))
fl=pd.read_excel(X,sheet_name='Filler')
fi=fl.groupby('ID').agg(ag=('age_group','first'),g=('gender','first'),m=('months','first'))
for a,d in fi.groupby('ag'):
    print('EXP2',a,len(d),'female',int((d.g==1).sum()),'range',ym(d.m.min()),ym(d.m.max()),'M',ym(d.m.mean()),round(d.m.mean()/12,2))
