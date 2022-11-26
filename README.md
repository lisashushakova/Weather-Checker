# Weather-Checker
Weather-checker app allows you to retrieve information about weather conditions 
### Getting current temperature by coordinates (lat and lon):
Route:
    
    http://localhost:8000/weather-by-coords?lat={LOCATION_LATITUDE}&lon={LOCATION_LONGTITUDE}
Example:
    
    http://localhost:5000/weather-by-coords?lat=60.0&lon=30.0
Returns:

    Temperature: -9.85°C

### Retrieving current temperature by city name:
Route:
    
    http://localhost:8000/weather-by-city?city={CITY_NAME}
Example:
    
    http://localhost:5000/weather-by-city?city=Murmansk
Returns:

    Temperature: -3.73°C


### Retrieving other weather params:

Route:
    
    http://localhost:8000/weather-by-coords?lat={LOCATION_LATITUDE}&lon={LOCATION_LONGTITUDE}&weather_params={WEATHER_PARAMETER}

Available weather parameters:
* temperature
* wind
* humidity
* pressure


Example:
    
    http://localhost:8000/weather-by-coords?lat=60&lon=30&weather_params=pressure&weather_params=wind
Returns:

    Temperature: -9.85°C
    Wind: 4.92 m/s, 108°

### Retrieving weather for 5 days (3 hours step):
Route:

    http://localhost:8000/week-weather-by-coords?lat={LOCATION_LATITUDE}&lon={LOCATION_LONGTITUDE}&weather_params={WEATHER_PARAMETER}
Example:

    http://localhost:8000/week-weather-by-coords?lat=60&lon=30&weather_params=temperature&weather_params=wind
Returns:

    Date: 2022-11-26 18:00:00
    Temperature: -8.38°C
    Wind: 4.86 m/s, 110°
    
    Date: 2022-11-26 21:00:00
    Temperature: -6.91°C
    Wind: 4.67 m/s, 112°
    
    ...
    
    Date: 2022-12-01 15:00:00
    Temperature: -4.68°C
    Wind: 2.69 m/s, 115°


### Retrieving general weather description:

Route:
    
    http://localhost:8000/description-by-coords?lat={LOCATION_LATITUDE}&lon={LOCATION_LONGTITUDE}
Example:

    http://localhost:8000/description-by-coords?lat=60&lon=30
Returns:

    Weather description:
    Clouds (overcast clouds)

##Docker
####Docker image creation:
    docker build -t weather-checker-image .  
####Docker container creation:
    docker create -p 8000:8000 --name weather-checker-container  weather-checker-image
####Start container:
    docker start weather-checker-container 
