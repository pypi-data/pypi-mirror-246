from typing import Union
from VaniLite.utils import *

class VaniLite:
    """Class for the VaniLiteLite library."""
    def __init__(self, language: Union[str, None] = None, language_dir: str = "/strings/", strip_at_end: bool = True) -> None:
        """Initialize the VaniLite class."""
        self.language = language
        self.strip_at_end = strip_at_end
        self.language_dir = language_dir
        self.local_strings = {}
        self.initilize()

    def initilize(self):
        """Initialize the VaniLite class."""
        if self.language:
            self.load_file(self.language, self.language_dir)
        else:
            files = get_all_files_in_dir(self.language_dir)
            for file in files:
                lang_name = file.split(".")[0]
                self.local_strings.update({f"{lang_name}_{key}": value for key, value in load_file(lang_name, self.language_dir).items()})

    
    def reload_language(self, language_code: str, language_dir: str = "/strings/") -> dict:
        """Reload the language file."""
        self.__init__(language_code, language_dir)

    def load_file(self, language_code: str, language_dir: str = "/strings/") -> dict:
        """Load the file for the given language code."""
        self.local_strings = load_file(language_code, language_dir)
        return self.local_strings
    
    def _get_string(self, string_name: str, default_string: str = "No string found.", lang=None) -> str:
        """Get the string from the loaded file."""
        return self.local_strings.get(string_name, default_string)

    def retrieve_string(self, string_name: str, default_string: str = "No string found.", *args, **kwargs) -> str:
        """Get the string from the loaded file and parse it with the given arguments."""
        string = self._get_string(string_name, default_string)
        return string.strip().format(*args, **kwargs) if self.strip_at_end else string.format(*args, **kwargs)
