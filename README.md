## Description
Python library for checking json settings file and loading first level settings to attributes of object. 
For validation used jsonschema https://python-jsonschema.readthedocs.io/en/stable/

## Restrictions:
First level of settings keys can't be:
- settingsfname
- schemafname
- logtoconsole
- full_settings_dict
- jsettingserror 

## Requirements:
- jsonschema

## Usage:
### create settings file mysettings.json
```
{'testint': 1}
```
### create schema file myschema.json
```
{'type': 'object',
 'properties': {'testint': {'type': 'number'} }
}
```
### exec code
```
import logging
from libsettings import Jsettings

logging.basicConfig(level=logging.ERROR,
                    filename='error.log',
                    format="%(levelname)s %(message)s")
mysettings = Jsettings(settingsfname='mysettings.json',
                          schemafname='myschema.json')
mysettings.load_settings()
print(mysettings.testint)
```
After this, first level of jsonsettingsfname will be imported in attributes
of mysettings. It will be print a number '1'.

If you don't use logging, code can be like that:
```
from libsettings import Jsettings

mysettings = Jsettings(settingsfname='mysettings.json',
                          schemafname='myschema.json', 
                          log_to_console=True)
mysettings.load_settings()
```
