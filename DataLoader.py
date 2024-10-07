import hashlib
from typing import Tuple

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from Cache import Cache
from auth import Auth, logger
from Browser import Browser
from data.Profesor import Profesor

teachers_url = 'https://intranet.upv.es/pls/soalu/sic_asi.Profes_TemaAlu_Asi?p_vista=intranet'


class DataLoader:
    def __init__(self, browser: Browser, auth: Auth):
        self._browser = browser
        self._auth = auth
        self._cache = Cache('profesores')

    def get_teachers(self) -> [Tuple[str, str]]:
        driver = self._browser.create(teachers_url)
        driver.add_cookie(self._auth.get_tdp())

        m = hashlib.sha256()

        enlaces = []
        bodies = driver.find_elements(By.TAG_NAME, 'tbody')
        for body in bodies:
            rows = body.find_elements(By.TAG_NAME, 'tr')
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, 'td')
                link = cells[0].find_element(By.TAG_NAME, 'a')

                href = link.get_attribute('href')
                text = link.text

                m.update(text.encode(encoding="utf-8"))

                enlaces.append((m.hexdigest(), href))

        return enlaces

    def get_teacher(self, uuid: str, url: str) -> Profesor:
        cached_teachers = self._cache.read()
        for teacher in cached_teachers:
            if teacher['id'] == uuid:
                logger.info("Profesor encontrado en cache")
                return Profesor(
                    teacher['id'],
                    teacher['nombre'],
                    teacher['email'],
                    teacher['centro'],
                    teacher['departamento'],
                    teacher['categoria'],
                    teacher['investigacion'],
                    teacher['direccion'],
                    teacher['telefono']
                )

        driver = self._browser.create(url)

        nombre = driver.find_element(By.CLASS_NAME, 'upv_sicpernombre').text
        email = driver.find_elements(By.CLASS_NAME, 'upv_sicperlink')[0].text

        entries = dict()
        rows = driver.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            try:
                key = row.find_element(By.TAG_NAME, 'th').text
                value = row.find_element(By.TAG_NAME, 'td').text
                entries[key] = value
            except NoSuchElementException:
                pass

        profesor = Profesor(
            uuid,
            nombre,
            email,
            entries.get('Centro'),
            entries.get('Departamento'),
            entries.get('Categoría'),
            entries.get('Investigación'),
            entries.get('Dirección postal'),
            entries.get('Teléfono')
        )

        cached_teachers.append(profesor.dict())
        self._cache.write(cached_teachers)

        return profesor
