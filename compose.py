## This file contains the functions that wrap the model loading and feedforward network running together.
import datetime
import numpy as np
import uuid
import subprocess

from midi2audio import FluidSynth
from model.MuseGAN import MuseGAN
from utils.loaders import load_music, fetch_midi_file

WEIGHTS_FOLDER = "./model/weights"

BATCH_SIZE = 64
DATA_NAME = 'chorales'
FILENAME = 'Jsb16thSeparated.npz'
RUN_ID = '0018'
RUN_FOLDER = 'run/'
RUN_FOLDER += '_'.join([RUN_ID, DATA_NAME])
WRITE_FOLDER = '/tmp'
n_bars = 2
n_steps_per_bar = 16
n_pitches = 84
n_tracks = 4

def load_music_binary():    
    data_binary, data_ints, raw_data = load_music(DATA_NAME, FILENAME, n_bars, n_steps_per_bar)
    data_binary = np.squeeze(data_binary)
    return data_binary

def load_muse_gan():
    data_binary = load_music_binary()
    gan = MuseGAN(input_dim = data_binary.shape[1:]
        , critic_learning_rate = 0.001
        , generator_learning_rate = 0.001
        , optimiser = 'adam'
        , grad_weight = 10
        , z_dim = 32
        , batch_size = BATCH_SIZE
        , n_tracks = n_tracks
        , n_bars = n_bars
        , n_steps_per_bar = n_steps_per_bar
        , n_pitches = n_pitches
        )
    return 
     
def load_muse_gan_with_weights():
    data_binary = load_music_binary()
    gan = MuseGAN(input_dim = data_binary.shape[1:]
        , critic_learning_rate = 0.001
        , generator_learning_rate = 0.001
        , optimiser = 'adam'
        , grad_weight = 10
        , z_dim = 32
        , batch_size = BATCH_SIZE
        , n_tracks = n_tracks
        , n_bars = n_bars
        , n_steps_per_bar = n_steps_per_bar
        , n_pitches = n_pitches
        )
    gan.load_weights(RUN_FOLDER, None)
    generator_summary = gan.generator.summary()
    critic_summary = gan.critic.summary()
    sum_dict = {
        "generator": generator_summary, 
        "critic": critic_summary
    }
    return sum_dict

def muse_gan_compose_write_to_midi():
    data_binary = load_music_binary()
    ## museGAN network object
    gan = MuseGAN(input_dim = data_binary.shape[1:]
        , critic_learning_rate = 0.001
        , generator_learning_rate = 0.001
        , optimiser = 'adam'
        , grad_weight = 10
        , z_dim = 32
        , batch_size = BATCH_SIZE
        , n_tracks = n_tracks
        , n_bars = n_bars
        , n_steps_per_bar = n_steps_per_bar
        , n_pitches = n_pitches
        )
    # load trained weights onto object
    gan.load_weights(RUN_FOLDER, None)
    #
    chords_noise = np.random.normal(0, 1, (1, gan.z_dim))
    style_noise = np.random.normal(0, 1, (1, gan.z_dim))
    melody_noise = np.random.normal(0, 1, (1, gan.n_tracks, gan.z_dim))
    groove_noise = np.random.normal(0, 1, (1, gan.n_tracks, gan.z_dim))
    #
    gen_scores = gan.generator.predict([chords_noise, style_noise, melody_noise, groove_noise])
    #
    np.argmax(gen_scores[0,0,0:4,:,3], axis = 1)
    #
    gen_scores[0,0,0:4,60,3] = 0.02347812
    #
    timestamp = datetime.datetime.now().strftime("%m-%d-%Y.%H-%M-%S")
    unique_id = str(uuid.uuid4())
    filename = timestamp + "_" + unique_id
    gan.notes_to_midi(RUN_FOLDER, gen_scores, filename)
#    gen_score = converter.parse(os.path.join(RUN_FOLDER, 'samples/{}.midi'.format(filename)))
#    gen_score.show()
    return 

# Fetch the actual midi file
def fetch_midi(filepath):
    midi_file = fetch_midi_file(filepath)
    return midi_file

