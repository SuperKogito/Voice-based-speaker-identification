import os
import pickle
import warnings
import numpy as np
from SilenceEliminator import SilenceEliminator
from FeaturesExtractor import FeaturesExtractor

warnings.filterwarnings("ignore")

# paths to training data & to speaker models
modelpath = "SpeakerModels/"
testpath  = "TestingData"

# collect all Gaussian mixture model paths & load the GMMs
db = {}
for fname in [fname for fname in os.listdir(modelpath) if fname.endswith('.gmm')]:
    speaker     = fname.split('.')[0]
    model       = pickle.load( open(os.path.join(modelpath, fname), 'rb'))
    db[speaker] = model

file_paths = []
# file_paths = [os.path.join(testpath, fname) for fname in os.listdir('TestingData')]
# get file paths
for root, dirs, files in os.walk(testpath):
    for file in files:
        file_paths.append( os.path.join(root, file))

error, total_sample = 0, 0

print("+=======================================================+")
# read the test directory and get the list of test audio files
for path in file_paths[:]:
    if os.path.basename(path).split('_')[0] in db.keys():
        features_extractor = FeaturesExtractor()
        silence_eliminator = SilenceEliminator()

        silence_eliminated_wave_file_path ="temp-" + os.path.basename(path).split('.')[0] + ".wav"
        audio, duration_string = silence_eliminator.ffmpeg_silence_eliminator(path, silence_eliminated_wave_file_path)
        vector                 = features_extractor.accelerated_get_features_vector(path, audio, 8000)

        if vector.shape != (0,):
            print(vector.shape)
            total_sample      += 1
            log_likelihood     = {}
            m                  = {}
            for speaker, model in db.items():
                gmm                     = model
                scores                  = np.array(gmm.score(vector))
                log_likelihood[speaker] = round(scores.sum(), 3)
                m[speaker]              = scores

            max_log_likelihood = max(log_likelihood.values())
            keys, values       = list(log_likelihood.keys()), list(log_likelihood.values())
            winner             = keys[values.index(max_log_likelihood)]

            checker_name = os.path.basename(path).split("_")[0]
            if winner != checker_name:
                error += 1

        print("+-------------------------------------------------------+")
        print("Processed filemame : %10s" % os.path.basename(path))
        print("Expected speaker   : %10s" % os.path.basename(path).split("_")[0])
        print("Identified speaker : %10s" % winner)
        print("+=======================================================+")


accuracy = ((total_sample - error) / total_sample) * 100
print(" %10s || %7s  " % ("THE ACCURACY   ", round(accuracy, 3)))
print("+=======================================================+")
