'''Test unit for jsettings module'''
import json
import logging
import os
import unittest

from libsettings import Jsettings

class TestJsettings(unittest.TestCase):
    '''Jsettings module tests'''
    def setUp(self):
        self.errfname = 'error_test.log'
        self.settingsfname = 'settings_test.json'
        self.schemafname = 'settings_schema_test.json'
        self.settings = Jsettings(settingsfname=self.settingsfname,
                                  schemafname=self.schemafname)
        logging.basicConfig(level=logging.INFO,
                            filename=self.errfname,
                            format="%(levelname)s %(message)s")
        
    def test_error_logging(self):
        '''Test saving logging'''
        #writing log mesages to logfile
        self.remove_all()
        self.settings.loggerchoose('info level')
        self.settings.loggerchoose('warning level', 'warning')
        self.settings.loggerchoose('error level', 'error')
        with open(self.errfname, encoding='utf-8') as f:
            errlilst = f.readlines()
            self.assertEqual(errlilst[0], 'INFO info level\n')
            self.assertEqual(errlilst[1], 'WARNING warning level\n')
            self.assertEqual(errlilst[2], 'ERROR error level\n')

    def test_exception_raising(self):
        '''Test exception raized when bad loglevel'''
        self.assertRaises(self.settings.JsettingsError, self.settings.loggerchoose, 'Bad level', 'bad level')

    def save_to_json(self, fname, data):
        '''Small function for saving dict to json'''
        with open(fname, "w", encoding='utf-8') as f:
            json.dump(data, f)

    def remove_all(self):
        '''Remove files if exist'''
        for fname in [self.settingsfname, self.schemafname]:
            if os.path.exists(fname):
                os.remove(fname)
        if os.path.exists(self.errfname):
            with open(fname, "w", encoding='utf-8') as f:
                f.write('')

    def test_create_simple_conf(self):
        '''Create simple conf, schema and checking loaded conf'''
        settings = {'testint': 1}
        self.save_to_json(self.settingsfname, settings)
        schema = {'type': 'object',
                  'properties': {
                      'testint': {'type': 'number'}
                    },
                  'required': ['testint']
                  }
        self.save_to_json(self.schemafname, schema)
        self.settings.load_settings()
        for key, val in self.settings.full.items():
            self.assertEqual(val, settings[key])

    def test_miss_conf(self):
        '''Check error in log when settings file is missing'''
        self.settings.loggerchoose('info level')
        #self.settings.load_settings()
        '''
        with open(self.errfname, encoding='utf-8') as f:
            errlilst = f.readlines()
            self.assertEqual(errlilst[0], 'INFO info level\n')
        '''

    def tearDown(self):
        self.remove_all()
        if os.path.exists(self.errfname):
            os.remove(self.errfname)


if __name__ == '__main__':
    unittest.main()
