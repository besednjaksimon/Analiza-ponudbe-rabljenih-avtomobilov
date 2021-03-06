# Analiza ponudbe rabljenih avtomobilov

Analiziral bom 1000 rabljenih limuzin s spletne strani Avto.net:
https://www.avto.net/Ads/results.asp?znamka=&model=&modelID=&tip=&znamka2=&model2=&tip2=&znamka3=&model3=&tip3=&cenaMin=0&cenaMax=999999&letnikMin=0&letnikMax=2090&bencin=0&starost2=999&oblika=11&ccmMin=0&ccmMax=99999&mocMin=&mocMax=&kmMin=0&kmMax=9999999&kwMin=0&kwMax=999&motortakt=0&motorvalji=0&lokacija=0&sirina=0&dolzina=&dolzinaMIN=0&dolzinaMAX=100&nosilnostMIN=0&nosilnostMAX=999999&lezisc=&presek=0&premer=0&col=0&vijakov=0&vozilo=&airbag=&barva=&barvaint=&EQ1=1000000000&EQ2=1000000000&EQ3=1000000000&EQ4=100000000&EQ5=1000000000&EQ6=1000000000&EQ7=1000100020&EQ8=1010000001&EQ9=1000000000&KAT=1010000000&PIA=&PIAzero=&PSLO=&akcija=0&paketgarancije=&broker=0&prikazkategorije=0&kategorija=0&zaloga=10&arhiv=0&presort=3&tipsort=DESC&stran=1

## Za vsak avtomobil bom zajel:
  * znamko oz. ime,
  * letnik 1. registracije,
  * število prevoženih kilometrov,
  * tip motorja (bencinski ali diesel motor),
  * delovna prostornina v ccm,
  * moč motorja v kW,
  * tip menjalnika,
  * cena

## Delovne hipoteze oziroma vprašanja:
  * Katere znamke so najdražje?
  * Katere so najbolj zastopane na tržišču?
  * Ali se prodaja več nemških ali več francoskih avtomobilov? 
  * Kakšna je povezava med letnikom in ceno? Ali starejši avto res nujno implicira tudi nižjo ceno?
  * Kakšna je povezava med številom prevoženih kilometrov in ceno?
  * Ali so večji in močnejši avtomobili res dražji? Kaj se zgodi s ceno le teh, če jih gledamo na posamezno leto?
  * Kako se je skozi leta spreminjala popularnost bencinskih oziroma diesel motorjev?
  * Kakšen delež avtomobilov z avtomatskim menjalnikom se prodaja? A je ta delež skozi leta narastel?
  * Ali lahko samo z imenom znamke in letnikom avtomobila okvirno ocenimo njegovo ceno? Ali potrebujemo še kakšen dodaten podatek?

## Datoteke in pridobljeni podatki
  * Datoteka `orodja.py` vsebuje pomožne funkcije za shranjevanje podatkov s spletnih strani.
  * Z datoteko `zajem.py` sem zajel spletne strani in jih shranil v mapo `zajeti-podatki`, iz shranjenih strani sem izluščil potrebne podatke in jih zapisal tako v `csv` kot tudi v `json` formatu.
  * Ti dve datoteki (`avtomobili.csv` oz. `avtomobili.json`) se nahajata v mapi `obdelani-podatki`.
  * Pri datoteki `avtomobili.csv` sem znak "è" zamenjal s "č" in malenkostno spremenil imena kategorij. Vse te spremembe sem shranil v datoteki `avtomobili_pravi.csv`, ki sem jo nato uporabil pri analizi.
  * Analiza se nahaja v datoteki `analiza_avtomobilov.ipynb`.
  * Vsakemu avtomobilu pripada: 
    * identifikacijska številka, 
    * znamka, 
    * ime modela (oziroma krajši opis), 
    * letnik 1. registracije,
    * tip motorja, 
    * število prevoženih kilometrov, 
    * delovna prostornina motorja v ccm, 
    * moč motorja v kW, 
    * tip menjalnika,
    * cena.
  * Pri nekaterih avtomobilih lahko manjkajo podatki o številu prevoženih kilometrov oziroma podatki o delovni prostornini.
  * Podatki so bili pridobljeni 3.11.2018 ob 15:50.
