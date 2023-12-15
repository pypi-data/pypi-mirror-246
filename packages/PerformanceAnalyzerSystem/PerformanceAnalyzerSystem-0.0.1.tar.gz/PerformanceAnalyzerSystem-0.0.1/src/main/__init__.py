from data_transformer.data_manager_factory import DataManagerFactory
from data_processor.performanceAnalizer import Performance_Analyzer
from data_processor.configuration import Config

LINE = "-----------------------------------------------------------"

def print_title():
    """
    Helps to print title
    :return: None
    """
    print(LINE)
    print("PERFORMANCE ANALYSIS SYSTEM")
    print(LINE)

def get_user_option():
    """
    Helps to get user option
    :return(string): User option
    """
    print("OPTIONS: ")
    print("1. Summary")
    print("2. Export PDF")
    print(LINE)
    return input("Please choose any one of the options below: ")

def validate(user_input):
    """
    Helps to validate user input.
    If the user input is not 1 or 2 throws error
    :param user_input: user_input
    :return: None
    """
    if user_input not in ['1', '2']:
        raise ValueError("Please enter a valid option.")

def get_config(config):
    """
    Helps to get config from user input
    :param config: config
    :return: None
    """
    print("Your configuration file is empty.")
    print("Please enter the values below to create a new configuration file: ")

    # Function to validate user input
    def validate_input(value):
        return value is not None and value.strip() != ''

    # Keep asking for input until valid values are provided
    while not validate_input(config.data_type):
        config.data_type = input("Please enter a data_type: ").upper()

    while not validate_input(config.entity_collection):
        config.entity_collection = input("Please enter an entity_collection_name: ")

    while not validate_input(config.base_field):
        config.base_field = input("Please enter a base_field: ")

    while not validate_input(config.path):
        config.path = input("Please enter path: ")

    computable_fields = ''
    while not validate_input(computable_fields):
        computable_fields = input("Please enter the computable_fields: ")
        config.computable_fields = [field.strip() for field in computable_fields.split(',')]

    # Ask the user for confirmation to proceed
    confirmation = input("Are you sure you want to proceed? (yes/no): ").lower()
    if confirmation != 'yes':
        print("Configuration process canceled.")
        return
        
    config.write_config()

def handle_display(config):
    """
    Handles the main user display screen by co-ordinating the other method
    :param config: config
    :return: None
    """
    config.read_config()
    user_input = get_user_option()
    validate(user_input)
    factory = DataManagerFactory(config)
    entityCollection = factory.call_parser()
    analyzer = Performance_Analyzer(config)
    if user_input == "1":
        analyzer.display(entityCollection)
    else:
        analyzer.export(entityCollection)


def run():
    """
    This is the initial method which co-ordinates all the other method
    to provide user interaction
    :return: None
    """
    config = Config()
    print_title()
    # config.read_config()
    if config.is_valid_config():
        handle_display(config)
    else:
        get_config(config)
        print(LINE)
        print(LINE)
        handle_display(config)

#Test
"""
config = Config()
print_title()
#config.read_config()
if config.is_valid_config():
    handle_display(config)
else:
    get_config(config)
    print(LINE)
    print(LINE)
    handle_display(config)
"""
