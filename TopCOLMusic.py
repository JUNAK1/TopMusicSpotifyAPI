import requests
import base64
import csv


client_id = '9b4bff08fded4ec5b3022992c818c6e9'
client_secret = '11d2b8ba037a442e8350886f10abe0cc'

# Codifica en base64 tu ID de cliente y tu secreto de cliente
auth_header = base64.b64encode(f'{client_id}:{client_secret}'.encode('ascii')).decode('ascii')


url = 'https://accounts.spotify.com/api/token'

# Datos para la solicitud
data = {
    'grant_type': 'client_credentials'
}

#  encabezados para la solicitud
headers = {
    'Authorization': f'Basic {auth_header}'
}

# solicitud para obtener el token de acceso
response = requests.post(url, data=data, headers=headers)

# Verifica si la solicitud fue exitosa
if response.status_code == 200:
    
    access_token = response.json()['access_token']

    # Define los géneros a buscar
    generos = ['pop', 'rock', 'reggaeton']

    #  Colombia
    pais = 'CO'

    # API de Spotify
    base_url = 'https://api.spotify.com/v1/'

    # encabezados para las solicitudes a la API
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    
    for genero in generos:
    
        canciones = []

        #  URL para obtener las canciones más populares del género actual en el país definido
        url = f'{base_url}search?q=genre:{genero}&type=track&market={pais}&limit=50'

        # Realiza la solicitud a la API de Spotify
        response = requests.get(url, headers=headers)

        # Verifica si la solicitud fue exitosa
        if response.status_code == 200:
            # Obtiene los datos de la respuesta
            data = response.json()

            # Recorre cada canción en los resultados
            for track in data['tracks']['items']:
                # Agrega la información de la canción a la lista de canciones del género actual
                canciones.append({
                    'nombre': track['name'],
                    'artista': track['artists'][0]['name'],
                    'popularidad': track['popularity']
                })

            # Ordena las canciones por popularidad (de mayor a menor)
            canciones.sort(key=lambda x: x['popularidad'], reverse=True)

            # Crea un archivo CSV para el género actual
            with open(f'{genero}.csv', mode='w') as file:
                writer = csv.writer(file)
                writer.writerow(['Nombre', 'Artista', 'Popularidad'])

                # Escribe cada canción en el archivo CSV
                for cancion in canciones:
                    writer.writerow([cancion['nombre'], cancion['artista'], cancion['popularidad']])