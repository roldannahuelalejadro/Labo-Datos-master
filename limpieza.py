import pandas as pd
import duckdb as dd
import sys
import os

carpeta = "TablasOriginales"

padron_poblacion =  pd.read_excel(carpeta + "/padron_poblacion.xlsX")
datos_departamento = pd.read_csv(carpeta + "/Datos_por_departamento_actividad_y_sexo.csv")
padron_establecimientos_educativos  = pd.read_excel(carpeta + "/2022_padron_oficial_establecimientos_educativos.xlsx", skiprows = 6)
actividades_establecimientos_productivos = pd.read_csv(carpeta + "/actividades_establecimientos.csv")

#%%--------------------------------------------------------------------------------------------------------------------------------
carpeta = "TablasOriginales"

padron_poblacion =  pd.read_excel(carpeta + "/padron_poblacion.xlsX")

padron_poblacion.columns = ['nada', 'edad', 'casos', 'porcentaje', 'porcentaje_acumulado']
padron_poblacion.columns


edad_index = []
total_index = []
areas = []
id_areas = []
counter = 0
counter_total = 0


for i in range(len(padron_poblacion['edad'].tolist())): # saco los indices de fila donde aparece Edad 
    if padron_poblacion['edad'].tolist()[i] == 'Edad':
        counter += 1
        edad_index.append(i+1)
        id_areas.append(padron_poblacion['edad'].tolist()[i-2])
        areas.append(padron_poblacion['casos'].tolist()[i-2])


for i in range(len(padron_poblacion['edad'].tolist())): # saco los indices de fila donde aparece Total
    if padron_poblacion['edad'].tolist()[i] == 'Total':
        total_index.append(i)
        counter_total += 1

if  counter != counter_total:
    print("Error: Tamaños de indexacion diferentes")
    sys.exit()


df_list = []
for index in range(counter): #
    edad = padron_poblacion['edad'][edad_index[index]: total_index[index]].tolist()
    casos = padron_poblacion['casos'][edad_index[index]: total_index[index]].tolist()
    porcentaje = padron_poblacion['porcentaje'][edad_index[index]: total_index[index]].tolist()
    porcentaje_acumulado = padron_poblacion['porcentaje_acumulado'][
        edad_index[index]: total_index[index]].tolist()
    
    data = {
        'edad': edad,
        'casos': casos,
        'porcentaje': porcentaje,
        'porcentaje_acumulado': porcentaje_acumulado
    }
    df_ = pd.DataFrame(data)

    ruta_subcarpeta = os.path.join('TablasModificadas', 'Padrones')

    os.makedirs(ruta_subcarpeta, exist_ok=True)


    id_departamentos = [id_area.replace('AREA # ', '') for id_area in id_areas]
    ruta_archivo = os.path.join(ruta_subcarpeta, f'padron_poblacion_{id_departamentos[index]}.csv')
    df_.to_csv(ruta_archivo, index=False)
    
    df_list.append(df_)

areas = areas[:-1]
id_areas = id_areas[:-1]



#%%--------------------------------------------------------------------------------------------------------------------------------
# Extraer las IDs numéricas de id_areas
id_departamentos = [id_area.replace('AREA # ', '') for id_area in id_areas]

# Crear el mapeo correcto
mapeo_departamentos = pd.DataFrame({
    'id_departamentos': id_departamentos,
    'departamento': areas
})

mapeo_departamentos



# Cambio el nombre en las columnas de '1º de Mayo' y 'Puan' en el df de EP
#%%--------------------------------------------------------------------------------------------------------------------------------
datos_departamento
consultaSQL = """
SELECT DISTINCT departamento
FROM datos_departamento 
              """

dataframeResultado = dd.sql(consultaSQL).df()
dataframeResultado

EP_deparatementos = list(dataframeResultado['departamento'])
conjunto1 = set(areas)
interseccion_set = conjunto1.intersection(EP_deparatementos)
interseccion_lista = list(interseccion_set)


[x for x in EP_deparatementos if x not in interseccion_lista]

print('1º de Mayo' == '1° de Mayo' )
print('Puan' == 'Puán')

