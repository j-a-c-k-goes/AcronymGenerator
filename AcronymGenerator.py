import sys
import string
import random
from collections import defaultdict

class Input:
    corpus = "/usr/share/dict/web2"
    acronym_dictionary = dict()
    def __init__( self ):
        self.current_acronym = None
    def get( self ): return self.current_acronym
    def set( self, new_acronym ): self.current_acronym = new_acronym
    def invalid_character_check( self, acronym_to_check:str ):
        string_has_invalid_characters = True
        alphabets = list( string.ascii_lowercase )
        numbers = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" ]
        alpha_numbers = alphabets + numbers
        for char in acronym_to_check:
            if char.lower() not in alpha_numbers:
                print( char, "is an invalid character. Input fails check." )
                string_has_invalid_characters = True
                return string_has_invalid_characters
        for char in acronym_to_check:
            if char.lower() in alpha_numbers:
                print( char, "is a valid character. Input passes check." )
                string_has_invalid_characters = False
        return string_has_invalid_characters
    def check_if_only_numbers( self, acronym_to_check:str ):
        print( "Checking if the input consists of only numbers.\n" )
        input_consists_of_only_numbers = True
        number_strings = ( "0", "1", "2", "3", "4", "5", "6", "7", "8", "9" )
        length_of_check = len( acronym_to_check )
        checked_characters = list()
        for char in acronym_to_check:
            for num in number_strings:
                if char == num:
                    print( char, "is a number. Remembering this." )
                    checked_characters.append( char )
        if ( ( len( checked_characters ) ) == ( len( acronym_to_check ) ) ):
            print( acronym_to_check, "consists of only numbers. This is not allowable.\n" )
        else:
            print( acronym_to_check, "passes the number-only check.\n" )
            input_consists_of_only_numbers = False
        return input_consists_of_only_numbers
    def check_if_correct_length( self, acronym_to_check:str ):
        print( "Checking is acronym is two characters or more." )
        input_is_correct_length = False
        if ( len(acronym_to_check) >= 2 ):
            print( acronym_to_check, "passes the length check.\n" )
            input_is_correct_length = True
        else:
            print( acronym_to_check, "fails the length check.\n" )
        return input_is_correct_length
    def isolate( self, acronym:str ):
        isolated_characters = list()
        for char in self.get():
            isolated_characters.append( char )
        return isolated_characters
    def create_word_map( self, acronym ):
        """ Counter-value being used as method to allow duplicate keys.
            Some acronyms, ABA, have duplicate characters. 
            By default, a dictionary cannot have duplicate keys.
            So, saving key for "ABA" as A_0, B_1, A_2.
        """
        acronym_as_list = self.isolate( acronym )
        acronym_dictionary = dict()
        counter = 0
        for letter in acronym_as_list: 
            # Establish dictionary's keys.
            key_name = f"{ letter.upper() }_{ counter }"
            acronym_dictionary[ key_name ] = list()
            counter += 1
        counter = 0
        for letter in acronym_as_list:
            # Establish dictionary's values.
            key_name = f"{ letter.upper() }_{ counter }"
            with open ( self.corpus, "r" ) as source:
                for line in source:
                    if letter.lower()[0] == line.strip().lower()[ 0 ]:
                        acronym_dictionary[ key_name ].append( line.strip() )
            counter += 1
        return acronym_dictionary
    def generate_acronym( self ):
        acronym = self.get()
        word_map = self.create_word_map( acronym )
        generated_acronym = ""
        for key, value in word_map.items():
            generated_acronym += random.choice( ( value ) ).upper() + " "
        return generated_acronym.rstrip()
    def generate_acronyms( self, generations_needed:int=10 ):
        generated_acronyms = list()
        for i in range( int( generations_needed ) ):
            generation = self.generate_acronym()
            generated_acronyms.append( generation )
        return generated_acronyms
    def display_generated_acronyms(self, generated_acronym_list ):
        print("Acronyms:\n")
        for index, word in enumerate(generated_acronym_list):
            print( "\t", index, "\t", word )
    def make( self ):
        def reprompt_msg():
            print( "Enter a valid acronym.\n" )
        input_mode = True
        while ( input_mode ):
            acronym = str( input( "Enter an acronym: " ) )
            if self.check_if_only_numbers( acronym ) == True:
                reprompt_msg()
            elif self.invalid_character_check( acronym ) == True:
                reprompt_msg()
            elif self.check_if_correct_length( acronym ) == False:
                reprompt_msg()
            else:
                self.set( acronym.upper() )
                input_mode = False; break

if __name__ == "__main__":
    Input = Input()
    Input.make()
    generations = Input.generate_acronyms( int( sys.argv[ 1 ] ) )
    Input.display_generated_acronyms( generations )
    