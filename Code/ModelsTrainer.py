import os
import pickle
import warnings
import numpy as np
from sklearn.mixture import GMM
from FeaturesExtractor import FeaturesExtractor
from SilenceEliminator import SilenceEliminator

warnings.filterwarnings("ignore")

# initializatiions
gmm_destination = "SpeakerModels/"
trainpath       = "TrainingData"
file_paths      = []

try:
    os.mkdir(gmm_destination)
except:
    pass

# get file paths
for root, dirs, files in os.walk(trainpath):
    speaker_file_paths = []
    for file in files:
        speaker_file_paths.append( os.path.join(root, file) )
    if speaker_file_paths != []:
        file_paths.append(speaker_file_paths)

# extracting features for each speaker (5 files per speakers)
for files in file_paths:
    features = np.asarray(())
    for filepath in files:
        print (filepath)

        # extract voice features
        features_extractor = FeaturesExtractor()
        silence_eliminator = SilenceEliminator()

        try   :
            silence_eliminated_wave_file_path = "temp-" + os.path.basename(filepath).split('.')[0] + ".wav"
            audio, duration_string = silence_eliminator.ffmpeg_silence_eliminator(filepath, silence_eliminated_wave_file_path)
            vector                 = features_extractor.accelerated_get_features_vector(filepath, audio, 8000)
        except:
            continue

        if features.size == 0:
            features = vector
        else:
            try:
                features = np.vstack((features, vector))
            except:
                print("ValueError: Shape mismatch")

    # adapt gmm
    gmm = GMM(n_components = 16, n_iter = 200, covariance_type='diag', n_init = 3)
    gmm.fit(features)

    # dumping the trained gaussian model
    picklefile = gmm_destination + os.path.basename(filepath).split('_')[0] + ".gmm"
    with open(picklefile, 'wb') as gmm_file:
        pickle.dump(gmm, gmm_file)


    print ('+ modeling completed for speaker:', picklefile," with data point = ", features.shape )
