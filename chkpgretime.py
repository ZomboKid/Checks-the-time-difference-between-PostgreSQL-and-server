#! /usr/bin/python

import sys, psycopg2, datetime

FMT = '%Y-%m-%d %H:%M:%S'#time and data format
trigger=int(sys.argv[1]) #set max time difference in seconds
db_host=str(sys.argv[2])
db_port=str(sys.argv[3])
db_user=str(sys.argv[4])
db_password=str(sys.argv[5])
db_name=str(sys.argv[6])
#Example: ./chkpgretime.py 100 127.0.0.1 5432 user pass db
#---------------------------------------------------------------------
def f_connect_cursor_postgre():
    connection_string = "dbname=%s user=%s password=%s host=%s port=%s" % (db_name,db_user,db_password,db_host,db_port)
    try:
        conn=psycopg2.connect(connection_string)
        cursor=conn.cursor()
        return cursor
    except Exception as error:
        print error.__class__.__name__
#---------------------------------------------------------------------
def f_get_time_iside_postgre():
    cursor=f_connect_cursor_postgre()
    cursor.execute("SELECT NOW();")
    result=cursor.fetchone()
    time_inside_postgre=datetime.datetime.strptime(result[0].strftime('%Y-%m-%d %H:%M:%S'), FMT)
    return time_inside_postgre
#---------------------------------------------------------------------
def f_get_time_on_host():
    time_on_host= datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), FMT)
    return time_on_host
#---------------------------------------------------------------------
def f_chktime():

    time_inside_postgre=f_get_time_iside_postgre()
    time_on_host=f_get_time_on_host()

    tdelta = time_inside_postgre - time_on_host
    if tdelta.days < 0:
        tdelta = time_on_host - time_inside_postgre
    if tdelta.seconds > trigger:
        print >> sys.stderr, "ERROR - timedelta %i sec between Postgre and host is bigger than max time difference in %i sec" %(tdelta.seconds, trigger)
        sys.exit(1)
#---------------------------------------------------------------------
if __name__=="__main__":
    f_chktime()
