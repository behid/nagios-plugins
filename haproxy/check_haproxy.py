#!/usr/bin/env python

import csv
import requests
import sys

import haproxy_settings as config

def get_haproxy_statistics(url, user, password):
    r = requests.get(url, auth=(user, password))
    data = r.content.lstrip('# ')
    return csv.DictReader(data.splitlines())

def get_backend_health(statistics_rows):
    
    backend_ok = []
    backend_not_ok = []
    
    for row in statistics_rows:
        if row['svname'] != 'BACKEND' and row['svname']!= 'localhost' and row['svname'] != 'FRONTEND':

                if row.get('check_status') == "L7OK" and (row.get('check_code') == "200" or row.get('check_code') == "301"):
                    #print "Server: " + row.get('svname') + " OK, returned status code: " + row.get('check_code')
                    backend_ok.append(row.get('svname'))
                else:
                    #print "Server: " + row.get('svname') + " NOT OK, returned status code: " + row.get('check_code')
                    backend_not_ok.append(row.get('svname'))
        
    if len(backend_not_ok) != 0:
        print "Backends not ok: [%s]" % ', '.join(map(str, backend_not_ok))
        exit_code = 2
    else:
        print "All backends OK! [%s]" % ', '.join(map(str, backend_ok))
        exit_code = 0
            
            
    return exit_code

output = get_haproxy_statistics(config.haproxy_url, config.auth_user, config.auth_password)
exit_code = get_backend_health(output)

sys.exit(exit_code)
