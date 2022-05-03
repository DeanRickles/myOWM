# myOWM

utilising the free api to pull weather data into postgress.

## todo:
- [x] get current weather forcast.
    - [ ] Add name of location for multipule api pulls for different locations.
- [ ] Forcasting data int sql.


#### muOWM example
```
# Variables
lat = '51.5072' # Latitude.
lon = '-0.1276' # longitude.
APItoken = '12345678901234567890123456789012' # open weather map API key.
lang = 'en' # language.
units = 'metric' # unit type.
vServerIP   = '192.168.1.199' # Postgress Server.
vServerPort = '5432' # Pogress port.
vServerDB   = 'DATABASE' # Database name.
vServerTbl  = 'OWMDATA'
vServerUser = 'username' # Username.
vServerPass = 'P@ssword'

owm.myOWM(lon, lat, APItoken, lang, units,
  vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass)
```