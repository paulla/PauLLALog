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
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")
    channels = settings['channels']
    if '\n' in channels:
        channels = [chan for chan in channels.splitlines() if chan]
    return HTTPFound(
            location=request.route_url(
                'date',
                day = day, 
                month = month, 
                year = year, 
                channel = channels[0]))

@view_config(route_name='date', renderer='templates/template.pt')
def date_view(request):
    if request.method == 'POST':
        channel = request.POST['channel']
        return HTTPFound(
                location=request.route_url(
                    'date',
                    day = request.matchdict['day'], 
                    month = request.matchdict['month'], 
                    year = request.matchdict['year'], 
                    channel = channel))
    else:
        channel = request.matchdict['channel']
    logs = []
    day = request.matchdict['day']
    month = request.matchdict['month']
    year = request.matchdict['year']
    channels = settings['channels']
    if '\n' in channels:
        channels = [chan for chan in channels.splitlines() if chan]
    date = '%s/%s/%s' % (day,month,year)
    path_log = settings['log_path'].format(channel = '#%s' % channel, year=year,month=month,day=day)
    file_format = settings['file_format']
    log_file = os.path.join(path_log, file_format.format(channel = '#%s' % channel, year=year,month=month,day=day))
    if os.path.exists(log_file):
        with open(log_file) as f:
            for line in f.readlines():
                match = _re_line.search(line.decode('utf-8','replace'))
                if not match:
                    raise ValueError('Unhandled line %r' % line)
                data = match.groupdict()
                logs.append(data)
        return {
                'logs': logs,
                'date': date,
                'channel': channel,
                'channels' : channels}
    else:
        return {'date' : date,
                'channel':channel,
                'channels':channels}
