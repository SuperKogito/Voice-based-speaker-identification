import os
import math
import tarfile


class DataManager:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def extract_dataset(self, compressed_dataset_file_name, dataset_directory):
        try:
            # extract files to dataset folder
            tar = tarfile.open(compressed_dataset_file_name, "r:gz")
            tar.extractall(dataset_directory)
            tar.close()
            print("Files extraction was successfull ...")

        except:
            print("Ecxception raised: No extraction was done ...")

    def make_folder(self, folder_path):
        try:
            os.mkdir(folder_path)
            print(folder_path, "was created ...")
        except:
            print("Ecxception raised: ", folder_path, "could not be created ...")

    def move_files(self, src, dst, group):
        for fname in group:
            os.rename(src + '/' + fname, dst + '/' + fname)

    def get_fnames_from_dict(self, dataset_dict, key):
        training_data, testing_data = [], []

        # get list lengths
        length_data       = len(dataset_dict[key])
        length_separator  = math.trunc(length_data*2/3)

        # build traing and testing lists
        training_data += dataset_dict[key][:length_separator]
        testing_data  += dataset_dict[key][length_separator:]
        
        return training_data, testing_data

    def manage(self):

        # read config file and get path to compressed dataset
        compressed_dataset_file_name = self.dataset_path
        dataset_directory = compressed_dataset_file_name.split(".")[0]

        # create a folder for the data
        try:
            os.mkdir(dataset_directory)
        except:
            pass

        # extract dataset
        self.extract_dataset(compressed_dataset_file_name, dataset_directory)

        # select females files and males files
        file_names   = [fname for fname in os.listdir(dataset_directory) if ("f0" in fname or "m0" in fname)]
        dataset_dict = {"f0001": [], "f0002": [], "f0003": [], "f0004": [], "f0005": [],
                        "m0001": [], "m0002": [], "m0003": [], "m0004": [], "m0005": [], }

        # fill in dictionary
        for fname in file_names:
            dataset_dict[fname.split('_')[0]].append(fname)

        # divide and group file names
        training_set, testing_set = {},{}

        # make training and testing foldersget_fnames_from_dict
        self.make_folder("TrainingData")
        self.make_folder("TestingData")

        # make folders with speakers ids and move data
        for key in dataset_dict.keys():
            # separate data into training and testing data
            training_set[key], testing_set[key] = self.get_fnames_from_dict(dataset_dict, key)

            # make folders
            self.make_folder("TrainingData/" + key)
            self.make_folder("TestingData/"  + key)

            # move files
            self.move_files(dataset_directory, "TrainingData/" + key, training_set[key])
            self.move_files(dataset_directory, "TestingData/"  + key, testing_set[key])


if __name__== "__main__":
    data_manager = DataManager("SLR45.tgz")
    data_manager.manage()
