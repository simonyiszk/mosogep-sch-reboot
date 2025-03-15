# mosogep-sch-reboot
Mosogep.sch project reboot

Projekt dokumentáció: https://docs.google.com/document/d/1uoIA5JC5i7Pd-E8AlqeZ2zfmS9e4bSQlHUPqoVc_8NE/edit?tab=t.0

Mappaszerkezet:
- HW: a boardok tervrajzai
- FW: boardon futó firmware
- scripts: random scriptek amiket használtunk
- backend: itt van a backend kód
- frontend: itt van a frontend kód
- proxy: a proxy konfigurációja
- collector: a szerveroldali adatgyűjtés kódja

Az előtúrt fileokat eredeti formájukban az "eredeti" branchon találod.

Build & launch
- `git pull --recurse-submodules git@github.com:simonyiszk/mosogep-sch-reboot.git` VAGY `git submodule init && git submodule update` pull után
- `cp .env.dist .env`
- `.env`-ben ki kell tölteni a `BACKEND_SECRET_KEY`-t valami titkosra, illetve célszerű `ALLOWED_HOSTS`-ot localhosnak megfelelőre
- `docker-compose up`
- InfluxDB beállítás `localhost:8086`-on, bucket name célszerűen `statusch`, vagy `.env`-ben be kell állítani!
  Jó az elején kapott, minden joggal rendelkező token is (dev célra), vagy generáljunk a buckethez egy read/write tokent, és használjuk azt
- a `docker-compose`-t a `Ctrl+C`-vel megállít, majd újraindít (ismert hiba 'ContainerConfig', ekkor `docker-compose down` és utána up)


A backend a `8000`-es, a frontend a `3000`-es, az influx a `8086`-os porton fut. A `proxy` mappa Caddy konfigja kiproxyzza a frontendet és a backend API-t, ami dockerből automatikusan indul. Production-ben a Caddyfile-t át kell írni a megfelelő hostra.

Dev célra a leghasznosabb script a `scripts/fake_sender`, ami kamu adatokat küld az influxdb-be.
