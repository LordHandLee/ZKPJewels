import rsa
import pickle
from Validator import Validator


publickKey, privateKey = rsa.newkeys(512)
print("PRivate key: ", privateKey)
message = "If you can read this, you are rich. Congratulations."
#encMessage = rsa.encrypt(message.encode(), publickKey)

class Jewel():
    def __init__(self, publicKey, id) -> None:
        self.__test_string = None
        self.__publicKey = publicKey
        self.__id = id
    def __encrypt_string(self, input_string):
        #encrypt self.__test_string(input_string)
        self.__test_string = rsa.encrypt(input_string.encode(), self.__publicKey)
        pass
    def decrypt_string(self, *key):
        #decrypts_string
        if not key: # or key is wrong # or encryption status is False
            return "Incorrect"
        else:
            #print(self.__test_string)
            #print(key[0][0], "key")
            return rsa.decrypt(self.__test_string, key[0][0]).decode("utf-8")
    def load_input(self, input_string):
        self.__encrypt_string(input_string)
    def acknowledge_input(self, *key):
        """Used to check the result/status of input string"""
        #print(self.__test_string)
        #self.__test_string = self.decrypt_string(self.__test_string, key)
        decrypted_string = self.decrypt_string(key)
        return decrypted_string
    def get_id(self):
        return self.__id
    
if __name__ == "__main__":
    ruby = Jewel(publickKey, 1)
    validator = Validator()

    pickled_ruby = pickle.dumps(ruby) #pickle the jewel

    validated_jewel = pickle.loads(validator.validate(pickled_ruby))
    validator_input = validated_jewel.acknowledge_input(privateKey)
    final_jewel = validator.validated(pickle.dumps(validated_jewel), validator_input) #unpickled the jewel
    print(final_jewel)


    # ruby.load_input(message)
    # ruby.acknowledge_input(privateKey)
    # #print(privateKey)
    # #print(ruby.decrypt_string(privateKey))