import utils
import consts

# 1
import my_package.my_mod_1
import my_package.my_mod_2
import my_package.my_folder.my_folder_mod_1

# 2
from my_package import my_mod_2

# 3
from my_package.my_folder.my_folder_mod_1 import my_folder_mod_1_function

# 4
from my_package import *

# 5
from my_package.my_folder import *

import math
import requests
from typing import List, Union, Tuple



def main():
    print("Hello World!", utils.sum(1, 2), consts.YURA_YEARS)
    # 1
    my_package.my_mod_1.my_mod_1_function()
    
    # 4
    my_mod_1.my_mod_1_function()

    # 1
    my_package.my_mod_2.my_mod_2_function()
    
    # 2
    my_mod_2.my_mod_2_function()

    # 1
    my_package.my_folder.my_folder_mod_1.my_folder_mod_1_function()
    
    # 3
    my_folder_mod_1_function()

    # 4
    my_folder.my_folder_mod_1.my_folder_mod_1_function()
    
    # 5
    my_folder_mod_1.my_folder_mod_1_function()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()