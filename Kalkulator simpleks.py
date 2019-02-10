import numpy as np
import pandas as pd
#1
Fc = [30,20]
Fc = np.array(Fc)
#2
tar = 'Min'
#3
W1 = np.array([2,1])
W2 = np.array([3,3])
W3 = np.array([1.5,0])
#4
LWO = 3
#5
sr = np.row_stack((W1, W2, W3))
#6
Ps = np.array([1000,2400,600])
#7
WN = ['<=', '<=','<=']
#8
mli=1000
#9
CTS='Yes'
######################################################################################################################################################################

Ps = np.float32(Ps)
cb = np.zeros((LWO, 1))
WN = np.array(WN)
for c in range(0, LWO):
    if WN[c] == '<=':
        e = np.zeros((LWO, 1))
        e[c] = 1
        sr = np.column_stack((sr, e))
        Fc = np.append(Fc, 0)
        cb[c] = 0
    elif WN[c] == '=':
        e = np.zeros((LWO, 1))
        e[c] = 1
        sr = np.column_stack((sr, e))
    elif WN[c] == '>=':
        f = np.zeros((LWO, 1))
        f[c] = -1
        sr = np.column_stack((sr, f))
        Fc = np.append(Fc, 0)

for d in range(0, LWO):
    if WN[d] == '=':
        if tar == 'Max':
            cb[d] = -1e100
            Fc = np.append(Fc, -1000000000)
        elif tar == 'Min':
            cb[d] = 1e100
            Fc = np.append(Fc, 1000000000)
    if WN[d] == '>=':
        e = np.zeros((LWO, 1))
        e[d] = 1
        sr = np.column_stack((sr, e))
        if tar == 'Max':
            cb[d] = -1e100
            Fc = np.append(Fc, -1000000000)
        elif tar == 'Min':
            cb[d] = 1e100
            Fc = np.append(Fc, 1000000000)

z = cb * sr
z = np.sum(z, axis=0)
cz = Fc - z
Mi = np.zeros((LWO, 1))

for j in range(0, np.ma.size(cz)):
    if tar == 'Max' and cz[j] == np.max(cz) or tar == 'Min' and cz[j] == np.min(cz):
        for m in range(0, np.ma.size(Ps)):
            if sr[m][j] == 0:
                Mi[m][0] = 10000000000000000000
            else:
                Mi[m][0] = Ps[m] / sr[m][j]
    if tar == 'Max' and cz[j] == np.max(cz) or tar == 'Min' and cz[j] == np.min(cz):
        break

for w in range(mli):
    for n in range(0, LWO):
        if Mi[n][0] == np.min(Mi) and Mi[n][0] >= 0:
            for m in range(0, LWO):
                if m == n:
                    Ps[n] = Ps[n] / sr[n][j]
                    sr[n] = sr[n] / sr[n][j]
            break

    for n in range(0, LWO):
        if Mi[n, 0] == np.min(Mi) and Mi[n, 0] >= 0:
            for m in range(0, LWO):
                if m == n:
                    continue
                Ps[m] = Ps[m] - sr[m][j] * Ps[n]

    for n in range(0, LWO):
        if Mi[n, 0] == np.min(Mi) and Mi[n, 0] >= 0:
            for m in range(0, LWO):
                if m == n:
                    continue
                sr[m] = sr[m] - sr[m][j] * sr[n]
            break

    for k in range(0, np.ma.count(Fc)):
        for m in range(0, LWO):
            if sr[m][k] == 1:
                if np.count_nonzero(sr[:, k] == 0) == LWO - 1:
                    cb[m] = Fc[k]

    z = cb * sr
    z = np.sum(z, axis=0)
    cz = Fc - z
    true = np.full((1, np.ma.count(cz)), True)
    STOP = np.zeros((1, np.ma.count(cz)))

    for a in range(0, np.ma.count(cz)):
        if tar == 'Min' and cz[a] >= 0 or tar == 'Max' and cz[a] <= 0:
            STOP[0][a] = True
        else:
            STOP[0][a] = False

    if np.sum(STOP) == np.ma.count(STOP):
        if w == mli - 1:
            print('Iteration limit has been reached', (mli - 1),
                  '. If you want to change itertions limit change value of mli variable (line no 91).')
        elif w == 0:
            print('Optimal solution has been received after', 1, 'iteration.')
        else:
            print('Optimal solution has been received after', w + 1, 'iterations')
        break


    for j in range(0, np.ma.size(cz)):
        if tar == 'Max' and cz[j] == np.max(cz) or tar == 'Min' and cz[j] == np.min(cz):
            for m in range(0, np.ma.size(Ps)):
                if sr[m][j] == 0:
                    Mi[m][0] = 10000000000000000000
                else:
                    Mi[m][0] = Ps[m] / sr[m][j]
        if tar == 'Max' and cz[j] == np.max(cz) or tar == 'Min' and cz[j] == np.min(cz):
            break

    for t in range(0, np.ma.count(Mi)):
        if Mi[t] <= 0:
            Mi[t] = 1.e+100


d={}
p=[]
for x in range(1,np.ma.count(Fc)+1):
   d['x{}'.format(x)]=x
d=list(d)

p=[]
for row in range(len(sr)):
    for col in range(len(sr[0])):
        if sr[row,col]==1:
            if sr.astype(bool)[:,col].sum()==1:
                p.append('{}'.format(d[col]))


sr=pd.DataFrame(sr,columns=d,index=p)
Fc=list(Fc)
Fc=pd.DataFrame(Fc,columns=['Obj. f.'],index=d)
Fc=pd.DataFrame.transpose(Fc)
sr=Fc.append([sr])
Ps=pd.DataFrame(Ps,index=p,columns=['Solutions'])
pd.DataFrame.transpose(Ps)
sr=pd.concat([Ps,sr],axis=1,sort=False)
cb=pd.DataFrame(cb,index=p,columns=['cb'])
sr=pd.concat([cb,sr],axis=1,sort=False)
z=pd.DataFrame(z,index=d,columns=['zj'])
z=z.transpose()
sr=sr.append([z])
cz=pd.DataFrame(cz,index=d,columns=['cj-zj'])
cz=cz.transpose()
sr=sr.append([cz])
Wfc=sr.Solutions*sr.cb
Wfc=Wfc.sum()
sr=sr.fillna('')
if CTS=='Yes':
    pd.set_option('display.float_format', lambda x: '%.4f' % x)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(sr)
else:
    pd.set_option('display.float_format', lambda x: '%.4f' % x)
    print(sr)
print('Objective function value =',Wfc)