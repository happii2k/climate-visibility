import traceback

def error_message_detail(error):
    tb = traceback.extract_tb(error.__traceback__)
    file_name, line_no, func_name, text = tb[-1]  # last trace point
    error_message = f"Error occurred in script [{file_name}] at line [{line_no}]: {str(error)}"
    return error_message

class VisibilityException(Exception):
    def __init__(self, error):
        message = error_message_detail(error)
        super().__init__(message)
        self.error_message = message

    def __str__(self):
        return self.error_message
