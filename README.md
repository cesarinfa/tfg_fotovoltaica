<h1>Desarrollo de aplicación web de monitorización de instalaciones fotovoltaicas con predicción de energía generada</h1>
César Plaza Benito - Julio 2024

<h2></h2>


El objetivo de este trabajo es el análisis, diseño y desarrollo de una aplicación web de monitorización de instalaciones fotovoltaicas con predicción de energía generada para los siguientes días. Para ello se reciben los datos de generación de las instalaciones junto con los datos meteorológicos y mediante modelos de regresión lineal múltiple, se obtiene el valor de energía generada predicha.


<h2>Entorno de desarrollo</h2>

- Python v3
 
 - Django v5

- PIP v23

- venv
	
 - Paquetes necesarios:

   - django
   - django-active_link
   - django-filter
   - django-utils-six
   - openmeteo_requests
   - requests_cache
   - pandas
   - retry_requests
   - scikit-learn
   - statsmodels
   - folium
   - plotly

- Librerías utilizadas:
  - Bootstrap v5:
    	<code>https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css</code>
  - Chart.js:
    <code>https://cdn.jsdelivr.net/npm/chart.js</code>
    
<h2>Pantallazos</h2>

Inicio de sesión:
![imagen](https://github.com/cesarinfa/tfg_fotovoltaica/assets/159906281/41a7bfdb-d5f2-4507-8119-b130a41591c8)

Menú de instalaciones:
![imagen](https://github.com/cesarinfa/tfg_fotovoltaica/assets/159906281/b67f1eb6-8fbe-4526-a828-ceb2a58fc021)

Datos históricos
![imagen](https://github.com/cesarinfa/tfg_fotovoltaica/assets/159906281/d1510ac5-7c4a-4651-8812-6f8be47f1a79)


