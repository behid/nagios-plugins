#!/usr/bin/env python

import sys
import haproxy_settings as config

from get_haproxy_statistics import get_statistics_from_url as get_haproxy_statistics
from haproxy_helpers import percentage
from logging import critical

def check_haproxy_frontend_sessions(statistics_rows):
    
    frontend_sessions_ok = []
    frontend_sessions_not_ok = []
    ok = []
    warning = []
    critical = []
    
    for row in statistics_rows:
        if row['svname'] == 'FRONTEND' and row['pxname'] != 'monitoring':
            LIMIT = row.get('slim')
            CURRENT = row.get('scur')
            PERCENT = percentage(CURRENT, LIMIT)
            if PERCENT >= config.frontend_session_critical_limit:
                frontend_sessions_not_ok.append([row['pxname'], 'CRITICAL'])
            elif PERCENT >= config.frontend_session_warning_limit and PERCENT > config.frontend_session_critical_limit:
                frontend_sessions_not_ok.append([row['pxname'], 'WARNING'])
            else:
                frontend_sessions_ok.append(row['pxname'])

    if len(frontend_sessions_not_ok) != 0:
        
        for row in frontend_sessions_not_ok:
            if row[1] == 'CRITICAL':
                critical.append(row[0])
            elif row[1] == 'WARNING':
                warning.append(row[0])
        
    if len(critical) != 0 and len(warning) != 0:
        print "Frontend sessions CRITICAL for: [%s]! Frontend sessions WARNING for [%s]! Frontend sessions OK for: [%s]" % (', '.join(map(str, critical)), ', '.join(map(str, warning)), ', '.join(map(str, frontend_sessions_ok)))
        exit_code = 2
    elif len(critical) != 0 :
        print "Frontend sessions CRITICAL for: [%s]! Frontend sessions OK for: [%s]" % (', '.join(map(str, critical)), ', '.join(map(str, frontend_sessions_ok)))
        exit_code = 2
    elif len(warning) != 0 and len(critical) == 0:
        print "Frontend sessions WARNING for [%s]! Frontend sessions OK for: [%s]"
        exit_code = 1
    else:
        print "All frontends within limits!"
        exit_code = 0
             
    return exit_code

output = get_haproxy_statistics(config.haproxy_url, config.auth_user, config.auth_password)
exit_code = check_haproxy_frontend_sessions(output)

sys.exit(exit_code)