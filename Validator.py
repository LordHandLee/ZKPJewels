import pickle

class Validator:
    def __init__(self) -> None:
        self.jewel = None
        self.validation_string = "abcd" # randomly generated string
    
    def validate(self, jewel_object):
        jewel_object = pickle.loads(jewel_object)
        print(self.validation_string)
        jewel = jewel_object # get the object
        jewel.load_input(self.validation_string) # load the input string
        return pickle.dumps(jewel) # return the jewel object
    
    def validated(self, jewel_object, jewel_string):
        jewel_object = pickle.loads(jewel_object)
        print(jewel_string, self.validation_string)
        if jewel_string == self.validation_string:
            print("Jewel successfully validated.")
            return pickle.dumps(jewel_object)
        else:
            return "Jewel was unsuccesfully validated."