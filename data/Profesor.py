import re


class Profesor:
    def __init__(self, id: str, fullname: str, email: str, centro: str | None, departamento: str | None,
                 categoria: str | None,
                 investigacion: str | None, direccion: str | None, telefono: str | None):
        self.id = id
        self.nombre = fullname
        self.email = email
        self.centro = centro
        self.departamento = departamento
        self.categoria = categoria
        self.investigacion = investigacion
        self.direccion = direccion
        self.telefono = telefono

    def get_fullname(self):
        pieces = self.nombre.split(',')
        return pieces[1].strip() + ' ' + pieces[0].strip()

    def _get_fullname_vcard(self):
        pieces = self.nombre.split(',')
        return pieces[1].strip() + ';' + ';'.join(pieces[0].split(' '))

    def get_email(self):
        """
        This function returns the email of the teacher.
        Since the HTML by default has the `@` separated by &nbsp; we need to remove it.
        :return:
        """
        # https://www.ascii-code.com/character/nbsp
        return self.email.replace('&nbsp;', '').replace('\u00a0', '').replace(' ', '')

    def get_phone(self) -> str | None:
        match = re.search(r"(\d+)", self.telefono)
        if match:
            return match.group(1)
        return None

    def get_ext(self) -> str | None:
        match = re.search(r"Ext\.:(\d+)", self.telefono)
        if match:
            return match.group(1)
        return None

    def dict(self) -> dict:
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.get_email(),
            'centro': self.centro,
            'departamento': self.departamento,
            'categoria': self.categoria,
            'investigacion': self.investigacion,
            'direccion': self.direccion,
            'telefono': self.telefono
        }

    def vcard(self) -> str:
        string = f"BEGIN:VCARD\n" \
                 f"VERSION:3.0\n" \
                 f"KIND:individual" \
                 f"UID:{self.id}"

        if self.nombre is not None:
            string += f"N:{self._get_fullname_vcard()}\n" \
                      f"FN:{self.get_fullname()}\n"

        string += "ORG:Universitat Politècnica de València"
        if self.centro is not None:
            string += f";{self.centro}"
        if self.departamento is not None:
            string += f";{self.departamento}"
        string += "\n"

        if self.email is not None:
            string += f"EMAIL:{self.get_email()}\n"

        if self.categoria is not None:
            string += f"TITLE:{self.categoria.replace('\n', ';')}\n"

        phone = self.get_phone()
        ext = self.get_ext()
        if phone is not None:
            string += f"TEL;VALUE=uri;PREF=1;TYPE=voice,work:tel:{phone}"
            if ext is not None:
                string += f";ext={ext}"
            string += "\n"

        if self.direccion is not None:
            string += f"ADR:{self.direccion.replace('\n', ';')}\n"

        string += f"END:VCARD\n"
        return string
