import base64
import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

from Browser import Browser
from DataLoader import DataLoader
from auth import Auth
from error.LoginException import LoginException

logger = logging.getLogger(__name__)


class WebServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm="Address Book Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'No auth header received'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            return

        try:
            auth_header: str = self.headers.get('Authorization')
            auth_header = auth_header.split(' ')[1]  # Remove Basic prefix
            print("auth_header: ", auth_header)
            decoded_header = base64.b64decode(auth_header).decode('utf-8').split(':')
            (username, password) = decoded_header

            self.send_response(200)
            self.send_header('Content-type', 'text/x-vcard')
            self.end_headers()

            self.wfile.write(bytes(self._load_vcard(username, password), 'utf-8'))
        except LoginException:
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {
                'success': False,
                'error': 'Login credentials wrong or invalid'
            }
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def _load_vcard(self, dni, password) -> str:
        browser = Browser()
        auth = Auth(browser)
        data_loader = DataLoader(browser, auth)

        token_cookie = auth.login(dni, password)
        print(f"Token cookie: {token_cookie.get('value')}")
        url_profesores = data_loader.get_teachers()
        print(f"Cargando datos de {len(url_profesores)} profesores")
        profesores = []
        for (uuid, url) in url_profesores:
            try:
                profesores.append(data_loader.get_teacher(uuid, url))
            except Exception as e:
                logger.error(f"Error getting teacher from URL: {url}")
                logger.error(e)

        browser.close()

        return ''.join((profesor.vcard() for profesor in profesores))


def serve(hostname: str = "0.0.0.0", port: int = 8080):
    webServer = HTTPServer((hostname, port), WebServer)
    print("Server started http://%s:%s" % (hostname, port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
