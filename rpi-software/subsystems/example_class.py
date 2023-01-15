# 'EXAMPLE' = name of subsystem

# use this file to help build your subsystem classes and learn how to use them

# this is ~only~ a syntax refresher, not a guide to everything your class needs

class EXAMPLE:

    # initialization method (like a constructor)
    def __init__(self, param1, param2):
        """Creates a COMMS object, assigns attribute/field values.

        Arguments:
            param1 (type): description
            param2 (type): description

        Returns:
            Type: description
        
        """
        self.attribute1 = param1
        self.attribute2 = param2
        self.attribute3 = 2         # don't need to get all the values externally


    def say_hello(self, message):
        """ This is an example method. Methods need a 'self' parameter. 
            Prints the message given.

        Arguments:
            message (str): message to be displayed in the console

        Exceptions:
            No exceptions thrown

        Returns:
            Nothing
        """
        print(message)


# creating an instance of an "EXAMPLE" type object called "example"
example = EXAMPLE("something", "something else")

# calling the "my_method" method on our ADCS instance
example.say_hello("hello world")

# demonstrating accessing an attribute from a class instance
print(example.attribute1)  