import json
import requests
import os
from compose import compose_midi, create_wav_with_midi, wav_filepath_out_of_midi_filepath 

# Core function for the make music functionality
def compose_music(user_id, title, artist, desc, compose_type, with_webapp, is_prod):
    try:
        # 
        # Create music
        # 
        # These next two method calls compose the file and then it creates a music format version in an mp3
        #
        # Compose the midi file
        composed_midi_filename , composed_midi_filepath = compose_midi(compose_type)
        
        # Create the music file out of the compoed midi
        composed_wav_filepath = create_wav_with_midi(composed_midi_filepath)
        composed_wav_filename = wav_filepath_out_of_midi_filepath(composed_midi_filename)
                
        print('________')
        print('composed_wav_filepath')
        print(composed_wav_filepath)
        print('composed_wav_filename')
        print(composed_wav_filename)
        print('________')

        # Fetch the music file
        music_file = open(composed_wav_filepath, 'rb')
        # only get the midi instead
        # music_file = open(composed_midi_filepath, 'rb')
        print('music_file')
        print(music_file) 
        print('________')
        print()

        # default cover image
        default_cover_file_path = "images/music_icon_blue_transparent.png"
        cover_file = open(default_cover_file_path, 'rb')
                    
        music_file_data = base64.b64encode(music_file)
        cover_file_data = base64.b64encode(cover_file)

        # File clean up.
        # if os.path.isfile(composed_midi_filepath):
        #     os.remove(composed_midi_filepath)
        # if os.path.isfile(composed_wav_filepath):
        #     os.remove(composed_wav_filepath)


        responseJson = {
            "title": title,
            "artist": artist,
            "description": desc,
            "composed_wav_filename": composed_wav_filename,
            "music_file": music_file_data,
            "default_cover_file_path": default_cover_file_path,
            "cover_file": cover_file_data
        }

        # TODO: make request and send to composify (create music) web app api.
        if with_webapp:
            port_number = 8000
            host_name = "app" # dev for local docker. the continaer name will be the host this cae.
            if is_prod:
                host_name = "compose-lb-34767192.us-east-2.elb.amazonaws.com"
                # host_name = "app" #"aws_host_name_app_container" #not the offical prod one yet. TODO: complete uploading containr to 
            
            compose_app_base_url = 'http://' + host_name + ':' + str(port_number)
            compose_app_create_url = '/api/tracks/createlocal'
            # Create the whole path we want for the call to Composify Go code.
            compose_app_url = compose_app_base_url + compose_app_create_url
    
            # I kept this here even though its read in the multipart form data and not here.
            # session. post seems to want this here. maybe one day figure this out.
            json_body = {
                    'userID': user_id,
                    'title': title,
                    'artist': artist,
                    'desc': desc
            }

            # Include the files with this dictionary.
            multipart_form_data_files = { 
                # Metadata in the request body will be in this.
                # Include the typical parameters in form data
                'userID': user_id,
                'title': title,
                'artist': artist,
                'desc': desc,
                # Of course include the files too.
                "coverimage": ('music_icon_blue_transparent.png', cover_file), 
                "musicfile": (composed_wav_filename, music_file)
                # "musicfile": (composed_midi_filename, music_file)
            }

            headers = requests.utils.default_headers()
            headers.update( { # We let the multipart/form-data be included in the content type header byt the requests library.
                    "Accept": "*/*",
                    "User-Agent": "Compose-ML",
                    "Connection": "keep-alive",
                    "User-Agent": "My User Agent 1.0"
                }
            )

            # Use sesion for request
            MAX_RETRIES = 10
            session = requests.Session()
            adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
            session.mount('https://', adapter)
            session.mount('http://', adapter)
            
            # Carry out request and get response.
            response = session.post(url = compose_app_url,
                                    headers = headers,
                                    data = json_body,
                                    files = multipart_form_data_files) 

            response.close()

            responseJson = response.json()

            print(' the response: ' + str(response), flush=True)


        return responseJson
        
    # Handle error case
    except Exception as e:
        response = {
            "success": False,
            "code": 500,
            "message": "Could not compose",
            "detail": str(e)
        }
        return response 
    return