import pickle
import os


class Save_Load_Manager:
    def __init__(self, file_extension: str, save_folder: str):
        self.file_extension = file_extension
        self.save_folder = save_folder

    def save(self, game, name: str):
        """ Extracts the needed meta data from the game and pickles it """
        # Extract player data
        player = game.player
        player_data = {'coins': player.coins,
                       'max_health': player.max_health,
                       'health': player.health,
                       'stamina': player.stamina_float,
                       'max_stamina': player.max_stamina,
                       'attack_1_damage': player.damages['attack_1'],
                       }

        # Extract shop data
        shop_menu = game.level_manager.levels['0-1'].entity_manager.shop_object[0].shop_menu
        shop_data = {'upgrade_costs': shop_menu.stat_upgrade_costs,
                     'stat_upgrades': shop_menu.stat_upgrades}

        # Extract timer data
        timer = game.level_manager.time_manager
        timing_data = {'best_times': timer.best_times,
                       'medals': timer.medals}

        # Packge up the data
        data = {'player': player_data,
                'shop': shop_data,
                'time': timing_data}

        # Create new file with 'write byte' mode
        data_file = open(self.save_folder + '/' + name + self.file_extension, 'wb')

        # Pickle the meta data and dump to the new file
        pickle.dump(data, data_file)

    def load(self, name):
        # Open file in 'read byte' mode
        data_file = open(self.save_folder + '/' + name + self.file_extension, 'rb')

        # Load the meta data
        data = pickle.load(data_file)

        # Give the data to the game
        return data