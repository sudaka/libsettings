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
        self.remove_all()
        self.settings = Jsettings(settingsfname=self.settingsfname,
                                  schemafname=self.schemafname)
        logging.basicConfig(level=logging.INFO,
                            filename=self.errfname,
                            format="%(levelname)s %(message)s")

    def save_to_json(self, fname, data):
        '''Small function for saving dict to json'''
        with open(fname, "w", encoding='utf-8') as f:
            json.dump(data, f)

    def remove_all(self):
        '''Remove files if exist'''
        for fname in [self.settingsfname, self.schemafname]:
            if os.path.exists(fname):
                os.remove(fname)

    def test_000(self):
        '''Init clear log'''
        with open(self.errfname, 'w', encoding='utf-8') as f:
            f.write('')

    def test_001_error_logging(self):
        '''Test saving logging'''
        logging.info('Test %s started', '001')
        #writing log mesages to logfile
        self.settings.loggerchoose('info level')
        self.settings.loggerchoose('warning level', 'warning')
        self.assertRaises(self.settings.jsettingserror,
                          self.settings.loggerchoose,
                          'error level',
                          'error')
        with open(self.errfname, encoding='utf-8') as f:
            errlilst = f.readlines()
            self.assertEqual(errlilst[-3], 'INFO info level\n')
            self.assertEqual(errlilst[-2], 'WARNING warning level\n')
            self.assertEqual(errlilst[-1], 'ERROR error level\n')

    def test_002_exception_raising(self):
        '''Test exception raized when bad loglevel'''
        logging.info('Test %s started', '002')
        self.assertRaises(self.settings.jsettingserror,
                          self.settings.loggerchoose,
                          'Bad level', 
                          'bad level')

    def test_003_create_simple_conf(self):
        '''Create simple conf, schema and checking loaded conf'''
        logging.info('Test %s started', '003')
        settings = {'testint': 1}
        self.save_to_json(self.settingsfname, settings)
        logging.info('Settings: %s', settings)
        schema = {'type': 'object',
                  'properties': {
                      'testint': {'type': 'number'}
                    },
                  'required': ['testint']
                  }
        self.save_to_json(self.schemafname, schema)
        logging.info('Schema: %s', schema)
        self.settings.load_settings()

        for key, val in self.settings.full_settings_dict.items():
            self.assertEqual(val, settings[key])

    def test_004_miss_conf(self):
        '''Check error in log when settings file is missing'''
        logging.info('Test %s started', '004')
        schema = {'type': 'object',
                  'properties': {
                      'testint': {'type': 'number'}
                    },
                  'required': ['testint']
                  }
        self.save_to_json(self.schemafname, schema)
        self.assertRaises(self.settings.jsettingserror,
                          self.settings.load_settings)
        with open(self.errfname, encoding='utf-8') as f:
            errlilst = f.readlines()
            self.assertEqual(errlilst[-1],
                             f'ERROR No such file or directory: {self.settingsfname}\n')

    def test_005_bad_config(self):
        '''Config has bad datatype to scheme'''
        logging.info('Test %s started', '005')
        settings = {'testint': 1}
        self.save_to_json(self.settingsfname, settings)
        logging.info('Settings: %s', settings)
        schema = {'type': 'object',
                  'properties': {
                      'testint': {'type': 'string'}
                    },
                  'required': ['testint']
                  }
        self.save_to_json(self.schemafname, schema)
        logging.info('Schema: %s', schema)
        self.assertRaises(self.settings.jsettingserror,
                          self.settings.load_settings)

    def test_006_unsupported_attrnames(self):
        '''Importing unsupported name \'full_settings_dict\' '''
        logging.info('Test %s started', '006')
        settings = {'full_settings_dict': 1}
        self.save_to_json(self.settingsfname, settings)
        logging.info('Settings: %s', settings)
        schema = {'type': 'object',
                  'properties': {
                      'full_settings_dict': {'type': 'number'}
                    }
                  }
        self.save_to_json(self.schemafname, schema)
        logging.info('Schema: %s', schema)
        self.assertRaises(self.settings.jsettingserror,
                          self.settings.load_settings)

    def test_007_load_attributes(self):
        '''Importing settings to attributes'''
        logging.info('Test %s started', '007')
        settings = {'testint': 1,
                    'testlist': [2,3],
                    'testobj': {'testint': 4}
                    }
        self.save_to_json(self.settingsfname, settings)
        logging.info('Settings: %s', settings)
        schema = {'type': 'object',
                  'properties': {
                      'testint': {'type': 'number'},
                      'testlist': {'type': 'array',
                                   'items': {'type': 'number'}},
                      'testobj': {'type': 'object',
                                  'properties': {'testint': {'type': 'number'}
                                  }}
                    }
                  }
        self.save_to_json(self.schemafname, schema)
        logging.info('Schema: %s', schema)
        self.settings.load_settings()
        self.assertEqual(self.settings.testint, settings['testint'])
        for i, element in enumerate(settings['testlist']):
            self.assertEqual(self.settings.testlist[i], element)
        for key, val in settings['testobj'].items():
            self.assertEqual(val, self.settings.testobj[key])

    def test_last(self):
        '''Final events before exit'''
        logging.info('Tests finished')

if __name__ == '__main__':
    unittest.main()
