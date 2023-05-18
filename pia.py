from PyQt5 import QtWidgets, uic, QtGui, QtCore
import mysql.connector
from PyQt5.QtGui import QMovie

# Conexión a la base de datos
connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='piavd'
)

id_usuario_actual = None


# Función para registrar un nuevo usuario
def registrar_usuario():
    nombre = ventana_registro.usuario.text()
    correo = ventana_registro.email.text()
    contraseña = ventana_registro.contrasena.text()

    cursor = connection.cursor()
    sql = "INSERT INTO usuario (nombre_usuario, correo, contrasena) VALUES (%s, %s, %s)"
    cursor.execute(sql, (nombre, correo, contraseña))
    connection.commit()

    ventana_registro.close()
    ventana_registro_exitoso.show()


# Función para iniciar sesión
def iniciar_sesion():
    global id_usuario_actual

    usuario = ventana_entrar.usuario.text()
    contraseña = ventana_entrar.contrasena.text()

    cursor = connection.cursor()
    sql = "SELECT * FROM usuario WHERE nombre_usuario = %s AND contrasena = %s"
    cursor.execute(sql, (usuario, contraseña))
    resultado = cursor.fetchone()

    if resultado:
        id_usuario_actual = resultado[0]
        ventana_entrar.close()
        ventana_menu.show()
        # Mostrar la ventana de reseñas o realizar cualquier otra acción
    else:
        ventana_entrar.close()
        ventana_error.show()


def abrir_ventana_resenas():
    ventana_resenas.show()


def abrir_ventana_favoritos():
    ventana_favoritos.show()


def abrir_ventana_salir():
    ventana_salir.show()


def abrir_ventana_resenas():
    ventana_resenas.show()

    # Realizar la consulta a la base de datos para obtener los registros de reseñas
    cursor = connection.cursor()
    sql = """
        SELECT u.nombre_usuario, r.titulo, r.genero, r.calificacion, r.texto
        FROM usuario u
        INNER JOIN resena r ON u.id_usuario = r.id_usuario
    """
    cursor.execute(sql)
    resultados = cursor.fetchall()

    # Configurar el QTableWidget
    ventana_resenas.tableWidget.setColumnCount(5)
    ventana_resenas.tableWidget.setHorizontalHeaderLabels(["Usuario", "Título", "Género", "Calificación", "Reseña"])
    ventana_resenas.tableWidget.setRowCount(len(resultados))

    # Insertar los datos en el QTableWidget
    for row, resultado in enumerate(resultados):
        for col, valor in enumerate(resultado):
            item = QtWidgets.QTableWidgetItem(str(valor))
            ventana_resenas.tableWidget.setItem(row, col, item)

    ventana_resenas.tableWidget.resizeColumnsToContents()


def abrir_ventana_resena_propia():
    ventana_resena_propia.show()


def guardar_resena():
    titulo = ventana_resena_propia.titulo.text()
    genero = ventana_resena_propia.genero.text()
    calificacion = ventana_resena_propia.calif.text()
    texto = ventana_resena_propia.resena.text()

    # Realizar la inserción en la base de datos
    cursor = connection.cursor()
    sql = "INSERT INTO resena (id_usuario, titulo, genero, calificacion, texto) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (id_usuario_actual, titulo, genero, calificacion, texto))
    connection.commit()

    ventana_guardado.show()


def regresandoamenuprincipal():
    ventana_guardado.close()
    ventana_resena_propia.close()
    ventana_resenas.close()
    ventana_menu.show()


def salir():
    app.exit()


# Configuración de las ventanas
app = QtWidgets.QApplication([])
ventana_bienvenida = uic.loadUi("ventana0.ui")
ventana_registro = uic.loadUi("ventana1.ui")
ventana_registro_exitoso = uic.loadUi("ventana1.5.ui")
ventana_entrar = uic.loadUi("ventana2.ui")
ventana_error = uic.loadUi("ventana3.ui")
ventana_menu = uic.loadUi("ventana4.ui")
ventana_resenas = uic.loadUi("ventana5.ui")
ventana_resena_propia = uic.loadUi("ventana6.ui")
ventana_guardado = uic.loadUi("ventana6.5.ui")
ventana_favoritos = uic.loadUi("ventana7.ui")
ventana_salir = uic.loadUi("ventana8.ui")

# Conexiones de los botones
ventana_bienvenida.registro.clicked.connect(ventana_registro.show)
ventana_registro.entrar.clicked.connect(registrar_usuario)
ventana_registro_exitoso.entrar.clicked.connect(ventana_registro_exitoso.close)
ventana_registro_exitoso.entrar.clicked.connect(ventana_entrar.show)
ventana_registro.cancelar.clicked.connect(ventana_registro.close)
ventana_registro.cancelar.clicked.connect(ventana_bienvenida.show)
ventana_bienvenida.iniciosesion.clicked.connect(ventana_entrar.show)
ventana_entrar.cancelar.clicked.connect(ventana_bienvenida.show)
ventana_entrar.cancelar.clicked.connect(ventana_entrar.close)
ventana_entrar.entrar.clicked.connect(iniciar_sesion)
ventana_bienvenida.salir.clicked.connect(app.exit)

