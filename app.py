import os
import re
import logging
import time
import concurrent.futures
from faster_whisper import WhisperModel

# Set OpenMP to use a single thread
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["MKL_THREADING_LAYER"] = "GNU"


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the faster-whisper model globally
model = WhisperModel("small", device="auto", compute_type="int8") 

# Function to check if the whisper file should be processed
def is_valid_file(whisper_file):
    match = re.match(r".*-(\d{8})-.*", whisper_file)
    if match and int(match.group(1)) >= 20240700:
        return True
    return False

# Function to transcribe a single file
def transcribe_file(whisper_file, resources_folder):
    temp_path_file = os.path.join(resources_folder, whisper_file)
    try:
        start_time = time.time()
        segments, _ = model.transcribe(temp_path_file, beam_size=5, language='es')
        transcription = " ".join(segment.text for segment in segments)
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f'{whisper_file}: done (Duration: {duration:.2f} seconds)')
        return f'{whisper_file}: {transcription} (Duration: {duration:.2f} seconds)'
    except Exception as error:
        logging.error(f'{whisper_file}: error {error}')
        return None

# Function to read and transcribe whisper files
def read_whisper_files():
    cwd = os.getcwd()
    resources_folder = os.path.join(cwd, 'resources/audios')
    
    whisper_files = [f for f in os.listdir(resources_folder) if is_valid_file(f)]
    whisper_files.sort()
    
    # Use a ThreadPoolExecutor for multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        # Create a future for each transcription task only for valid files
        futures = {executor.submit(transcribe_file, whisper_file, resources_folder): whisper_file for whisper_file in whisper_files}
        
        with open("results.txt", "w") as txt:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:  # Only write to file if the result is not None
                    txt.write(result + '\n')
                else:
                    logging.warning(f'{futures[future]}: transcription skipped or failed')

read_whisper_files()
