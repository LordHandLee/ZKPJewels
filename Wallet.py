import base64
#from copyreg import pickle
import pickle
import rsa
import os
import time
import copy
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

class Wallet:
    """Gets ledger from Minter when purchasing jewels. Your password unlocks/decrypts ledger."""
    aa = "hello"
    def __init__(self) -> None:
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.self_path = self.dir_path + "/running/"
        self.pickle_path = self.self_path + "wallet_pickle.pkl"
        self.salt = b'\xff\xb4\xbc\x03C\r\x118\x9d\xa3%m\x81\xb5\xd2\xc0'
        if not os.path.exists(self.self_path): # doesnt exist, make the path
            os.makedirs(self.self_path)
            self.message = "Ethan Lee".encode()
            self.ledger = "/Wallet/ledger.dat"
            self.universalKey = "abc"
            print("the salt", self.salt)
            self.password = self.ask_user_pass() #'password'.encode()
            print(self.password)
            self.unique_id = "asdf"#randomly generate unique id
            self.address = "dsafas" #randomly generated address
            self.balance = 0
            self.jewel_list = [] #get list from ledger
            #after initalizing, save state to pickle file
            print("locking the wallet ")
            self.save_state = self.lock_wallet()
        else: # else for everything in the path, look for wallet pickle file
            for i in os.listdir(self.self_path):
                if i == "wallet_pickle.pkl":
                    with open(self.pickle_path, 'rb') as pkl:
                        print()
                        print("ohshit:                                            ", pkl.read())
                        #wallet = pickle.load(pkl)
                        self.password = self.ask_user_pass()#get password
                        d_file = self.unlock_wallet()#unlock wallet
                        wallet = pickle.loads(d_file)
                        print("HAHAHAH, L : ", wallet)
                        print(wallet.__dict__)
                        #wallet.set_balance()#set the balance
                        #self.__dict__.update(wallet)
                        self.__dict__ = wallet.__dict__
                        #return wallet
                        #return wallet#return wallet


        # use hashed password
        # password unlocks wallet
        # wallet has its own keys, generates new ones each time is opened
        # encrypts/decrypts ledger with new keys each time .....needs way to make backup in case power goes out in middle of process
        # Minter generates new set of keys to be given to wallet. Wallet unlocks ledger, makes it own keys and adds info to its ledger
        # each ledger file is encrypted and contains pickle objects.
        # If user sends jewels to another user, keys are sent along with ledger and new ones are created.
        # Check for ledger. if ledger, dont generate new keys. Use existing ones.

        # Never decrypt files....always read encrypted file and then decrypt...Write new info to new encrypted file.
        # with open(self.ledger) as ledger: #open ledger
        #     ledger_files = ledger.readlines()
            
        pass
    def get_balance(self):
        print(self.balance)
        pass
    def set_balance(self, num):
        #loop thru ledger and get count of all jewel ids
        self.balance += num
        self.lock_wallet()
        #self.open_ledger = open(self.ledger, "r") # open the ledger
        pass
    def send_jewel(self):
        #select first jewel from list
        jewel_2_send = self.jewel_list[0]
        recipient_addr = self.get_recipient_addr()#get the address
        print(recipient_addr)
        pass
    def send_jewels(self, amount):
        """Send request to server containing jewels and recipient address."""
        recipient_addr = self.get_recipient_addr()#get the address
        print(recipient_addr)
        #send query containing address and jewel/s.
        pass
    def receive_jewels(self, ledger):
        """Merge the ledgers."""
        pass
    def listen_for_jewels(self):
        """Send periodic queries to server. Once we receive ledger from query, merge ledgers."""
        """This needs to be in a thread."""
        #while True:
            #send query
            #if query returns ledger:
                #receive ledger
                #self.receive_jewels()
                #self.set_balance()
            #time.sleep(60)
        pass
    def display_address(self):
        print(self.address)
        pass
    def ask_user_pass(self):
        password = input("Please enter your passsword: ")
        return password
        pass
    def get_recipient_addr(self):
        addr = input("Please enter the address of the user whom you would like to send a/some jewel/s: ")
        return addr
    def copy_self(self):
        return copy.deepcopy(self)
    def lock_wallet(self):
        """Encrypts the ledger, pickles itself, and encrypts the pickle file. Then exits?"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256,
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        print("password: ", bytes(self.password, encoding="utf-8"))
        key = base64.urlsafe_b64encode(kdf.derive(bytes(self.password, encoding="utf-8"))) #use password to lock wallet and encrypt files
        #print(self.key)
        cipher = Fernet(key)
        print(key)
        clone = self.copy_self()#make copy of self
        print("key!!!!: ", key)
        clone = pickle.dumps(clone)
        clone = cipher.encrypt(clone) #encrypt the clone
        with open(self.pickle_path, "wb") as clone1:
            clone1.write(clone)
            #cipher.encrypt(self.ledger), cipher.encrypt(clone)
        #clone = pickle.dump(clone, self.pickle_path, 'w') # create pickle file
        # read, encrypt, write
        #cipher.encrypt(self.ledger), cipher.encrypt(clone) # encrypt ledger and pickle files
        return "LOCKED"
    def unlock_wallet(self):
        print("unlock wallet pword: ", self.password)
        print(self.salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256,
            length=32,
            salt=self.salt,
            iterations=100000,
            backend=default_backend()
        )
        #user_pass = "password".encode()
        #user_pass = self.password
        user_key = base64.urlsafe_b64encode(kdf.derive(bytes(self.password, encoding="utf-8")))  #(kdf.derive(self.password.encode())) #use password to unlock wallet and decrypt files
        print("key!!!!: ", user_key)
        user_cipher = Fernet(user_key)
        #open what in the file first, then decrypt
        with open(self.pickle_path) as pickle_p:
            #print("yeehaw", pickle_p.read().encode())
            yeehaw = pickle_p.read().encode()
            print("WHAT: ", yeehaw)
            decrypted_file = user_cipher.decrypt(yeehaw)
            #decrypted_file = base64.urlsafe_b64decode(user_cipher.decrypt(pickle_p.read().encode())) # decrypt the files
            print(decrypted_file)
            #decrypted_file = pickle.loads(decrypted_file)
            print(decrypted_file)
            return decrypted_file#"UNLOCKED"
    def read_wallet(self):
        self.unlock_wallet()
        #read files
        pass
    def write_wallet(self):
        #write files
        self.lock_wallet()
        pass
    def get_user_input(self):
        commands = ["help", "balance", "send", "receive", "exit"]
        while True:
            choice = input("Type 'help' for a list of commands or enter the command now: ")
            if choice == "help":
                #display list of commands
                for i in commands:
                    print(i)
                pass
            if choice == "balance":
                self.get_balance()
                pass
            if choice == "send":
                while True:
                    try:
                        num_jewels = abs(int(input("How many jewel/s do you want to send: ")))
                        if num_jewels > 1 and num_jewels >= len(self.jewel_list):
                            self.send_jewels(num_jewels) #gets the first X amount of jewels to send from the jewel_list
                            break
                        elif num_jewels == 1:
                            print(num_jewels)
                            self.send_jewel()
                            break
                        elif num_jewels == 0:
                            break
                    except ValueError:
                        print("Please enter a number specifying the amount of jewel/s you want to send: ")#int(input("Please enter a number specifying the amount of jewel/s you want to send: "))
                        continue
                    else:
                        num_jewels = int(input("Please enter a number specifying the amount of jewel/s you want to send: "))
                        print(num_jewels)
                        break

                #pass
            if choice == "receive":
                # wait and listen for jewels
                pass
            if choice == "exit":
                #create new key and encrypt wallet with new key, delete old files
                exit()
            if choice == "ubalance":
                num = input("Please enter the amount of jewels you would like to send: ")
                self.set_balance(num)

if __name__ == "__main__":
    wallet = Wallet()
    wallet.get_user_input()