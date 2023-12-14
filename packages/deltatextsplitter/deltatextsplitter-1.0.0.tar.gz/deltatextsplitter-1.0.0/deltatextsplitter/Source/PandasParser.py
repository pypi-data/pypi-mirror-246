"""
Module for the PandasParser-function, a member function of the documentclass.
"""

# Import Python base-functionality:

# Import third-party software:
import pandas

# import relevant parts from pdftextsplitter:
from pdftextsplitter import texttype
from pdftextsplitter import enum_type


# Function definition of converting enumerations:
def get_maintype(enum_identifcation: texttype) -> str:
    """
    Converts the main texttype (headlines, enumeration, etc.)
    from a python enumeration into a human-readable string.

    # Parameters: enum_identifcation: texttype: the enumeration to convert.
    # Returns: str: the human-readable string:
    """

    # Begin by declaring the answer:
    answer = "Unknown"

    # Move through all options:
    if enum_identifcation == texttype.TITLE:
        answer = "Title"
    elif enum_identifcation == texttype.FOOTER:
        answer = "Header/Footer"
    elif enum_identifcation == texttype.BODY:
        answer = "Body"
    elif enum_identifcation == texttype.HEADLINES:
        answer = "Headline"
    elif enum_identifcation == texttype.ENUMERATION:
        answer = "Enumeration"

    # Return the answer:
    return answer


# Function definition of converting enumerations:
def get_headlines_type(cascadelevel: int) -> str:
    """
    Converts the cascadelevel into a human-readable string like
    chapter, section, etc.

    NOTE: This function can only be used IF the maintype is
    identified as a Headline/texttype.HEADLINES.

    # Parameters: cascadelevel: int: the cascadelevel to convert.
    # Returns: str: the human-readable string:
    """

    # Begin by declaring the answer:
    answer = "Unknown"

    # Move through all options:
    if cascadelevel == 0:
        answer = "Title"
    elif cascadelevel == 1:
        answer = "Chapter"
    elif cascadelevel == 2:
        answer = "Section"
    elif cascadelevel == 3:
        answer = "Subsection"
    elif cascadelevel == 4:
        answer = "Subsubsection"
    elif cascadelevel > 4:
        answer = "Higher_Order"

    # Return the answer:
    return answer


# Function definition of converting enumerations:
def get_enumtype(enum_identifcation: enum_type) -> str:
    """
    Converts the enumeration-type (an python-enumeration)
    into a human-readable string like Bigroman, Bigletter, etc.

    NOTE: This function can only be used IF the maintype is
    identified as an Enumeration/texttype.ENUMERATION.

    # Parameters: enum_identifcation: enum_type: the enumeration to convert.
    # Returns: str: the human-readable string:
    """

    # Begin by declaring the answer:
    answer = "Unknown"

    # Move through all options:
    if enum_identifcation == enum_type.BIGROMAN:
        answer = "Bigroman"
    elif enum_identifcation == enum_type.SMALLROMAN:
        answer = "Smallroman"
    elif enum_identifcation == enum_type.BIGLETTER:
        answer = "Bigletter"
    elif enum_identifcation == enum_type.SMALLLETTER:
        answer = "Smallletter"
    elif enum_identifcation == enum_type.DIGIT:
        answer = "Digit"
    elif enum_identifcation == enum_type.SIGNMARK:
        answer = "Signmark"

    # Return the answer:
    return answer


# Main function definition:
def PandasParser_documentclass(self):
    """
    This function will transform the outcomes of a pdftextsplitter-analysis
    into a pandas dataframe, as created in the documentclass.

    NOTE: The user must take care that there is actually some output to parse
    in the splitter-instance. So run self.splitter.process() before this
    function!

    # Parameters: None (taken from the class.)
    # Return: None (stored in the class.)
    """

    # Before we do anything: clear out the pandas dataframe:
    self.outcomes = pandas.DataFrame(columns=self.columns)

    # Begin by verifying that there is some content to parse:
    if len(self.splitter.textalineas) == 0:
        print("You cannot run this function if the splitter-instance")
        print("has no textalineas-content. provide one by running")
        print("process() on the splitter-instance yourself first.")
    else:
        # then, we can proceed. Loop over the textalineas:
        alineaindex = -1

        for alinea in self.splitter.textalineas:
            # First indrease the index:
            alineaindex = alineaindex + 1

            # begin by extracting types:
            maintype = get_maintype(alinea.alineatype)
            subtype = "Unknown"
            if maintype == "Headline":
                subtype = get_headlines_type(alinea.textlevel)
            elif maintype == "Enumeration":
                subtype = get_enumtype(alinea.enumtype)

            # Begin by creating a single line of the pandas dataframe:
            ThisRow = {
                "NativeID": alinea.nativeID,
                "Version": self.splitter.VERSION,
                "Documentname": self.splitter.get_documentname(),
                "Title": alinea.texttitle,
                "MainType": maintype,
                "SubType": subtype,
                "Cascadelevel": alinea.textlevel,
                "parentID": alinea.parentID,
            }

            # Add it to the existing pandas dataframe.
            self.outcomes.loc[alineaindex] = pandas.Series(ThisRow)

            # That should do the trick!
