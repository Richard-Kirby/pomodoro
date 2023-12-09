import datetime


# Class to help testing.
class Test:
    def __init__(self, file, test_name, test_result, result_desc=None):
        self.test_time = datetime.datetime.now().isoformat()
        self.file = file
        self.test_name = test_name
        self.result_desc = result_desc
        if test_result == 'failed' or test_result == 'passed':
            self.test_result = test_result
        else:
            raise ValueError("Must be passed or failed")

    def return_result(self) -> str:
        return f"{self.test_time}, {self.file},  {self.test_name}, {self.test_result}, {self.result_desc}"
