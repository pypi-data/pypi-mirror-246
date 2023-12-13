# Based on https://www.djangosnippets.org/snippets/186/

import cProfile
import os
import subprocess
import sys
from io import StringIO
from pathlib import Path
from tempfile import NamedTemporaryFile

from django.http import StreamingHttpResponse

from iommi._web_compat import HttpResponse
from ._web_compat import settings

MEDIA_PREFIXES = ['/static/']

_dot_search_paths = [
    '/usr/bin/dot',
    '/usr/local/bin/dot',
]


def get_dot_path():
    for p in _dot_search_paths:
        if os.path.exists(p):
            return p
    return None


def should_profile(request):
    disabled = getattr(request, 'profiler_disabled', True)
    is_staff = hasattr(request, 'user') and request.user.is_staff

    return ('_iommi_prof' in request.GET or '_iommi_prof' in request.POST) and ((not disabled and is_staff) or settings.DEBUG)


class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Disable profiling early on /media requests since touching request.user will add a
        # "Vary: Cookie" header to the response.
        request.profiler_disabled = False
        for prefix in MEDIA_PREFIXES:
            if request.path.startswith(prefix):
                request.profiler_disabled = True
                break

        if should_profile(request):
            prof = cProfile.Profile()
            prof.enable()
            request._iommi_prof = [prof]
        else:
            request._iommi_prof = []

        response = self.get_response(request)

        if request._iommi_prof:
            if isinstance(response, StreamingHttpResponse):
                # consume the entire streaming response, redirecting to stdout
                for line in response.streaming_content:
                    print(line.decode(), file=sys.__stdout__)

            response = HttpResponse()
            for prof in request._iommi_prof:
                prof.disable()

            import pstats

            s = StringIO()
            ps = pstats.Stats(*request._iommi_prof, stream=s)

            prof_command = request.GET.get('_iommi_prof')

            if prof_command == 'graph':
                with NamedTemporaryFile() as stats_dump:
                    ps.stream = stats_dump
                    ps.dump_stats(stats_dump.name)

                    gprof2dot_path = Path(sys.executable).parent / 'gprof2dot'
                    if not gprof2dot_path.exists():
                        raise Exception('gprof2dot not found. Please install it to use the graph feature.')

                    with subprocess.Popen(
                        (sys.executable, gprof2dot_path, '-f', 'pstats', stats_dump.name), stdout=subprocess.PIPE
                    ) as gprof2dot:

                        response['Content-Type'] = 'image/svg+xml'

                        dot_path = get_dot_path()
                        if dot_path:
                            response.content = subprocess.check_output((dot_path, '-Tsvg'), stdin=gprof2dot.stdout)
                        else:
                            response['Content-Type'] = 'text/plain'
                            response['Content-Disposition'] = "attachment; filename=gprof2dot-graph.txt"
                            response.content = subprocess.check_output('tee', stdin=gprof2dot.stdout)

                        gprof2dot.wait()

            elif prof_command == 'snake':
                # noinspection PyPackageRequirements
                try:
                    import snakeviz  # noqa
                except ImportError:
                    return HttpResponse('You must `pip install snakeviz` to use this feature')

                with NamedTemporaryFile() as stats_dump:
                    ps.stream = stats_dump
                    ps.dump_stats(stats_dump.name)

                    subprocess.Popen(
                        [sys.executable, str(Path(sys.executable).parent / 'snakeviz'), stats_dump.name],
                        stdin=None,
                        stdout=None,
                        stderr=None,
                    )

                    # We need to wait a bit to give snakeviz time to read the file
                    from time import sleep

                    sleep(3)

                return HttpResponse(
                    'You should have gotten a new browser window with snakeviz opened to the profile data'
                )

            else:
                ps = ps.sort_stats(prof_command or 'cumulative')
                ps.print_stats()

                stats_str = s.getvalue()

                limit = 280
                result = []

                def strip_extra_path(s, token):
                    if token not in s:
                        return s
                    pre, _, post = s.rpartition(' ')
                    post = post[post.rindex(token) + len(token) :]
                    return f'{pre} {post}'

                base_dir = str(settings.BASE_DIR)
                for line in stats_str.split("\n")[:limit]:
                    should_bold = base_dir in line and '/site-packages/' not in line
                    line = line.replace(base_dir, '')
                    line = strip_extra_path(line, '/site-packages')
                    line = strip_extra_path(line, '/Python.framework/Versions')
                    if should_bold:
                        line = f'<b>{line}</b>'

                    line = line.replace(' ', '&nbsp;')
                    result.append(line)

                # language=html
                start_html = '''
                    <style>
                        html {
                            font-family: monospace;
                            white-space: nowrap;
                        }

                        @media (prefers-color-scheme: dark) {
                            html {
                                background-color: black;
                                color: #bbb;
                            }
                            b {
                                color: white;
                            }
                        }
                    </style>

                    <div>
                        <a href="?_iommi_prof=graph">graph</a>
                        <a href="?_iommi_prof=snake">snakeviz</a>
                    </div>

                    <div>
                '''
                lines_html = "<br />\n".join(result)
                end_html = '</div>'

                response.content = start_html + lines_html + end_html

                response['Content-Type'] = 'text/html'

        return response
