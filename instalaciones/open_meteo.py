import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
from .regresion_multiple import prediccion_energia
from datetime import timedelta

def open_meteo (request,insta):
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": insta.latitud,
		"longitude": insta.longitud,
		"current": ["temperature_2m", "relative_humidity_2m", "precipitation", "weather_code", "wind_speed_10m"],
		"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "uv_index_max", "precipitation_sum", "wind_speed_10m_max"],
		"timezone": "auto",
		"forecast_days": 4
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]

	# Current values. The order of variables needs to be the same as requested.
	current = response.Current()
	current_temperature_2m = current.Variables(0).Value()
	current_relative_humidity_2m = current.Variables(1).Value()
	current_precipitation = current.Variables(2).Value()
	current_weather_code = current.Variables(3).Value()
	current_weather_code_image = str(round(current_weather_code))+".png"
	current_wind_speed_10m = current.Variables(4).Value()

	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	daily_weather_code = daily.Variables(0).ValuesAsNumpy()
	daily_weather_code_image = []
	for element in daily_weather_code:
		daily_weather_code_image.append(str(round(element))+".png")

	daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
	daily_uv_index_max = daily.Variables(3).ValuesAsNumpy()
	daily_precipitation_sum = daily.Variables(4).ValuesAsNumpy()
	daily_wind_speed_10m_max = daily.Variables(5).ValuesAsNumpy()

	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	daily_data["weather_code"] = daily_weather_code
	daily_data["weather_code_image"] = daily_weather_code_image
	daily_data["temperature_2m_max"] = daily_temperature_2m_max
	daily_data["temperature_2m_min"] = daily_temperature_2m_min
	daily_data["uv_index_max"] = daily_uv_index_max
	daily_data["precipitation_sum"] = daily_precipitation_sum
	daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max


	return({'temperatura':current_temperature_2m, 'humedad':current_relative_humidity_2m,'viento':current_wind_speed_10m,
			'cielo':current_weather_code_image, 'precipitacion':current_precipitation,'diario':daily_data})

def open_meteo_energia (request,insta,dias):


	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
	retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
	openmeteo = openmeteo_requests.Client(session=retry_session)

	# Make sure all required weather variables are listed here
	# The order of variables in hourly or daily is important to assign them correctly below
	url = "https://api.open-meteo.com/v1/forecast"
	params = {
		"latitude": insta.latitud,
		"longitude": insta.longitud,
		"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "uv_index_max", "uv_index_clear_sky_max", "precipitation_sum", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_hours", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"],
	"timezone": "Europe/Berlin",
	"forecast_days": dias
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]


	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	daily_weather_code = daily.Variables(0).ValuesAsNumpy()
	daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
	daily_apparent_temperature_max = daily.Variables(3).ValuesAsNumpy()
	daily_apparent_temperature_min = daily.Variables(4).ValuesAsNumpy()
	daily_sunrise = daily.Variables(5).ValuesAsNumpy()
	daily_sunset = daily.Variables(6).ValuesAsNumpy()
	daily_daylight_duration = daily.Variables(7).ValuesAsNumpy()
	daily_sunshine_duration = daily.Variables(8).ValuesAsNumpy()
	daily_uv_index_max = daily.Variables(9).ValuesAsNumpy()
	daily_uv_index_clear_sky_max = daily.Variables(10).ValuesAsNumpy()
	daily_precipitation_sum = daily.Variables(11).ValuesAsNumpy()
	daily_rain_sum = daily.Variables(12).ValuesAsNumpy()
	daily_showers_sum = daily.Variables(13).ValuesAsNumpy()
	daily_snowfall_sum = daily.Variables(14).ValuesAsNumpy()
	daily_precipitation_hours = daily.Variables(15).ValuesAsNumpy()
	daily_precipitation_probability_max = daily.Variables(16).ValuesAsNumpy()
	daily_wind_speed_10m_max = daily.Variables(17).ValuesAsNumpy()
	daily_wind_gusts_10m_max = daily.Variables(18).ValuesAsNumpy()
	daily_wind_direction_10m_dominant = daily.Variables(19).ValuesAsNumpy()
	daily_shortwave_radiation_sum = daily.Variables(20).ValuesAsNumpy()
	daily_et0_fao_evapotranspiration = daily.Variables(21).ValuesAsNumpy()

	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	daily_data["weather_code"] = daily_weather_code
	daily_data["temperature_2m_max"] = daily_temperature_2m_max
	daily_data["temperature_2m_min"] = daily_temperature_2m_min
	daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
	daily_data["apparent_temperature_min"] = daily_apparent_temperature_min
	daily_data["sunrise"] = daily_sunrise
	daily_data["sunset"] = daily_sunset
	daily_data["daylight_duration"] = daily_daylight_duration
	daily_data["sunshine_duration"] = daily_sunshine_duration
	daily_data["uv_index_max"] = daily_uv_index_max
	daily_data["uv_index_clear_sky_max"] = daily_uv_index_clear_sky_max
	daily_data["precipitation_sum"] = daily_precipitation_sum
	daily_data["rain_sum"] = daily_rain_sum
	daily_data["showers_sum"] = daily_showers_sum
	daily_data["snowfall_sum"] = daily_snowfall_sum
	daily_data["precipitation_hours"] = daily_precipitation_hours
	daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
	daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
	daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
	daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant
	daily_data["shortwave_radiation_sum"] = daily_shortwave_radiation_sum
	daily_data["et0_fao_evapotranspiration"] = daily_et0_fao_evapotranspiration



	daily_dataframe = pd.DataFrame(data = daily_data)

	predict = prediccion_energia(daily_dataframe)

	return predict

