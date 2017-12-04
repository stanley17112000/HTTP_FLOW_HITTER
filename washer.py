import requests
import random
import json
import time
from requests import exceptions
from threading import Thread

#put the target url link, using http get
target_url = "[YOUR URL HERE]"

# proxy will be removed after X requests
proxy_use_limit = 10

#request time
min_request_time = 5
max_request_time = 15

# update proxy time in seconds
min_proxy_request_time = 3 * 60
max_proxy_request_time = 10 * 60

# config method [1,2], different proxy sources
config_method = 2



# should not modify below area
#============================================================
get_proxy_url1 = "https://api.getproxylist.com/proxy"
get_proxy_url2 = "http://pubproxy.com/api/proxy?limit=5&country=TW,JP,CN&format=txt&http=true&type=http"
query_cnt = 0
ip_list = []
duplicated_proxy = {}


#===========================================================

def UpdateProxyThread():
    global ip_list
    global get_proxy_url
    global config_method
    global min_proxy_request_time
    global max_proxy_request_time
    while True:


        if config_method == 1:
            r = requests.get( get_proxy_url1 )
            print r.text
            proxy_info = json.loads( r.text )
            ip_port = str(proxy_info['ip']) + ":" + str ( proxy_info['port'] )
            ip_ports = [ip_port]
        
        elif config_method == 2:
            r = requests.get( get_proxy_url2 )
            print r.text
            ip_ports = str( r.text ).split( '\n' )
        
        for ip_port in ip_ports:
            if ip_port not in ip_list:
                ip_list.append( ip_port )
                print ( "New Added Proxy IP : {}".format( ip_port ) )

        wait_time = random.randrange( min_proxy_request_time , max_proxy_request_time )
        time.sleep( wait_time )


    return

def QueryThread():
    global ip_list
    global query_cnt
    global duplicated_proxy
    while True:
        wait_time = random.randrange( min_request_time , max_request_time )
        print ( "waiting to make {} requests ..... (wait {} sec)".format( query_cnt+1, wait_time ) )
        time.sleep( wait_time )
        proxyCnt = len( ip_list )

        if proxyCnt > 0:
            random_select = random.randrange(0, proxyCnt )
            http_proxy = ip_list[ random_select ]
            if http_proxy in duplicated_proxy:
                if duplicated_proxy[http_proxy] > proxy_use_limit:
                    print ( "Remove proxy used too much {}".format( http_proxy ) )
                    ip_list.remove( http_proxy )
                    continue
                else:
                    duplicated_proxy[http_proxy] += 1
            else:
                duplicated_proxy[http_proxy] = 1

            proxy_dict = {
                  "http"  : http_proxy,
                  "https" : http_proxy,
                  "ftp"   : http_proxy
            }

            try:

                r = requests.get(target_url, proxies=proxy_dict, timeout=10)
                print( "Proxy : {}".format( http_proxy ) )
                print( "Request Success......" )
                query_cnt = query_cnt + 1
            except requests.ConnectionError:
                print ( 'Error : {}'.format( 'Connection Error' ) )
                print ( "Bad proxy {} is removed".format( http_proxy ) )
                ip_list.remove( http_proxy )
            except requests.Timeout:
                print ( 'Error : {}'.format( 'Request Timeout' ) )
                print ( "Bad proxy {} is removed".format( http_proxy ) )
                ip_list.remove( http_proxy )
            except Exception, e:
                print ( "Request Failed ...... " )
                print ( "Bad proxy {} is removed".format( http_proxy ) )
                ip_list.remove( http_proxy )


        else:
            print ( "Proxy Empty" )




    return

thread_update = Thread(target=UpdateProxyThread)
thread_query  = Thread(target=QueryThread)

thread_update.start()
thread_query.start()
