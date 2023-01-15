
class ADCS:

    # initialization method (like a constructor)
    def __init__(self, param1, param2):
        # examples of setting class attributes/fields
        self.attribute1 = param1
        self.attribute2 = param2
        self.attribute3 = 2         # don't need to get all the values externally


    # example method
    def my_method(self, param1):    # needs a "self" parameter
        print("hello")


# creating an instance of an "ADCS" type object called "adcs"
adcs = ADCS("something", "something else")

# calling the "my_method" method on our ADCS instance
adcs.my_method("param_value")

# demonstrating accessing an attribute from a class instance
print(adcs.attribute1)  