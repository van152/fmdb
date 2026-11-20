import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel().astype(np.int64)
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel().astype(np.int64)
lat = np.ascontiguousarray(ms[:,160:164]).view('<f4').ravel()
lon = np.ascontiguousarray(ms[:,164:168]).view('<f4').ravel()
cap0 = u32(0)
# (name, lat, lon, published capacity, year opened/built)
KNOWN = [
 ("Vitality Stadium",50.7352,-1.8383,11364,1910),
 ("Villa Park",52.5091,-1.8848,42657,1897),
 ("Anfield",53.4308,-2.9608,61276,1884),
 ("Old Trafford",53.4631,-2.2913,74310,1910),
 ("Stamford Bridge",51.4816,-0.1910,40343,1877),
 ("Goodison Park",53.4388,-2.9663,39414,1892),
 ("Wembley Stadium",51.5560,-0.2796,90000,2007),
 ("Emirates Stadium",51.5551,-0.1085,60704,2006),
 ("Etihad Stadium",53.4831,-2.2004,53400,2002),
 ("Camp Nou",41.3809,2.1228,99354,1957),
 ("Santiago Bernabeu",40.4530,-3.6884,81044,1947),
 ("San Siro",45.4781,9.1240,75710,1926),
 ("Allianz Arena",48.2188,11.6247,75000,2005),
 ("Signal Iduna Park",51.4926,7.4518,81365,1974),
 ("Veltins-Arena",51.5546,7.0675,62271,2001),
 ("MHPArena",48.7922,9.2321,60449,1933),
 ("Olympiastadion Berlin",52.5147,13.2395,74649,1936),
 ("Stade de France",48.9244,2.3600,81338,1998),
 ("Parc des Princes",48.8414,2.2531,47926,1972),
 ("Johan Cruijff ArenA",52.3144,4.9420,55500,1996),
 ("Celtic Park",55.8493,-4.2052,60411,1892),
 ("Ibrox Stadium",55.8532,-4.3092,50817,1899),
 ("St James' Park",54.9755,-1.6216,52305,1892),
 ("Mestalla",39.4746,-0.3582,48600,1923),
 ("Estadio da Luz",38.7526,-9.1847,64642,2003),
 ("Estadio do Dragao",41.1620,-8.5837,50033,2003),
 ("Stadio Olimpico",41.9340,12.4548,70634,1937),
 ("Allianz Stadium",45.1100,7.6411,41507,2011),
 ("Stadio San Paolo",40.8280,14.1929,54726,1959),
 ("BayArena",51.0382,7.0023,30210,1958),
 ("Deutsche Bank Park",50.0687,8.6455,58000,1925),
 ("Red Bull Arena",51.3458,12.3483,47069,1956),
 ("Vodafone Park",41.0392,28.9948,42590,2016),
 ("Tottenham Hotspur Stadium",51.6043,-0.0665,62850,2019),
 ("Molineux",52.5904,-2.1303,31750,1889),
 ("Elland Road",53.7778,-1.5722,37790,1897),
 ("Hillsborough",53.4114,-1.5006,39732,1899),
 ("Riverside Stadium",54.5783,-1.2170,34742,1995),
 ("King Power Stadium",52.6204,-1.1422,32261,2002),
 ("St Mary's Stadium",50.9058,-1.3910,32384,2001),
 ("Selhurst Park",51.3983,-0.0855,25486,1924),
 ("Craven Cottage",51.4748,-0.2216,22384,1896),
 ("Bramall Lane",53.3703,-1.4708,32050,1855),
 ("Turf Moor",53.7890,-2.2302,21944,1883),
 ("Vicarage Road",51.6499,-0.4016,22200,1922),
 ("London Stadium",51.5387,-0.0166,62500,2012),
 ("Amex Stadium",50.8616,-0.0835,31800,2011),
 ("Vitality",50.7352,-1.8383,11364,1910),
]
dates = {'A':(37,39),'B':(41,43),'C':(45,47),'D':(131,133),'E':(135,137)}
rows=[]
for name, la, lo, pub, yr in KNOWN:
    m = (np.abs(lat-la)<0.003) & (np.abs(lon-lo)<0.005)
    idx = np.where(m)[0]
    if len(idx)==0: print('MISS', name); continue
    # choose the row with the largest capacity (the real stadium, not a youth pitch)
    j = idx[np.argmax(cap0[idx])]
    d = {k: (int(u16(dates[k][0])[j]), int(u16(dates[k][1])[j])) for k in dates}
    rows.append((name, pub, yr, int(cap0[j]), d, int(u32(8)[j]), int(u32(4)[j]), int(u32(12)[j]), int(u32(16)[j]), int(u32(21)[j])))
print(f'{"name":28s} {"pub":>7s} {"@0":>7s} {"@8":>7s} {"@4":>7s} {"@12":>7s} {"@16":>8s} {"@21":>7s} | A(yr) B(yr) C(yr) D(yr) E(yr) | opened')
okA=0
for name,pub,yr,c0,d,c8,c4,c12,c16,c21 in rows:
    flags = ''.join(('*' if d[k][1]==yr else '.') for k in 'ABCDE')
    if d['A'][1]==yr: okA+=1
    print(f'{name:28s} {pub:7d} {c0:7d} {c8:7d} {c4:7d} {c12:7d} {c16:8d} {c21:7d} | '
          + ' '.join(f'{d[k][1]:4d}' for k in 'ABCDE') + f' | {yr} {flags}')
print(f'\nA-year == published opening year: {okA}/{len(rows)}')
print('capacity @0 == published (exact):', sum(1 for r in rows if r[3]==r[1]), '/', len(rows))
print('capacity @0 within 3%:', sum(1 for r in rows if r[1] and abs(r[3]-r[1])/r[1]<0.03), '/', len(rows))
