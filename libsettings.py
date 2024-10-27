'''Main module'''
import json
import logging
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

class JsettingsError(Exception):
    pass

class Jsettings():
    def __init__(self,
                 settingsfname: str = 'settings.json',
                 schemafname: str = 'settings_schema.json',
                 log_to_console: bool = False):
        self.settingsfname = settingsfname
        self.schemafname = schemafname
        self.logtoconsole = log_to_console
        self.full = {}
        self.JsettingsError = JsettingsError

    def loggerchoose(self, loggingtext: str = '', loglevel: str = 'info'):
        '''Choose a way to logging errors'''
        if self.logtoconsole:
            print(f'{loglevel}: {loggingtext}')
        else:
            if loglevel in ['info', 'warning', 'error']:
                getattr(logging, loglevel)(loggingtext)
            else:
                raise self.JsettingsError(
                    f'Log level {loglevel} not in supported levels list (info, warning, error)'
                    )

    def _load_json_file(self, fname: str) -> dict:
        '''Load json from file'''
        outdict = {}
        if os.path.exists(fname):
            try:
                with open(fname, encoding='utf-8') as f:
                    try:
                        outdict = json.load(f)
                    except json.JSONDecodeError:
                        self.loggerchoose(f'File {fname} is not a json file', 'error')
            except OSError:
                self.loggerchoose(f'Can\'t open file {fname}', 'error')
        else:
            self.loggerchoose(f'No such file or directory: {fname}', 'error')
        return outdict

    def load_settings(self):
        '''Checking and loading settings'''
        self.full = {}
        settingsdict = self._load_json_file(self.settingsfname)
        schemadict = self._load_json_file(self.schemafname)
        if (len(settingsdict) > 0) and (len(schemadict) > 0):
            try:
                validate(instance=settingsdict, schema=schemadict)
            except ValidationError as e:
                self.loggerchoose(e)
            except SchemaError as e:
                self.loggerchoose(e)
            else:
                self.full = settingsdict
        else:
            self.loggerchoose('Schema or settings is empty', 'warning')