#saco los indices de los id sucios:
datos_departamento['departamento'] = datos_departamento['departamento'].replace({
    'Puán': 'Puan',
    '1° de Mayo': '1º de Mayo'
})

consultaSQL = """
SELECT DISTINCT departamento
FROM datos_departamento 
              """

dataframeResultado = dd.sql(consultaSQL).df()
dataframeResultado

EP_deparatementos = list(dataframeResultado['departamento'])
conjunto1 = set(areas)
interseccion_set = conjunto1.intersection(EP_deparatementos)
interseccion_lista = list(interseccion_set)

[x for x in EP_deparatementos if x not in interseccion_lista]

#%%--------------------------------------------------------------------------------------------------------------------------------
ruta_padrones = os.path.join('TablasModificadas', 'Padrones')
df_grupos_etarios_ = []

archivos_padrones = [f for f in os.listdir(ruta_padrones) if f.startswith('padron_poblacion_') and f.endswith('.csv')]
archivos_padrones = archivos_padrones[:-1] # Quito el Resumen
for archivo in archivos_padrones:
    nombre_departamento = archivo.replace('padron_poblacion_', '').replace('.csv', '')
    ruta_completa = os.path.join(ruta_padrones, archivo)
    df_departamento = pd.read_csv(ruta_completa)
    nombre_departamento = nombre_departamento.replace("'", "''")
    consultaSQL = f"""
    SELECT 
        '{nombre_departamento}' AS id_departamento,
        SUM(CASE WHEN edad BETWEEN 0 AND 2 THEN casos ELSE 0 END) AS cant_edad_prescolar,
        SUM(CASE WHEN edad BETWEEN 3 AND 5 THEN casos ELSE 0 END) AS cant_edad_jardin,
        SUM(CASE WHEN edad BETWEEN 6 AND 11 THEN casos ELSE 0 END) AS cant_edad_primaria,
        SUM(CASE WHEN edad BETWEEN 12 AND 17 THEN casos ELSE 0 END) AS cant_edad_secundaria,
        SUM(CASE WHEN edad BETWEEN 18 AND 64 THEN casos ELSE 0 END) AS cant_edad_laboral,
        SUM(CASE WHEN edad >= 65 THEN casos ELSE 0 END) AS cant_edad_jubilatoria
    FROM df_departamento;
    """
    
    dataframeResultado = dd.sql(consultaSQL).df()
    df_grupos_etarios_.append(dataframeResultado)

df_grupos_etarios = pd.concat(df_grupos_etarios_, ignore_index=True)

df_grupos_etarios


#%%--------------------------------------------------------------------------------------------------------------------------------
consultaSQL = """ SELECT id_departamento, mapeo_departamentos.departamento AS departamento_nombre , cant_edad_prescolar, cant_edad_jardin, cant_edad_primaria,cant_edad_secundaria, cant_edad_laboral,cant_edad_jubilatoria,

FROM df_grupos_etarios INNER JOIN mapeo_departamentos ON  df_grupos_etarios.id_departamento = mapeo_departamentos.id_departamentos


ORDER BY id_departamento ASC
"""


df_depa_con_nombre = dd.sql(consultaSQL).df()
df_depa_con_nombre

#%%--------------------------------------------------------------------------------------------------------------------------------

consultaSQL = """   SELECT DISTINCT provincia, id_departamento, departamento_nombre, cant_edad_prescolar, cant_edad_jardin, cant_edad_primaria,cant_edad_secundaria, cant_edad_laboral,cant_edad_jubilatoria,


FROM df_depa_con_nombre LEFT JOIN datos_departamento ON  datos_departamento.in_departamentos = df_depa_con_nombre.id_departamento

ORDER BY id_departamento ASC

"""

df_final = dd.sql(consultaSQL).df()

df_final.loc[45, 'provincia'] = 'Buenos Aires'
df_final.loc[524, 'provincia'] = 'Tierra Del Fuego'
df_final.loc[526, 'provincia'] = 'Tierra Del Fuego'

df_final

#%%--------------------------------------------------------------------------------------------------------------------------------

ruta = os.path.join('TablasModificadas')
os.makedirs(ruta, exist_ok=True)
ruta_archivo = os.path.join(ruta, 'dato_padron_por_departamento.csv')
df_final.to_csv(ruta_archivo, index=False)


