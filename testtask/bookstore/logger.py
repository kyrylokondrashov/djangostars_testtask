import re, logging
from django.conf import settings
from django.core.handlers.wsgi import STATUS_CODE_TEXT


req_handler = logging.FileHandler(settings.HOME_DIR + '/logs/requests.log')
req_handler.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] %(message)s')
req_handler.setFormatter(formatter)

req_log = logging.getLogger('requests')
req_log.propagate = False
req_log.addHandler(req_handler)


def log_cond(request):
    return re.search(r'^$', request.path)


class HeadersLoggingMiddleware(object):
    def process_response(self, request, response):
        if log_cond(request):
            keys = sorted(filter(lambda k: re.match(r'(HTTP_|CONTENT_)', k), request.META))
            keys = ['REMOTE_ADDR'] + keys
            meta = ''.join("%s=%s\n" % (k, request.META[k]) for k in keys)

            try:
                status_text = STATUS_CODE_TEXT[response.status_code]
            except KeyError:
                status_text = 'UNKNOWN STATUS CODE'
            status = '%s %s' % (response.status_code, status_text)
            response_headers = [(str(k), str(v)) for k, v in response.items()]
            for c in response.cookies.values():
                response_headers.append(('Set-Cookie', str(c.output(header=''))))
            headers = ''.join("%s: %s\n" % c for c in response_headers)
            req_log.info('"%s %s\n%s\n%s\n%s' % (request.method, request.build_absolute_uri(), meta,
                                                 status, headers))
        return response
