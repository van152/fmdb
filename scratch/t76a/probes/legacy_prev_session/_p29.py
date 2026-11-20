import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel()
lat = np.ascontiguousarray(ms[:, 160:164]).view('<f4').ravel()
lon = np.ascontiguousarray(ms[:, 164:168]).view('<f4').ravel()
KNOWN = [
 ("Signal Iduna Park",51.4926,7.4519),("Anfield",53.4308,-2.9609),("Etihad",53.4831,-2.2004),
 ("Emirates",51.5549,-0.1084),("Stamford Bridge",51.4817,-0.1910),("Allianz Arena",48.2188,11.6247),
 ("Parc des Princes",48.8414,2.2531),("Johan Cruijff ArenA",52.3143,4.9419),("Celtic Park",55.8497,-4.2055),
 ("Ibrox",55.8532,-4.3092),("St James Park",54.9756,-1.6217),("Villa Park",52.5092,-1.8847),
 ("Mestalla",39.4747,-0.3583),("Estadio da Luz",38.7527,-9.1848),("Dragao",41.1618,-8.5839),
 ("Stadio Olimpico",41.9339,12.4547),("Allianz Stadium Turin",45.1096,7.6411),("San Paolo",40.8280,14.1927),
 ("BayArena",51.0383,7.0024),("Veltins-Arena",51.5545,7.0676),("MHPArena",48.7923,9.2319),
 ("Deutsche Bank Park",50.0686,8.6455),("Red Bull Arena Leipzig",51.3458,12.3482),
 ("Olympiastadion Berlin",52.5147,13.2395),("Stade de France",48.9245,2.3601),
 ("Vodafone Park",41.0392,28.9942),("Ali Sami Yen",41.1030,28.9900),
]
for name, la, lo in KNOWN:
    m = (np.abs(lat-la)<0.004) & (np.abs(lon-lo)<0.006)
    for j in np.where(m)[0][:3]:
        print(f'{name:24s} row {j:6d} lat={lat[j]:.4f} lon={lon[j]:.4f} ' +
              ' '.join(f'@{o}={int(u32(o)[j])}' for o in (0,4,8,12,16,21)))
