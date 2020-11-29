#

from collection import CollectionWrite
from market import Jasdaq

if __name__ == '__main__':
    # Get companies code of Jasdaq from jasdaq.txt file
    jasdaq = Jasdaq()

    # Get stock collection data and save stock file
    iw = CollectionWrite()
    iw.get_incomes(jasdaq)
