import pickle
import os


class Save_Load_Manager:
    def __init__(self, file_extension: str, save_folder: str):
        self.file_extension = file_extension
        self.save_folder = save_folder

    def save(self, game, name: str):
        # Extract the meta data from the game to pickle
        player_data = {}
        shop_data = {}
        timing_data = {}
        data = {'player': player_data,
                'shop': shop_data,
                'time': timing_data}

        # Create new file with 'write byte' mode
        data_file = open(self.save_folder + '/' + name + self.file_extension, 'wb')

        # Pickle the meta data
        pickle.dump(data, data_file)

    def load(self, name):
        # Open file in 'read byte' mode
        data_file = open(self.save_folder + '/' + name + self.file_extension, 'rb')

        # Load the meta data
        data = pickle.load(data_file)

        # Give the data to the game

        return data