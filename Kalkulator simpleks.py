import numpy as np
import pandas as pd

# Ponizszy kalkulator simpleksowy pozwala na rozwiazanie dowolnego programu liniowego.
# Przy uzupelnianiu ponizszych danych nalezy pamietac, ze wielkosc uzytych znakow ma znaczenie.
# Linijka pełna znakow '#' oznacza koniec strefy ustalania programu liniowego.
# Separatorem dziesietnym jest kropka.


# Współczynniki lewych stron f. celu i jej specyfikacja.
Fc = [1000,2400,600]
Fc = np.array(Fc)

# Max czy Min?
cel = 'Min'

# Lewe strony warunków ograniczających. Chcac dodac wiecej warunkow ograniczajacych nazelz dodac kolejne linijki wg formuly: 'Wx=np.array([]) gdzie w miejsce x
# należy wpisac numer warunku ograniczajacego, a w nawiasie kwadratowym po przecinku wspolczynniki lewych stron warunkow ograniczajacych.
W1 = np.array([2,3,1.5])
W2 = np.array([1,3,0])



# Liczba warunkow ograniczajacych. W linijce znajdujacej sie pod zmienna LWO nalezy rowniez po przecinku dopisac zmienne wg przykladowego schematu.
LWO = 2
sr = np.row_stack((W1, W2))

# Prawe strony warunków ograniczających
Ps = np.array([30,20])
Ps = np.float32(Ps)

# Kierunki nierówności (odpowiednio do kolejności warunków ograniczających)
WN = ['>=', '>=']

# Maksymalna mozliwa liczba iteracji (w konwencjonalnych przypadkach zadana wartosc powinna byc wystarczajaca)
mli=1000

# Czy pokazywac cale tablice simpleksowe? Zmniejsza czytelnosc przy duzej liczbie kolumn (Tak lub Nie).
CTS='Tak'

######################################################################################################################################################################


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
        if cel == 'Max':
            cb[d] = -1e100
            Fc = np.append(Fc, -1000000000)
        elif cel == 'Min':
            cb[d] = 1e100
            Fc = np.append(Fc, 1000000000)
    if WN[d] == '>=':
        e = np.zeros((LWO, 1))
        e[d] = 1
        sr = np.column_stack((sr, e))
        if cel == 'Max':
            cb[d] = -1e100
            Fc = np.append(Fc, -1000000000)
        elif cel == 'Min':
            cb[d] = 1e100
            Fc = np.append(Fc, 1000000000)

z = cb * sr
z = np.sum(z, axis=0)
cz = Fc - z
Mi = np.zeros((LWO, 1))

for j in range(0, np.ma.size(cz)):
    if cel == 'Max' and cz[j] == np.max(cz) or cel == 'Min' and cz[j] == np.min(cz):
        for m in range(0, np.ma.size(Ps)):
            if sr[m][j] == 0:
                Mi[m][0] = 10000000000000000000
            else:
                Mi[m][0] = Ps[m] / sr[m][j]
    if cel == 'Max' and cz[j] == np.max(cz) or cel == 'Min' and cz[j] == np.min(cz):
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
        if cel == 'Min' and cz[a] >= 0 or cel == 'Max' and cz[a] <= 0:
            STOP[0][a] = True
        else:
            STOP[0][a] = False

    if np.sum(STOP) == np.ma.count(STOP):
        if w == mli - 1:
            print('Osiagnieto maksymalna liczbe iteracji', (mli - 1),
                  '. Aby zmienic liczbe iteracji zmien wartosc zmiennej "mli" (linijka nr 91).')
        elif w == 0:
            print('Otrzymano rozwiązanie optymalne po', 1, 'iteracji.')
        else:
            print('Otrzymano rozwiązanie optymalne po', w + 1, 'iteracjach.')
        break


    for j in range(0, np.ma.size(cz)):
        if cel == 'Max' and cz[j] == np.max(cz) or cel == 'Min' and cz[j] == np.min(cz):
            for m in range(0, np.ma.size(Ps)):
                if sr[m][j] == 0:
                    Mi[m][0] = 10000000000000000000
                else:
                    Mi[m][0] = Ps[m] / sr[m][j]
        if cel == 'Max' and cz[j] == np.max(cz) or cel == 'Min' and cz[j] == np.min(cz):
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
Fc=pd.DataFrame(Fc,columns=['F.celu'],index=d)
Fc=pd.DataFrame.transpose(Fc)
sr=Fc.append([sr])
Ps=pd.DataFrame(Ps,index=p,columns=['Rozwiazania'])
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
Wfc=sr.Rozwiazania*sr.cb
Wfc=Wfc.sum()
sr=sr.fillna('')
if CTS=='Tak':
    pd.set_option('display.float_format', lambda x: '%.4f' % x)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(sr)
else:
    pd.set_option('display.float_format', lambda x: '%.4f' % x)
    print(sr)
print('Wartosc funkcji celu jest rowna',Wfc)