# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import colemen_utils as c
import colemen_linux_utils.settings as _settings



class ColemenLinuxUtils:
    def __init__(self):
        self.settings = {}
        self.data = {}
        # self.set_defaults()

    # def set_defaults(self):
    #     self.settings = c.file.import_project_settings("colemen_linux_utils.settings.json")

    def master(self):
        print("master")


if __name__ == '__main__':
    m = ColemenLinuxUtils()
    m.master()