def create_wav_with_midi(midi_filepath):
    # print('___________________  create_wav_with_midi  ___________________')
    fs = FluidSynth()
    # print('___________________  fs  ___________________')
    # print(fs)    
    wav_filepath = wav_filepath_out_of_midi_filepath(midi_filepath)

    # try:
    #     print('___________________  command method env var setup ___________________')
        
    #     # command = 'export LD_LIBRARY_PATH=/usr/local/lib64'
    #     # print(command)
    #     # process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    #     # output, error = process.communicate()
    #     # print('___________________  output  ___________________')
    #     # print(output)
        
    #     # print('___________________  command method  ___________________')
    #     # command = 'fluidsynth -F compose/tmp/changing_chords.wav /usr/local/share/soundfonts/default.sf2 compose/run/0018_chorales/samples/changing_chords.midi'
    #     command = 'fluidsynth -F ' + wav_filepath + ' /usr/local/share/soundfonts/default.sf2 ' + midi_filepath #compose/run/0018_chorales/samples/changing_chords.midi'     
    #     print(command)
    #     process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    #     output, error = process.communicate()
    #     print('___________________  output  ___________________')
    #     print(output)
    # except: 
    print('___________________  fs.midi_to_audio commencing  ___________________')
    fs.midi_to_audio(midi_filepath, wav_filepath)
    print('___________________  fs.midi_to_audio completed  ___________________')
    ####
    return wav_filepath

def wav_filepath_out_of_midi_filepath(midi_filepath):
    # print('___________________  wav_filepath_out_of_midi_filepath  ___________________')
    wav_filepath = midi_filepath
    if midi_filepath.endswith('mid'):
       wav_filepath = midi_filepath[:-len('mid')]
    if midi_filepath.endswith('midi'):
       wav_filepath = midi_filepath[:-len('midi')]
    if not wav_filepath.endswith('.'):
       wav_filepath =  wav_filepath + '.'
    wav_filepath = wav_filepath + 'wav'
    return wav_filepath


##
##
## The main function on the application. Compose track and write to midi.
##
def compose_midi(compose_type = ''):
    data_binary = load_music_binary()
    ## museGAN network object
    gan = MuseGAN(input_dim = data_binary.shape[1:]
        , critic_learning_rate = 0.001
        , generator_learning_rate = 0.001
        , optimiser = 'adam'
        , grad_weight = 10
        , z_dim = 32
        , batch_size = BATCH_SIZE
        , n_tracks = n_tracks
        , n_bars = n_bars
        , n_steps_per_bar = n_steps_per_bar
        , n_pitches = n_pitches
        )
    # load trained weights onto object
    gan.load_weights(RUN_FOLDER, None)

    # noise
    chords_noise = np.random.normal(0, 1, (1, gan.z_dim))
    style_noise = np.random.normal(0, 1, (1, gan.z_dim))
    melody_noise = np.random.normal(0, 1, (1, gan.n_tracks, gan.z_dim))
    groove_noise = np.random.normal(0, 1, (1, gan.n_tracks, gan.z_dim))
    #
    
    #
    # Optional compose type parameter
    # If not specified make changes to the noise
    #
    if compose_type == 'changing_chords':
        chords_noise = 5 * np.ones((1, gan.z_dim))
    elif compose_type == 'changing_style': 
        style_noise = 5 * np.ones((1, gan.z_dim))
    elif compose_type == 'changing_melody':
        melody_noise = np.copy(melody_noise)
        melody_noise[0,0,:] = 5 * np.ones(gan.z_dim) 
    elif compose_type == 'changing_groove':
        groove_noise = np.copy(groove_noise)
        groove_noise[0,3,:] = 5 * np.ones(gan.z_dim)
    
    gen_scores = gan.generator.predict([chords_noise, style_noise, melody_noise, groove_noise])

    np.argmax(gen_scores[0,0,0:4,:,3], axis = 1)
    gen_scores[0,0,0:4,60,3] = 0.02347812
    
    timestamp = datetime.datetime.now().strftime("%m-%d-%Y.%H-%M-%S")
    unique_id = str(uuid.uuid4())
    filename = "compose.io_" + timestamp + "_" + unique_id
    
    filepath = gan.notes_to_midi(WRITE_FOLDER, gen_scores, filename)

    ## TODO: Consider maybe adding score image file later <-- actually do this
    return filename, filepath 
