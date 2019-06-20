#!/usr/bin/env python

import sys
import haproxy_settings as config
from get_haproxy_statistics import get_statistics_from_url as get_haproxy_statistics

def check_haproxy_backend_health(statistics_rows):
    
    backend_ok = []
    backend_not_ok = []
    
    for row in statistics_rows:
        if row['svname'] != 'BACKEND' and row['svname'] != 'localhost' and row['svname'] != 'FRONTEND':
            if row.get('check_status') == 'L4OK':
                backend_ok.append(row.get('svname'))
            elif (row.get('check_status') == 'L7OK' or row.get('check_status') == '* L7OK') and row.get('check_code') in ["200", "301", "302"]:
                backend_ok.append(row.get('svname'))
            else:
                backend_not_ok.append(row.get('svname'))

    # Critical if any backend has failed
    if len(backend_not_ok) != 0:
        print "Backends not ok: [%s]" % ', '.join(map(str, backend_not_ok))
        exit_code = 2
    else:
        print "All backends OK!"
        exit_code = 0
             
    return exit_code

output = get_haproxy_statistics(config.haproxy_url, config.auth_user, config.auth_password)
exit_code = check_haproxy_backend_health(output)

sys.exit(exit_code)