# Me quedo con los datos que quiero:
#%%--------------------------------------------------------------------------------------------------------------------------------
consultaSQL = """
SELECT
    datos_departamento.clae6,
    genero,
    in_departamentos AS id_departamentos,
    empresas_exportadoras,
    establecimientos AS establecimientos,
    empleo AS empleados,
    clae2_desc
FROM datos_departamento

INNER JOIN  actividades_establecimientos_productivos 
ON datos_departamento.clae6 = actividades_establecimientos_productivos.clae6
WHERE anio = 2022
              """

datos_establecimientos= dd.sql(consultaSQL).df()

datos_establecimientos


#%%--------------------------------------------------------------------------------------------------------------------------------

ruta = os.path.join('TablasModificadas')
os.makedirs(ruta, exist_ok=True)
ruta_archivo = os.path.join(ruta, 'datos_establecimientos.csv')
datos_establecimientos.to_csv(ruta_archivo, index=False)


#%%--------------------------------------------------------------------------------------------------------------------------------
padron_establecimientos_educativos  = pd.read_excel(carpeta + "/2022_padron_oficial_establecimientos_educativos.xlsx", skiprows = 6) # salto los irrelevantes
# saquemosle los espacios para poder llamarlos con sql despues:
padron_establecimientos_educativos.columns=['Jurisdicción', 'Cueanexo', 'Nombre', 'Sector', 'Ámbito', 'Domicilio',
       'C_P', 'Código_de_área', 'Teléfono', 'Código_de_localidad',
       'Localidad', 'departamento', 'Mail', 'Común', 'Especial', 'Adultos',
       'Artística', 'Hospitalaria', 'Intercultural', 'Encierro',
       'Jardín_maternal', 'Jardín_de_infantes',
       'Primario', 'Secundario', 'Secundario_INET', 'SNU', 'SNU_INET',
       'Secundario.1', 'SNU.1', 'Talleres',
       'Nivel_inicial_Educación_temprana',
       'Nivel_inicial_Jardín_de_infantes.1', 'Primario.1', 'Secundario.2',
       'Integración_a_la_modalidad_común/_adultos', 'Primario.2',
       'Secundario.3', 'Alfabetización', 'Formación_Profesional',
       'Formación_Profesional_INET', 'Inicial', 'Primario.3', 'Secundario.4',
       'Unnamed: 43']
print(padron_establecimientos_educativos.columns)


#%%--------------------------------------------------------------------------------------------------------------------------------
len(set(mapeo_departamentos['id_departamentos'].to_list()))
# TAbla relaciones cuanexo_nivel
#%%--------------------------------------------------------------------------------------------------------------------------------
tipos_educativos = [
    'Jardín_maternal',
    'Jardín_de_infantes', 
    'Primario',
    'Secundario',
    'Secundario_INET',
    'SNU',
    'SNU_INET'
]

partes_sql = []

for tipo in tipos_educativos:
    parte = f"""
    SELECT Cueanexo, '{tipo}' as tipo_establecimiento
    FROM padron_establecimientos_educativos 
    WHERE (Común = '1' OR Formación_Profesional = '1' OR Formación_Profesional_INET = '1')
      AND {tipo} = '1'
    """
    partes_sql.append(parte)

consulta_union_completa = " UNION ALL ".join(partes_sql)

tabla_de_relaciones = dd.sql(consulta_union_completa).df()
tabla_de_relaciones


#%%--------------------------------------------------------------------------------------------------------------------------------

print(f"Total Cueanexos únicos: {padron_establecimientos_educativos_limpio['Cueanexo'].nunique()}")
print(f"Total filas: {len(tabla_de_relaciones)}")
#Ver que la tabla de relaciones es mayor que el padron de establecimientos limpio
#%%--------------------------------------------------------------------------------------------------------------------------------


a = list(set(list(actividades_establecimientos_productivos['clae6'])))
b  = list(set(list(datos_departamento['clae6'])))

interseccion_set = list(set(a) & set(b))
interseccion_lista = list(interseccion_set)
[x for x in b if x not in interseccion_lista]
# No hay ids fuera