ventana_error.cancelar.clicked.connect(ventana_error.close)
ventana_error.cancelar.clicked.connect(ventana_entrar.show)
ventana_error.entrar.clicked.connect(ventana_error.close)
ventana_error.entrar.clicked.connect(ventana_registro.show)

ventana_menu.resena.clicked.connect(abrir_ventana_resenas)
ventana_menu.favoritos.clicked.connect(abrir_ventana_favoritos)

ventana_menu.salir.clicked.connect(ventana_salir.show)
ventana_resenas.agregar.clicked.connect(abrir_ventana_resena_propia)
ventana_resenas.cancelar.clicked.connect(lambda: ventana_resenas.close() and ventana_menu.show())
# Conexiones de los botones de ventana_resena_propia
ventana_resena_propia.enviar.clicked.connect(guardar_resena)
ventana_resena_propia.cancelar.clicked.connect(ventana_resena_propia.close)
ventana_resena_propia.cancelar.clicked.connect(ventana_menu.show)
ventana_guardado.cancelar.clicked.connect(regresandoamenuprincipal)
ventana_favoritos.regresar.clicked.connect(ventana_favoritos.close)
ventana_favoritos.regresar.clicked.connect(ventana_menu.show)
ventana_salir.cancelar.clicked.connect(ventana_salir.close)
ventana_salir.cancelar.clicked.connect(ventana_menu.show)
ventana_salir.salir.clicked.connect(salir)

ventana_favoritos.resena.clicked.connect(ventana_favoritos.close)
ventana_favoritos.resena.clicked.connect(ventana_resena_propia.show)

# Configuración de las imágenes
ventana_bienvenida.labelImagen.setPixmap(QtGui.QPixmap("rosa.png"))
ventana_bienvenida.labelImagen.setScaledContents(True)
ventana_registro.labelImagen.setPixmap(QtGui.QPixmap("rosa.png"))
ventana_registro.labelImagen.setScaledContents(True)
ventana_registro_exitoso.labelImagen.setPixmap(QtGui.QPixmap("rosa.png"))
ventana_registro_exitoso.labelImagen.setScaledContents(True)
ventana_entrar.labelImagen.setPixmap(QtGui.QPixmap("rosa.png"))
ventana_entrar.labelImagen.setScaledContents(True)
ventana_error.labelImagen.setPixmap(QtGui.QPixmap("rosa.png"))
ventana_error.labelImagen.setScaledContents(True)
ventana_menu.labelImagen.setPixmap(QtGui.QPixmap("amarillo.png"))
ventana_menu.labelImagen.setScaledContents(True)
ventana_resenas.labelImagen.setPixmap(QtGui.QPixmap("rosa.png"))
ventana_resenas.labelImagen.setScaledContents(True)
ventana_resena_propia.labelImagen.setPixmap(QtGui.QPixmap("rosa.png"))
ventana_resena_propia.labelImagen.setScaledContents(True)
ventana_guardado.labelImagen.setPixmap(QtGui.QPixmap("rosa.png"))
ventana_guardado.labelImagen.setScaledContents(True)
ventana_salir.labelImagen.setPixmap(QtGui.QPixmap("amarillo.png"))
ventana_salir.labelImagen.setScaledContents(True)


def escalar_imagen(label, ruta_imagen):
    pixmap = QtGui.QPixmap(ruta_imagen)
    pixmap = pixmap.scaled(label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
    label.setPixmap(pixmap)
    label.setScaledContents(True)

escalar_imagen(ventana_favoritos.labelImagen_3, "1.png")
escalar_imagen(ventana_favoritos.labelImagen_4, "2.png")
escalar_imagen(ventana_favoritos.labelImagen_6, "3.png")
escalar_imagen(ventana_favoritos.labelImagen_8, "4.png")
escalar_imagen(ventana_favoritos.labelImagen_9, "c.png")
escalar_imagen(ventana_favoritos.labelImagen_7, "e.png")
escalar_imagen(ventana_favoritos.labelImagen_5, "a.png")
escalar_imagen(ventana_favoritos.labelImagen, "rosa.png")

movie = QMovie("giphy2.gif")
original_size = movie.frameRect().size()
ventana_favoritos.labelvideo.setMovie(movie)
# Obtener el tamaño actual del QLabel
current_size = ventana_favoritos.labelvideo.size()
# Escalar el GIF al tamaño actual del QLabel
scaled_size = original_size.scaled(current_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
# Asignar el QMovie al QLabel y establecer el tamaño
ventana_favoritos.labelvideo.setMovie(movie)
ventana_favoritos.labelvideo.setFixedSize(scaled_size)
# Iniciar la reproducción del GIF
movie.start()


ventana_bienvenida.show()
app.exec_()
