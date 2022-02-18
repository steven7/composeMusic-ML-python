## This file contains the API endpoint definations and is the gateway to the application.
from flask import Flask

from flask import jsonify, make_response, request, send_file
from compose import load_muse_gan, muse_gan_compose_write_to_midi, compose_midi, create_wav_with_midi, wav_filepath_out_of_midi_filepath, fetch_midi
import os
import requests

app = Flask(__name__)

is_prod = False

@app.route("/")
def index():
    return "<p>Hello, World!</p>"


## Creates and writes composed midi file and converts to a wav. Both versions are saved.
@app.route("/compose", methods = ['POST'])
def compose():
    composed_midi_filepath, _ = compose_midi()
    composed_wav_filepath = create_wav_with_midi(composed_midi_filepath)
    response = {
      "success": True,
      "code": 200,
      "message": "Muse Gan created a midi and converted to music file",
      "filepath" : composed_wav_filepath # composed_midi_filepath
    }
    return jsonify(response)


## outputs composed midi file to the user
#@app.route("/fetchMidi/<filename>")
#def fetchMidi(filename):
#@app.route("/fetchMidi")
#def fetchMidi():   
#    filename = '10-15-2021.00-09-47_3dfca061-03b0-4a93-82d8-32addd81ec91.midi'
#    run_folder = 'run/0018_chorales/composed_music/'
#    filepath = run_folder + filename
#    # Send midifile to client
#    try:
#        # Fetch the midi file
#        midi_file = open(filepath, 'rb')
#        # File length in bytes
#        file_size = os.path.getsize(filepath)
#        # response object
#        response = make_response()
#        # Add midi file data
#        response.data = midi_file.read()
#        # Add headers 
#        response.headers['Content-Disposition'] = "attachment; filename="+filename
#        response.headers['Content-Type'] = "audio/midi"
#        response.headers['Content-Length'] = file_size
#        return response
#    # Handle error case
#    except Exception as e:
#        response = {
#          "success": False,
#          "code": 404,
#          "message": "Could not fetch midi file",
#          "detail": str(e)
#        }
#        return jsonify(response)

 

#@app.route("/fetchMidiAndSendToComposify", methods = ['POST'])
#def fetchMidiAndSendToComposify():
#    filename = '10-15-2021.00-09-47_3dfca061-03b0-4a93-82d8-32addd81ec91.midi'
#    run_folder = 'run/0018_chorales/composed_music/'
#    filepath = run_folder + filename
#    # Send midifile to client
#    try:
#        
#        # Fetch the midi file
#        midi_file = open(filepath, 'rb')
#        
#        # File length in bytes
#        file_size = os.path.getsize(filepath)
#        
#        # default cover image
#        default_cover_file_path = "images/music_icon_blue_transparent.png"
#        cover_file = open(default_cover_file_path, 'rb')
# 
#        # Initial fallback values
#        user_id = 1
#        title = '' 
#        artist = '' 
#        desc = '' 
#         
#        # Write the key values once for beter organization.
#        user_id_key = 'userID'
#        title_key = 'title'
#        artist_key = 'artist'
#        desc_key = 'desc'
#        
#        # Will take either form data or json.
##        if len(request.form) > 0:
##            print(request.form)
##            user_id = request.form.get('userID') # 1
##            user_id = request.form.get('title')
##            user_id = request.form.get('artist')
##            user_id = request.form.get('desc')
##        else: # Look through the json body  to put into the follow up post request to the web app.
#        request_data = request.get_json() 
#
#        if user_id_key in request_data:
#            user_id = request_data[user_id_key]
#
#        if title_key in request_data:
#            title = request_data[title_key]
#
#        if artist_key in request_data:
#            artist = request_data[artist_key]
#
#        if desc_key in request_data:
#            desc = request_data[desc_key]
#    
#        # TODO: make request and send to composify (create music) web app api.
#        port_number = 8000
#        docker_container_name = "app"
#        composify_base_url = 'http://' + docker_container_name + ':' + str(port_number)
#        composify_create_url = '/api/tracks/createlocal'
#        # Create the whole path we want for the call to Composify Go code.
#        composify_url = composify_base_url + composify_create_url
#
#        # Metadata in the request bosy will be in this dictionary.
#        json_body = {
#                'userID':user_id,
#                'title': title,
#                'artist': artist,
#                'desc': desc
#        }
#
#        # coverimage file object
#        coverimage = {'file':('coverimage', cover_file, 'image/png')}
#        # musicfile file object
#        musicfile = {'file':('musicfile', midi_file, 'audio/midi')}
#        
#        # Include the files with this dictionary.
#        multipart_form_data_files = { 
#            "coverimage": ('music_icon_blue_transparent.png', cover_file), 
#            "musicfile": (filename, midi_file)
#        }
#
#
#        headers = requests.utils.default_headers()
#
#        headers.update( { # We let the multipart/form-data be included in the content type header byt the requests library.
#                "Accept": "*/*",
#                "Host": "Compose",
#                "Connection": "keep-alive",
#                "User-Agent": "My User Agent 1.0"
#            }
#        )
#
#        # Use sesion for request
#        MAX_RETRIES = 10
#        session = requests.Session()
#        adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
#        session.mount('https://', adapter)
#        session.mount('http://', adapter)
#
#        # Carry out request and get response.
#        response = session.post(url = composify_url,
#                                headers = headers, 
#                                data = json_body,
#                                files = multipart_form_data_files) 
#
#        response.close()
#
#        responseJson = response.json()
#
#        print(' the response: ' + str(response), flush=True)
#
#        return responseJson
#    
#    # Handle error case
#    except Exception as e:
#        response = {
#          "success": False,
#          "code": 500,
#          "message": "Could not fetch midi file",
#          "detail": str(e)
#        }
#        return jsonify(response)
#    return


