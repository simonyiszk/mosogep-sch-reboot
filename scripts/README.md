# Mindenféle dev & debug scriptek

## CSV LOGGER
A legelső elkészült script, CSV-kompatibilis formába printeli a bejövő packeteket, timestampelve. Fileba irányítható.

## INFLUXDB UPLOADER
Setupolható egy telepített influxdb mellé, feltölti a bejövő adatokat. A tokeneket természetesen ki kell tölteni. A mellékelt serveice fileal futtatható.

## STATUS DISPLAY
Kijelzi a pillanatnyi állapotot 3 másodperces frissítéssel.

A kijelzett oszlopok:
- az emelet száma, színkódolva (lásd lentebb)
- a 3 másodperc alatt kapott csomagok száma
- a mosógép által adott mérések maximuma
- a szárító által adott mérések maximuma

Zölddel látszanak azok az emeletek, ahonnan kaptunk adatot, pirossal, ahonnan kellett volna de nem jött, és szürke ahonnan nem jött (nincs külön színkód ha nem kellett volna de kaptunk!).

Az emeletek adatai a `mosogep_data.py`-ban vannak

## COUNTER

Hosszabb ideig számolja a beérkezett csomagokat emelet szerint csoportosítva, majd kiírja az eredményt, illetve fileba is menti.

A program célja az FW-k összehangolása hogy azonos mintavételi sebességgel küldjék a csomagokat. Minden panel külön megmérhető közvetlenül is, illetve a központi szerveren futtatva a ténylegesen megkapott csomagszámokat látjuk (a hálózat esetlege hibáival együtt).

## FAKE SENDER

Kamu adatokat küld az 1-4 szintek nevében az influxdb-be, teszteléshez. Másfél percenként ki-be kapcsolgatja az összes gépet. A tokeneket természetesen ki kell tölteni.