import logging
import os
from os import path

from DataLoader import DataLoader
from auth import Auth
from Browser import Browser


def run():
    if not path.exists('cache'):
        logging.info('Creating cache directory')
        os.mkdir('cache')

    browser = Browser()
    auth = Auth(browser)
    data_loader = DataLoader(browser, auth)

    token_cookie = auth.login('21698565', '7xVqPqiJBN6ueHtqb9GM')
    print(f"Token cookie: {token_cookie.get('value')}")
    url_profesores = data_loader.get_teachers()
    print(f"Cargando datos de {len(url_profesores)} profesores")
    profesores = []
    for (uuid, url) in url_profesores:
        try:
            profesores.append(data_loader.get_teacher(uuid, url))
        except Exception as e:
            logging.error(f"Error getting teacher from URL: {url}")
            logging.error(e)
    print(f"Cards:\n{''.join((profesor.vcard() for profesor in profesores))}")

    browser.close()

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    run()