@app.route("/composeWithWebApp", methods = ['POST'])
def composeWithWebApp():
    # find channel 
    channel = os.environ.get('channel_env_var')
    is_prod = channel == 'prod'
    
    print('___________________ we are in ' + channel + ' channel ___________________ ' + str(is_prod))

    # folder to complete operaion with
    run_folder = 'run/0018_chorales/composed_music/'
    # Send music file to client
    try:
        request_data = request.get_json()
        print(request_data) 
      
        #
        # Parse paramters
        #
            
        # Initial fallback values
        user_id = 1
        title = '' 
        artist = '' 
        desc = '' 
        compose_type = ''
        
        # Write the key values once for beter organization.
        user_id_key = 'userID'
        title_key = 'title'
        artist_key = 'artist'
        desc_key = 'desc'
        compose_type_key = 'compose_type'
        
        # Will take either form data or json.
        if len(request.form) > 0:
            print(request.form)
#            user_id = request.form.get('userID') # 1
#            user_id = request.form.get('title')
#            user_id = request.form.get('artist')
#            user_id = request.form.get('desc')
        else: # Look through the json body  to put into the follow up post request to the web app.
            request_data = request.get_json() 
          
            if user_id_key in request_data:
                user_id = request_data[user_id_key]
                
            if title_key in request_data:
                title = request_data[title_key]
                
            if artist_key in request_data:
                artist = request_data[artist_key]
                
            if desc_key in request_data:
                desc = request_data[desc_key]
                
            if compose_type_key in request_data:
                compose_type = request_data[compose_type_key]

        # 
        # Create music
        # 
        # These next two methods compose the file and then it creates a music format version in an mp3
        #
        # Compose the midi file
        composed_midi_filepath, composed_midi_filename = compose_midi(compose_type)
        
        
        # Create the music file out of the compoed midi
        composed_wav_filepath = create_wav_with_midi(composed_midi_filepath)
        composed_wav_filename = wav_filepath_out_of_midi_filepath(composed_midi_filename)
               
        
        # Fetch the music file
        music_file = open(composed_wav_filepath, 'rb')
         
        # default cover image
        default_cover_file_path = "images/music_icon_blue_transparent.png"
        cover_file = open(default_cover_file_path, 'rb')
         
 
        # TODO: make request and send to composify (create music) web app api.
        port_number = 8000
        host_name = "app" # dev for local docker. the continaer name will be the host this cae.
        if is_prod:
            host_name = "app" #"aws_host_name_app_container" #not the offical prod one yet. TODO: complete uploading containr to 
            
        composify_base_url = 'http://' + host_name + ':' + str(port_number)
        composify_create_url = '/api/tracks/createlocal'
        # Create the whole path we want for the call to Composify Go code.
        composify_url = composify_base_url + composify_create_url

        # Metadata in the request bosy will be in this dictionary.
        json_body = {
                'userID':user_id,
                'title': title,
                'artist': artist,
                'desc': desc
        }
 
        # Include the files with this dictionary.
        multipart_form_data_files = { 
            "coverimage": ('music_icon_blue_transparent.png', cover_file), 
            "musicfile": (composed_wav_filename, music_file)
        }


        headers = requests.utils.default_headers()
        
        headers.update( { # We let the multipart/form-data be included in the content type header byt the requests library.
                "Accept": "*/*",
                "Host": "Compose",
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
        response = session.post(url = composify_url,
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
        return jsonify(response)
    return