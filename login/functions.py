def crear_archivo_csv(usuario, nombre_carpeta, nombre_archivo):
    ruta = 'organizador/static/archivos_csv/{}/{}/{}.csv'.format(usuario, nombre_carpeta, nombre_archivo)
    
    archivo = open(ruta, 'wb+')
    archivo.close()

    return ruta

def crear_carpeta(usuario, nombre_carpeta):
    import os

    carpeta = os.makedirs('organizador/static/archivos_csv/{}/{}'.format(usuario,nombre_carpeta), exist_ok=True)
    ruta = 'organizador/static/archivos_csv/{}/{}'.format(usuario,nombre_carpeta)
    return ruta