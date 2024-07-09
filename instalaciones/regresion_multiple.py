import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import statsmodels.api as sm

from datetime import datetime, timedelta

def forward_selection(
		X: pd.DataFrame,
		y: pd.Series,
		criterio: str = 'aic',
		add_constant: bool = True,
		verbose: bool = True
	) -> list:
		if add_constant:
			X = sm.add_constant(X, prepend=True).rename(columns={'const': 'intercept'})

		restantes = X.columns.to_list()
		seleccion = []
		if criterio == 'rsquared_adj':
			mejor_metrica = -np.inf
			ultima_metrica = -np.inf
		else:
			mejor_metrica = np.inf
			ultima_metrica = np.inf

		while restantes:
			metricas = []
			for candidata in restantes:
				seleccion_temp = seleccion + [candidata]
				modelo = sm.OLS(endog=y, exog=X[seleccion_temp])
				modelo_res = modelo.fit()
				metrica = getattr(modelo_res, criterio)
				metricas.append(metrica)
			if criterio == 'rsquared_adj':
				mejor_metrica = max(metricas)
				if mejor_metrica > ultima_metrica:
					mejor_variable = restantes[np.argmax(metricas)]
				else:
					break
			else:
				mejor_metrica = min(metricas)
				if mejor_metrica < ultima_metrica:
					mejor_variable = restantes[np.argmin(metricas)]
				else:
					break

			seleccion.append(mejor_variable)
			restantes.remove(mejor_variable)
			ultima_metrica = mejor_metrica

		return sorted(seleccion)

def prediccion_energia(df_a_predecir):
	df= pd.read_csv("./5-instalacion2.csv")

	#Se borran las columnas de fecha y el índice por ser irrelevantes
	del df['date']
	del df['Unnamed: 0']

	#Se quita la columna producción de los datos a utilizar y se establece como los valores en el eje Y
	X = df.drop(columns='produccion')
	y = df['produccion']

	#Se dividen los datos en train y test
	X_train, X_test, y_train, y_test = train_test_split(
											X,
											y.values.reshape(-1,1),
											train_size   = 0.8,
											random_state = 1234,
											shuffle      = True


										)

	X_train = sm.add_constant(X_train, prepend=True).rename(columns={'const':'intercept'})

	predictores = forward_selection(
		X            = X_train,
		y            = y_train,
		criterio     = 'aic',
		add_constant = False, # Ya se le añadió anteriormente
		verbose      = True
	)

	modelo_final  = sm.OLS(endog=y_train, exog=X_train[predictores])
	modelo_final_res = modelo_final.fit()


	mod =modelo_final_res.predict(df_a_predecir[predictores])

	now = datetime.now()

	dias = []
	for element in mod:
		text_date = now.strftime("%d-%b")
		dias.append({'fecha':text_date,'prediccion':round(element,2)})
		now = now + timedelta(days=1)



	return dias

