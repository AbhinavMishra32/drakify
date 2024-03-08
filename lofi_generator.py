from effects.drakify import drakify
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import subprocess

def check_lofi_generated(normal_path, lofi_path) -> list:
    normal_songs = [song for song in os.listdir(normal_path) if song.endswith('.wav')]
    lofi_songs = [song[:-9] for song in os.listdir(lofi_path) if song.endswith('.wav')] #:-23
    unmatched_songs = [song for song in normal_songs if song[:-4] not in lofi_songs]
    if unmatched_songs == []:
        print("All songs have been made lofi")
        exit(0)
    return unmatched_songs

def generate_lofi(songs_list, folderpath, savepath="source/songs/slowed_songs/"):
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    for song in songs_list:
        drakify(os.path.join(folderpath, song), wet = 0.35)  # Use os.path.join for path concatenation
        shutil.move(
            os.path.join(folderpath, song[:-4] + "_drakify_normalized.wav"),
            os.path.join(savepath, song[:-4] + "_lofi.wav")
        )
        print(f"Song {songs_list.index(song)+1} out of {len(songs_list)} done")

def concatenate_wav_files(input_folder, output_file):
    # Get a list of all files in the input folder
    input_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.wav')]
    
    # Check if there are any WAV files in the folder
    if not input_files:
        print("No WAV files found in the input folder.")
        return
    
    # Check if the output file already exists. If so, delete it.
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Concatenate the input files into the output file
    subprocess.run(['sox'] + input_files + [output_file])

def delete_files_in_folder(folder_path):
    # Iterate over all files in the folder
    for file_name in os.listdir(folder_path):
        # Construct the full file path
        file_path = os.path.join(folder_path, file_name)
        # Check if the file is a regular file (not a directory)
        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)

if __name__ == "__main__":
    songs_folder = "source/songs/normal_songs/" #normal songs folder path
    save_path = "source/songs/slowed_songs/" #lofi songs folder path
    songs = check_lofi_generated(songs_folder, save_path) #gives list of only those songs who havent been made in lofi
    print("Songs not made lofi: ", songs)

    # with ThreadPoolExecutor(max_workers=4) as executor:  # Limiting to 4 threads
    #     executor.map(generate_lofi, [songs[i:i+4] for i in range(0, len(songs), 4)], [songs_folder]*len(songs))
    generate_lofi(songs, songs_folder, save_path)

    concatenate_wav_files(save_path, "source/songs/lofi_songs.wav")

    print("Lofi songs created successfully at source/songs/lofi_songs.wav")
