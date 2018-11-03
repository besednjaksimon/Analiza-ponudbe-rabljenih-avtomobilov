import re
import os
import orodja


##############################################################################

# REGULARNI IZRAZI


vzorec_bloka = re.compile(
    r'<div class="ResultsAd">.*?'
    r'<div class="ResultsAdLogo"',
    flags=re.DOTALL
)

vzorec_avtomobila = re.compile(
    r'<a class="Adlink" href="../Ads/details.asp\?id=(?P<id>\d+)&display.*?'
    r'<span>(?P<Model>.*?)</span>.*?'
    r'<li>Letnik 1.registracije:(?P<Letnik>\d{4})</li>.*?'
    r'<li>(?P<Tip_motorja>\D+?),.*?'
    r' (?P<kW>\d+) kW.*?'
    r'<li>(?P<Menjalnik>.+?)</li>.*?'
    r'<div class="ResultsAdPrice.*?'
    r'("AkcijaCena">|\t|Grey">)(?P<Cena>\d+\.{0,1}\d*).*?',
    flags=re.DOTALL
)

vzorec_ccm = re.compile(
    r' (?P<ccm>\d+) ccm,.*?',
    flags=re.DOTALL
)

vzorec_km = re.compile(
    r'<li>(?P<Prevozeni_km>\d+) km</li>.*?',
    flags=re.DOTALL
)


##############################################################################

##############################################################################

# OBDELAVA


avto_imenik = 'zajeti-podatki'


def read_file_to_string(directory, filename):
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as file_in:
        return file_in.read()


def stran_na_bloke(stran):
    '''Vrne seznam oglasov s strani.'''
    oglasi = re.findall(vzorec_bloka, stran)
    return oglasi


def izloci_podatke_oglasa(blok):
    '''Izloci slovar s podatki posameznega avtomobila.'''
    for izraz in vzorec_avtomobila.finditer(blok):
        oglas = izraz.groupdict()
    # Zabelezimo podatek o ccm, ce je omenjen
    ccm = vzorec_ccm.search(blok)
    if ccm:
        oglas['ccm'] = int(ccm['ccm'])
    else:
        oglas['ccm'] = None
    # Zabelezimo podatek o stevilu prevozenih kilometrov,
    # ce je omenjen
    km = vzorec_km.search(blok)
    if km:
        oglas['Prevozeni_km'] = int(km['Prevozeni_km'])
    else:
        oglas['Prevozeni_km'] = None
    # Prevedemo vse stevilke v tip int
    oglas['id'] = int(oglas['id'])
    oglas['Letnik'] = int(oglas['Letnik'])
    oglas['kW'] = int(oglas['kW'])
    oglas['Cena'] = int(oglas['Cena'].replace('.', ''))
    # Prva beseda v kljucu 'Model' je znamka avtomobila,
    # kar ostane v tem nizu, je ime modela (oz krajsi opis).
    # Zato dodamo kljuc 'Znamka', ki kot vrednost vsebuje prvo besedo
    # vrednosti kljuca 'Model', vrednost kljuca 'Model' pa nadomestimo
    # s tistim, kar ostane, ce odstranimo prvo besedo.
    oglas['Znamka'] = oglas['Model'].split()[0]
    oglas['Model'] = oglas['Model'].replace(oglas['Model'].split()[0], '')[1:]
    # Posebej je treba paziti pri znamki 'Alfa Romeo', kajti ime te znamke
    # se sestoji iz dveh besed. Zato postopek posebej v tem primeru
    # ponovimo:
    if oglas['Znamka'] == 'Alfa':
        oglas['Znamka'] = 'Alfa Romeo'
        oglas['Model'] = oglas['Model'].replace(
            oglas['Model'].split()[0], ''
        )[1:]
    return oglas

# Nemcija = ['Audi', 'BMW', 'Mercedes-Benz',
#           'Opel', 'Porsche', 'Volkswagen', 'Warthburg']
# Francija = ['Aixam', 'Citroen', 'JDM', 'Ligier',
#            'Microcar', 'Peugeot', 'Renault']


def oglasi_na_strani(st_strani):
    '''Vrne podatke oglasov s posamezne strani.'''
    url = (
        'https://www.avto.net/Ads/results.asp?znamka=&model=&'
        'modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&'
        'tip3=&cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090'
        '&bencin=0&starost2=999&oblika=11&ccmMin=0&ccmMax=99999'
        '&mocMin=&mocMax=&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999'
        '&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina='
        '&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999'
        '&lezisc=&presek=0&premer=0&col=0&vijakov=0&vozilo=&airbag=&'
        'barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000'
        '&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1000100020'
        '&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&'
        'PSLO=&akcija=0&paketgarancije=&broker=0&prikazkategorije=0&'
        'kategorija=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran={}'
    ).format(st_strani)
    ime_datoteke = 'zajeti-podatki/avtomobili-{}.html'.format(st_strani)
    # Posamezno stran shranimo:
    orodja.shrani_spletno_stran(url, ime_datoteke)
    ime_datoteke = 'avtomobili-{}.html'.format(st_strani)
    # Jo nato preberemo:
    vsebina = read_file_to_string(avto_imenik, ime_datoteke)
    # Jo razdelimo na bloke oglasov:
    oglasi = stran_na_bloke(vsebina)
    # Za vsak blok/oglas izlocimo podatke, ki jih potrebujemo.
    for i in range(0, len(oglasi)):
        yield izloci_podatke_oglasa(oglasi[i])


##############################################################################

##############################################################################

# IZVEDBA


vsi_oglasi = []
for st_strani in range(1, 22):
    for oglas in oglasi_na_strani(st_strani):
        vsi_oglasi.append(oglas)
vsi_oglasi.sort(key=lambda oglas: oglas['id'])
orodja.zapisi_json(vsi_oglasi, 'obdelani-podatki/avtomobili.json')
orodja.zapisi_csv(vsi_oglasi, ['id', 'Znamka', 'Model', 'Letnik',
                               'Tip_motorja', 'Prevozeni_km', 'ccm', 'kW',
                               'Menjalnik', 'Cena'],
                  'obdelani-podatki/avtomobili.csv')

##############################################################################
