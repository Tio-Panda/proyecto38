def guardar_archivos_cache(archivos, nombre_usuario):
    for archivo in archivos:

        with open('organizador/static/archivos_csv/{}/cache/{}'.format(nombre_usuario,archivo.name), 'wb+') as destination:
            for chunk in archivo.chunks():
                destination.write(chunk)

def crear_archivo_csv(usuario, nombre_negocio, nombre_archivo):
    import os

    carpeta = os.makedirs('organizador/static/archivos_csv/{}/{}'.format(usuario.username, nombre_negocio), exist_ok=True)
    ruta = 'organizador/static/archivos_csv/{}/{}/{}.csv'.format(usuario.username, nombre_negocio, nombre_archivo)
    
    archivo = open(ruta, 'wb+')
    archivo.close()

    return ruta

def crear_cache(usuario):
    import os

    carpeta = os.makedirs('organizador/static/archivos_csv/{}/cache'.format(usuario.username), exist_ok=True)
    ruta = 'organizador/static/archivos_csv/{}/cache'.format(usuario.username)

    return ruta

def fusionar_csv(ruta_master, cache):
    import os
    import glob
    import pandas as pd

    archivos = glob.glob(cache + "/*.csv")
    frames = []

    try:
        master = pd.read_csv(ruta_master, sep=";")
        master.drop([''], axis=1)
    except:
        master = pd.read_csv(archivos.pop(0), sep=";")
    
    frames.append(master)

    for archivo in archivos:
         data = pd.read_csv(archivo, sep=";")
         frames.append(data)

    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates()
    df['fecha'] = df['fecha'].apply(limpiar_fecha)
    print(df.shape)

    df.to_csv(ruta_master, header=True, sep=";")

    # Separar la columna fecha en fecha y horas
    
    #Sumar el numero de boletas

    for archivo in archivos:
        os.remove(archivo)

def sacar_nombres_negocios(lista):
    nombres_totales = []

    for nombre in lista:
        if nombre not in nombres_totales:
            nombres_totales.append(nombre)

    return nombres_totales

def separar_csv_por_negocio(ruta_master):
    import pandas as pd

    master = pd.read_csv(ruta_master, sep=";")

    nombres = sacar_nombres_negocios(master['sucursal'])

    return nombres

def limpiar_fecha(string):
    fecha = string[0:10] + ":" + string[11:23]
    return fecha

def distribuir_csv_por_negocio(ruta_master, ruta_negocio, nombre_selecto):
    import pandas as pd
    pd.options.mode.chained_assignment = None

    print(nombre_selecto + " inicio a guardar en " + ruta_negocio)
    
    master = pd.read_csv(ruta_master, sep=";")
    master = master.drop(['Unnamed: 0'], axis=1)

    try:
        negocio = pd.read_csv(ruta_negocio, sep=";")
        negocio = negocio.drop(['Unnamed: 0'], axis=1)

        print(negocio.shape)

        frames = []
        frames.append(negocio)

        print("hay archivo")
        archivo_anterior = True

    except:
        print("no hay archivo anterior")
        archivo_anterior = False
    
    df = master[master["sucursal"] == nombre_selecto]

    if archivo_anterior:
        frames.append(df)
        df = pd.concat(frames, ignore_index=True)
        df = df.drop_duplicates()
        print(df.shape)

    df.to_csv(ruta_negocio, header=True, sep=";")


# Mostrador que te muestre ganancias por la fecha que tu elijas y los intervalos que tu elijas
def organizar_intervalos(archivo, inter):
    import pandas as pd

    df = archivo
    intervalo = df.index.to_period(inter)

    df_sum = df.groupby([intervalo]).sum()

    df_nuevo = pd.DataFrame(columns=['fecha', 'neto', 'iva', 'total', 'volumen'])

    df_nuevo['fecha'] = df_sum.index
    df_nuevo = df_nuevo.set_index(['fecha'])

    df_nuevo['neto'] = df_sum['neto']
    df_nuevo['iva'] = df_sum['iva']
    df_nuevo['total'] = df_sum['total']
    df_nuevo['volumen'] = df.groupby([intervalo]).size()

    k = {'fecha' : df_nuevo.index, 'neto' : df_nuevo['neto'], 'iva' : df_nuevo['iva'], 'total' : df_nuevo['total'], 'volumen' : df_nuevo['volumen']}
    
    return k

def mostrar_info(ruta_negocio, fecha_inicio, fecha_final, intervalo):
    import pandas as pd
    #pd.options.mode.chained_assignment = None

    negocio = pd.read_csv(ruta_negocio, sep=";")
    negocio = negocio.drop(['Unnamed: 0'], axis=1)

    negocio['fecha'] = pd.to_datetime(negocio['fecha'], format='%Y-%m-%d:%H:%M:%S.%f')
    negocio = negocio.set_index(['fecha'])
    #print(negocio.shape)

    #dias = (negocio.index > fecha_inicio) & (negocio.index <= fecha_final)
    #datos_filtrados = negocio.loc[dias]
    datos_filtrados = negocio.loc[fecha_inicio:fecha_final]
    #print(datos_filtrados.head(5))

    #datos_filtrados = negocio[negocio["fecha"].isin(pd.date_range(fecha_inicio, fecha_final))]

    k = organizar_intervalos(datos_filtrados, intervalo)
    
    return k
