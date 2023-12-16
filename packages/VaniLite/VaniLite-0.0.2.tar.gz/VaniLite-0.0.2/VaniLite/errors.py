# Copyright (C) 2023-present by TelegramExtended@Github, < https://github.com/TelegramExtended >.
#
# This file is part of < https://github.com/TelegramExtended/TelegramExtended > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TelegramExtended/TelegramExtended/blob/main/LICENSE >
#
# All rights reserved.

# Error to raise when translation file not found
class TranslationFileNotFoundError(Exception):
    """Error to raise when translation file not found."""
    def __init__(self, language_code: str, language_dir: str="/strings/", raw_error=None) -> None:
        """Initialize the TranslationFileNotFoundError class."""
        self.language_code = language_code
        self.language_dir = language_dir
        self.message = f"Translation file for language code {self.language_code} not found in directory {self.language_dir}. \nRaw error: {raw_error}"
        super().__init__(self.message)

