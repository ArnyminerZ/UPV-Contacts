import logging

from selenium.webdriver.common.by import By

from Browser import Browser
from error.LoginException import LoginException

logger = logging.getLogger(__name__)

auth_url = "https://intranet.upv.es/pls/soalu/est_intranet.Ni_portal_n"


class Auth:
    def __init__(self, browser: Browser):
        """
        This class is used to authenticate the user in the intranet.
        :param browser: The browser to use to authenticate the user
        """
        self._browser = browser
        self._tdp: dict | None = None

    def login(self, dni: str, password: str, tipo: str = 'alumno'):
        """
        This function logs in the user to the intranet
        :param dni: The user's DNI
        :param password: The user's password
        :param tipo: The type of login to use. Options: alumno, personal, externo
        :return: The cookie with the session information. Keys: ǹame, value, path, domain, secure, httpOnly, sameSite
        """

        # initializing webdriver
        driver = self._browser.create(auth_url)

        # Find the login form
        logger.debug("Finding login form")
        form = driver.find_element(By.ID, tipo)

        # Introduce the DNI and password
        logger.debug("Introducing DNI and password")
        form.find_element(By.NAME, 'dni').send_keys(dni)
        form.find_element(By.NAME, 'clau').send_keys(password)

        # Submit the form
        logger.debug("Submitting form")
        form.find_element(By.CLASS_NAME, 'upv_btsubmit').click()

        # Get the cookies
        cookie = driver.get_cookie('TDp')
        if cookie is None:
            logger.error("Error logging in")
            raise LoginException()
        self._tdp = cookie

        return cookie

    def get_tdp(self):
        """
        Returns the cookie with the session information
        :return: The cookie with the session information. Keys: ǹame, value, path, domain, secure, httpOnly, sameSite
        """
        return self._tdp
