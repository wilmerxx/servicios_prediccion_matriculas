from werkzeug.security import generate_password_hash, check_password_hash


class Ubicacion:
    """Clase base para representaciones geográficas como Provincia, Canton y Parroquia."""
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    def __repr__(self):
        return f"<{self.__class__.__name__}(codigo={self.codigo}, nombre={self.nombre})>"

    def to_dict(self):
        return {
            'codigo': self.codigo,
            'nombre': self.nombre
        }


class Provincia(Ubicacion):
    pass


class Canton(Ubicacion):
    pass


class Parroquia(Ubicacion):
    pass


class Usuario:
    """Clase que representa un usuario en el sistema."""
    def __init__(self, id, username, email, nombre, apellido, password, rol_id):
        self.id = id
        self.username = username
        self.email = email
        self.nombre = nombre
        self.apellido = apellido
        self._password = generate_password_hash(password)
        self.rol_id = rol_id

    def __repr__(self):
        return f"<Usuario(id={self.id}, username={self.username}, email={self.email}, " \
               f"nombre={self.nombre}, apellido={self.apellido}, rol_id={self.rol_id})>"

    @property
    def password(self):
        raise AttributeError("La contraseña no es accesible directamente.")

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'rol_id': self.rol_id
        }

class Prediccion:
    """Clase que representa una predicción de matrícula y datos asociados."""
    def __init__(self, id, periodo, zona, codprovincia, nombre_provincia, codcanton, nombre_canton,
                 codparroquia, nombre_parroquia, amie, tipoeducacion, niveleducacion, area,
                 regimenescolar, modalidad, jornada, docentesfemenino, docentesmasculino, totaldocentes,
                 estudiantesfemeninoterceranobach, estudiantesmasculinoterceranobach,
                 total_estudiantesterceranobach, estudiantesfemeninodesertoresterceranobach,
                 estudiantesmasculinodesertoresterceranobach, total_desertoresterceranobach,
                 estudiantesfemeninopromovidosterceranobach, estudiantesmasculinopromovidosterceranobach,
                 total_nopromovidosterceranobach, estudiantesfemeninonopromovidosterceranobach,
                 estudiantesmasculinonopromovidosterceranobach, total_promovidosterceranobach,
                 prediccion_promovidos, tasa_desercion, tasa_promocion,
                 proporcion_docentes_estudiante, proporcion_noactualizados, proporcion_nopromovidos):
        self.id = id
        self.periodo = periodo
        self.zona = zona
        self.codprovincia = codprovincia
        self.nombre_provincia = nombre_provincia
        self.codcanton = codcanton
        self.nombre_canton = nombre_canton
        self.codparroquia = codparroquia
        self.nombre_parroquia = nombre_parroquia
        self.amie = amie
        self.tipoeducacion = tipoeducacion
        self.niveleducacion = niveleducacion
        self.area = area
        self.regimenescolar = regimenescolar
        self.modalidad = modalidad
        self.jornada = jornada
        self.docentesfemenino = docentesfemenino
        self.docentesmasculino = docentesmasculino
        self.totaldocentes = totaldocentes
        self.estudiantesfemeninoterceranobach = estudiantesfemeninoterceranobach
        self.estudiantesmasculinoterceranobach = estudiantesmasculinoterceranobach
        self.total_estudiantesterceranobach = total_estudiantesterceranobach
        self.estudiantesfemeninodesertoresterceranobach = estudiantesfemeninodesertoresterceranobach
        self.estudiantesmasculinodesertoresterceranobach = estudiantesmasculinodesertoresterceranobach
        self.total_desertoresterceranobach = total_desertoresterceranobach
        self.estudiantesfemeninopromovidosterceranobach = estudiantesfemeninopromovidosterceranobach
        self.estudiantesmasculinopromovidosterceranobach = estudiantesmasculinopromovidosterceranobach
        self.total_nopromovidosterceranobach = total_nopromovidosterceranobach
        self.estudiantesfemeninonopromovidosterceranobach = estudiantesfemeninonopromovidosterceranobach
        self.estudiantesmasculinonopromovidosterceranobach = estudiantesmasculinonopromovidosterceranobach
        self.total_promovidosterceranobach = total_promovidosterceranobach
        self.prediccion_promovidos = prediccion_promovidos
        self.tasa_desercion = tasa_desercion
        self.tasa_promocion = tasa_promocion
        self.proporcion_docentes_estudiante = proporcion_docentes_estudiante
        self.proporcion_noactualizados = proporcion_noactualizados
        self.proporcion_nopromovidos = proporcion_nopromovidos

    def to_dict(self):
        return {
            'ID': self.id,
            'PERIODO': self.periodo,
            'ZONA': self.zona,
            'CODPROVINCIA': self.codprovincia,
            'NOMBRE_PROVINCIA': self.nombre_provincia,
            'CODCANTON': self.codcanton,
            'NOMBRE_CANTON': self.nombre_canton,
            'CODPARROQUIA': self.codparroquia,
            'NOMBRE_PARROQUIA': self.nombre_parroquia,
            'AMIE': self.amie,
            'TIPOEDUCACION': self.tipoeducacion,
            'NIVELEDUCACION': self.niveleducacion,
            'AREA': self.area,
            'REGIMENESCOLAR': self.regimenescolar,
            'MODALIDAD': self.modalidad,
            'JORNADA': self.jornada,
            'DOCENTESFEMENINO': self.docentesfemenino,
            'DOCENTESMASCULINO': self.docentesmasculino,
            'TOTALDOCENTES': self.totaldocentes,
            'ESTUDIANTESFEMENINOTERCERANOBACH': self.estudiantesfemeninoterceranobach,
            'ESTUDIANTESMASCULINOTERCERANOBACH': self.estudiantesmasculinoterceranobach,
            'TOTAL_ESTUDIANTESTERCERANOBACH': self.total_estudiantesterceranobach,
            'ESTUDIANTESFEMENINODESERTORESTERCERANOBACH': self.estudiantesfemeninodesertoresterceranobach,
            'ESTUDIANTESMASCULINODESERTORESTERCERANOBACH': self.estudiantesmasculinodesertoresterceranobach,
            'TOTAL_DESERTORESTERCERANOBACH': self.total_desertoresterceranobach,
            'ESTUDIANTESFEMENINOPROMOVIDOSTERCERANOBACH': self.estudiantesfemeninopromovidosterceranobach,
            'ESTUDIANTESMASCULINOPROMOVIDOSTERCERANOBACH': self.estudiantesmasculinopromovidosterceranobach,
            'TOTAL_NOPROMOVIDOSTERCERANOBACH': self.total_nopromovidosterceranobach,
            'ESTUDIANTESFEMENINONOPROMOVIDOSTERCERANOBACH': self.estudiantesfemeninonopromovidosterceranobach,
            'ESTUDIANTESMASCULINONOPROMOVIDOSTERCERANOBACH': self.estudiantesmasculinonopromovidosterceranobach,
            'TOTAL_PROMOVIDOSTERCERANOBACH': self.total_promovidosterceranobach,
            'PREDICCION_PROMOVIDOS': self.prediccion_promovidos,
            'TASA_DESERCION': self.tasa_desercion,
            'TASA_PROMOCION': self.tasa_promocion,
            'PROPORCION_DOCENTES_ESTUDIANTE': self.proporcion_docentes_estudiante,
            'PROPORCION_NOACTUALIZADOS': self.proporcion_noactualizados,
            'PROPORCION_NOPROMOVIDOS': self.proporcion_nopromovidos
        }
