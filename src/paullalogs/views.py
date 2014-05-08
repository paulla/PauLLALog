from pyramid.view import view_config
from datetime import datetime
from pyramid.httpexceptions import HTTPFound
import os
from pyramid.threadlocal import get_current_registry

import re

settings = get_current_registry().settings

_re_line = re.compile(settings['message_format'], re.VERBOSE)

@view_config(route_name='home')
def my_view(request):
    year = datetime.now().year
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime("%d")
    return HTTPFound(location=request.route_url('date',day = day, month = month, year = year))

@view_config(route_name='date', renderer='templates/template.pt')
def date_view(request):
    logs = []
    day = request.matchdict['day']
    month = request.matchdict['month']
    year = request.matchdict['year']
    date = '%s/%s/%s' % (day,month,year)
    path_log = settings['log_path']
    file_format = settings['file_format']
    if os.path.exists(path_log + file_format.format(year=year,month=month,day=day)):
        with open(path_log + file_format.format(year=year,month=month,day=day)) as f:
            for line in f.readlines():
                try:
                    match = _re_line.search(line.decode('utf-8','replace'))
                    if not match:
                        raise ValueError('Unhandled line %r' % line)
                    data = match.groupdict()
                    logs.append(data)
                except:
                    pass
        return {
                'logs': logs,
                'date': date,}
    else:
        return {'date' : date}
