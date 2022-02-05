from Jewel import Jewel
import rsa
import random
import string
import json


#publickKey, privateKey = rsa.newkeys(512)

class Minter:
    """Mint 1000 Jewels"""
    """Minter needs to generate a set of private and public keys along with
    identifier to original purchaser of coin so they can encryp/decrypt messages"""
    def __init__(self) -> None:
        self.__all_jewels = {} # empty dict
        self.publicKey, self.privateKey = rsa.newkeys(512)
        #self.y = 
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        letters = string.ascii_letters
        digits = string.digits
        punctuation = string.punctuation
        self.random_chars = [lower, upper, letters, digits, punctuation]
        self.random_string = ""
        self.y = None
        #for _ in range(20):
            #self.random_string += random.choice(random.choice(self.random_chars))

        # for i in range(1000000000): # 1 billion
        #     self.__all_jewels[i]
        print(self.random_string)
        print(len(self.random_string))
    def generate_rand_strings(self): # right now generate 1 billion jewels
        """Generate 1 billion random strings used to seed 1 billion"""
        """Genertes 1 billion jewels"""
        """TODO: Generate 1 billion jewels of different denominations starting
        with degree 1000 for diamond and subtracting degree -x10 per level of hierarchy
        which is 6. 1000, 100, 20, 10, 5, 1."""
        for _ in range(100):#for _ in range(1000000000): # 1 billion
            random_string = "" #empty string
            for _1 in range(20):
                random_string += random.choice(random.choice(self.random_chars)) #populate empty string with random chars
            random_string = random_string.encode('utf-8')
            key = self.encrypt_rand_str(bytes(random_string)) #encrypt random string
            #print(key)
            jewel_public, jewel_private = rsa.newkeys(512)
            self.__all_jewels[key] = Jewel(jewel_public, random_string) # each Jewel has its own public key used to encrypt messages
            # adds to self.__all_jewels
            # request to send private key to wallet paired with hashed wallet ID for wallet to store Jewel in dictionary
            #store private key hashed to Jewel ID/key as value

    def encrypt_rand_str(self, the_string):
        #print(the_string, self.publicKey)
        key = rsa.encrypt(the_string, self.publicKey) # key is random encrypted string
        return key.decode('latin-1')
    def list_jewels(self):
        print(self.__all_jewels)
        # for i in self.__all_jewels.keys():
        #     print(i.encode('latin-1'))
    def dump_to_file(self):
        self.y = json.dumps(self.__all_jewels)
    def write_jewels_tofile(self):
        self.dump_to_file()
        with open("jewels.json", "w") as file:
            file.write(self.y)
    
    

minted = Minter()
#print(minted)
minted.generate_rand_strings()
minted.list_jewels()
minted.write_jewels_tofile()