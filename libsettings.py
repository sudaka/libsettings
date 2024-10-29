'''Main module'''
import json
import logging
import os
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

class JsettingsError(Exception):
    '''Jsettings error class'''
    pass

class Jsettings():
    '''Main jsettings class'''
    def __init__(self,
                 settingsfname: str = 'settings.json',
                 schemafname: str = 'settings_schema.json',
                 log_to_console: bool = False):
        self.settingsfname = settingsfname
        self.schemafname = schemafname
        self.logtoconsole = log_to_console
        self.full_settings_dict = {}
        self.jsettingserror = JsettingsError

    def loggerchoose(self, loggingtext: str = '', loglevel: str = 'info'):
        '''Choose a way to logging errors'''
        if loglevel not in ['info', 'warning', 'error']:
            raise self.jsettingserror(
                f'Log level {loglevel} not in supported levels list (info, warning, error)'
                )
        if not self.logtoconsole:
            if loglevel in ['info', 'warning', 'error']:
                getattr(logging, loglevel)(loggingtext)
            else:
                raise self.jsettingserror(
                    f'Log level {loglevel} not in supported levels list (info, warning, error)'
                    )
        if loglevel in ['error']:
            raise self.jsettingserror(loggingtext)

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

    def _check_attr_names(self):
        '''Checking first level settings names to added it in attributes'''
        settings_attrs = set(self.__dict__.keys())
        new_attrs = set(self.full_settings_dict.keys())
        bad_attrs = new_attrs.intersection(settings_attrs)
        if len(bad_attrs) > 0:
            self.loggerchoose(f'Attributes {bad_attrs} can\'t be imported.', 'error')
        for key, val in self.full_settings_dict.items():
            setattr(self, key, val)


    def load_settings(self):
        '''Checking and loading settings'''
        self.full_settings_dict = {}
        settingsdict = self._load_json_file(self.settingsfname)
        schemadict = self._load_json_file(self.schemafname)
        try:
            validate(instance=settingsdict, schema=schemadict)
            self.full_settings_dict = settingsdict
            self._check_attr_names()
        except ValidationError as e:
            self.loggerchoose(e, 'error')
        except SchemaError as e:
            self.loggerchoose(e, 'error')
