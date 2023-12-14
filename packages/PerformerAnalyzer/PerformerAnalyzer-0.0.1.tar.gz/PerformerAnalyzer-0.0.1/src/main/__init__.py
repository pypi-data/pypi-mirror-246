from data_transformer.data_manager_factory import DataManagerFactory
from data_processor.performanceAnalizer import Performance_Analyzer
from data_processor.configuration import Config

LINE = "-----------------------------"

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
    Helps to get user oprion
    :return(string): User option
    """
    print("OPTIONS: ")
    print("1. Summary")
    print("2. Export Pdf")
    print(LINE)
    return input("Choose any one of the below options: ")

def validate(user_input):
    """
    Helps to validate user input.
    If the user input is not 1 0r 2 throws error
    :param user_input: user_input
    :return: None
    """
    if user_input not in ['1', '2']:
        raise ValueError("Please Enter valid options.")

def get_config(config):
    """
    Helps to get config from user input
    :param config: config
    :return: None
    """
    print("Your Config is empty. So please enter below values which creates a new new config file")
    config.data_type = input("Please enter data_type: ")
    config.entity_collection = input("Please enter entity_collection_name: ")
    config.base_field = input("Please enter base_field: ")
    config.path = input("Please enter path: ")
    config.computable_fields = input("Please enter computable_fields: ").split(',')
    config.write_config()

def handle_display(config):
    """
    Handles the main user display screen by co-ordinating the other method
    :param config: config
    :return: None
    """
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
    config.read_config()
    if config.is_valid_config():
        handle_display(config)
    else:
        get_config(config)
        print(LINE)
        print(LINE)
        handle_display(config)

#Test
config = Config()
print_title()
config.read_config()
if config.is_valid_config():
    handle_display(config)
else:
    get_config(config)
    print(LINE)
    print(LINE)
    handle_display(config)