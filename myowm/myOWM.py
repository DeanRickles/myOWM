import requests, psycopg
from datetime import datetime


def myOWM(lon, lat,APItoken, lang, units,
          vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Requirement:
            pip install psycopg-binary psycopg
        
        APItoken = '123456789123456789'
        lon   = '51.5133905'
        lat   = '-0.073925'
        lang  = 'en'
        units = 'metric'
        
        vServerIP   = IP address
        vServerPort = port
        vServerDB   = database name
        vServerTbl  = table name
        vServerUser = username
        vServerPass = password
    '''
    
    # loads the website
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={APItoken}&lang={lang}&units={units}')
    
    # load api data ito j
    j = r.json()
    
    # load datetime api loaded.
    vdatetime = r.headers.get('date')
    
    # no-longer need r.
    del r
    
    # Connect to the database.
    vConn = psycopg.connect(dbname=vServerDB,
                            user=vServerUser,
                            password=vServerPass,
                            host=vServerIP,
                            port=vServerPort)

    # set the autocommit behavior of the current session.
    vConn.autocommit = True

    with vConn:
         # Open a cursor to proform database operations.
        with vConn.cursor() as vCurr:
            
            #  Wind gust. Metric: meter/sec,
            try: gust = j['wind']['gust']
            except: gust = 0
            
            # volume for the last 1 hour, mm
            try:    rain1h = j['rain']['1h']
            except: rain1h = 0
            
            # volume for the last 3 hours, mm
            try:    rain3h = j['rain']['3h']
            except: rain3h = 0
            
            # Snow volume for the last 1 hour, mm
            try:    snow1h = j['snow']['1h']
            except: snow1h = 0
            
            # Snow volume for the last 3 hours, mm
            try:    snow3h = j['snow']['3h']
            except: snow3h = 0
            
            # Generate the insert query.
            insert_table_query = f'''insert into {vServerTbl} (
                datetime,
                timezone,
                lon,
                lat,
                sunrise_datetime,
                sunset_datetime,
                status,
                status_detailed,
                wind_speed,
                wind_degree,
                wind_gust,
                clouds,
                rain1h,
                rain3h,
                snow1h,
                snow3h,
                temp,
                feels_like,
                temp_min,
                temp_max,
                pressure,
                humidity,
                visibility
            )
            values(
            '%s', '%s', '%s', '%s', '%s',
            '%s', '%s', '%s', '%s', '%s',
            '%s', '%s', '%s', '%s', '%s',
            '%s', '%s', '%s', '%s', '%s',
            '%s', '%s', '%s'
            ); ''' % (
                vdatetime,
                j['timezone'],
                j['coord']['lon'],
                j['coord']['lat'],
                datetime.utcfromtimestamp(int(j['sys']['sunrise'])).strftime('%Y/%m/%d %H:%M:%S'),
                datetime.utcfromtimestamp(int(j['sys']['sunset'])).strftime('%Y/%m/%d %H:%M:%S'),
                j['weather'][0]['main'],
                j['weather'][0]['description'],
                j['wind']['speed'],
                j['wind']['deg'],
                gust,
                j['clouds']['all'],
                rain1h,
                rain3h,
                snow1h,
                snow3h,
                j['main']['temp'],
                j['main']['feels_like'],
                j['main']['temp_min'],
                j['main']['temp_max'],
                j['main']['pressure'],
                j['main']['humidity'],
                j['visibility']
            )
            
            vCurr.execute(insert_table_query)
            print(f"OWM on {vdatetime} imported.")
            
    del gust, rain1h, rain3h, snow1h, snow3h
    
    # Close conection to the database.
    vConn.close()


def create_myOWM_table(vServerIP, vServerPort, vServerDB, vServerTbl, vServerUser, vServerPass):
    '''
        Requirement:
            pip install psycopg-binary psycopg
        
        vServerIP   = IP address
        vServerPort = port
        vServerDB   = database name
        vServerTbl  = table name
        vServerUser = username
        vServerPass = password
    '''
    
    # Connect to the database.
    vConn = psycopg.connect(dbname=vServerDB,
                            user=vServerUser,
                            password=vServerPass,
                            host=vServerIP,
                            port=vServerPort)

    # set the autocommit behavior of the current session.
    vConn.autocommit = True

    with vConn:
         # Open a cursor to proform database operations.
        with vConn.cursor() as vCurr:
            
            # Generate the insert query.
            create_table_query = f'''CREATE TABLE {vServerTbl} (
                datetime TIMESTAMP,
                timezone NUMERIC,
                lon NUMERIC,
                lat NUMERIC,
                sunrise_datetime TIMESTAMP,
                sunset_datetime TIMESTAMP,
                status TEXT,
                status_detailed TEXT,
                wind_speed NUMERIC,
                wind_degree NUMERIC,
                wind_gust NUMERIC,
                clouds NUMERIC,
                rain1h NUMERIC,
                rain3h NUMERIC,
                snow1h NUMERIC,
                snow3h NUMERIC,
                temp NUMERIC,
                feels_like NUMERIC,
                temp_min NUMERIC,
                temp_max NUMERIC,
                pressure NUMERIC,
                humidity NUMERIC,
                visibility NUMERIC
            ) '''
            
            vCurr.execute(create_table_query)
    
    # Close conection to the database.
    vConn.close()

