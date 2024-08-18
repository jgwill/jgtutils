import os
import sys
import json
import yaml

import dotenv


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jgtcliconstants import JGTSET_CLI_DESCRIPTION, JGTSET_CLI_EPILOG, JGTSET_CLI_PROG_NAME,_JGTSET_EXCLUDED_ENV_EXPORT_KEYS
from jgtenv import get_dotenv_jgtset_export_path, is_dotjgt_env_sh_exist, load_dotjgt_env_sh
from jgterrorcodes import JGTFILES_EXIT_ERROR_CODE, JGTSETTING_EXIT_ERROR_CODE

import jgtcommon

def parse_args():

    parser = jgtcommon.new_parser(JGTSET_CLI_DESCRIPTION, JGTSET_CLI_EPILOG,prog=JGTSET_CLI_PROG_NAME, enable_specified_settings=True)
    #parser=jgtcommon.add_settings_argument(parser)
    parser.add_argument('-E','-env','--export-env', action='store_true', help='Export settings as environment variables')
    #env keys to export
    parser.add_argument('-K','-keys','--keys', nargs='+', help='Export only the specified keys as environment variables')
    
    parser.add_argument('-J','-json','--json', action='store_true', help='Print as JSON')
    
    parser.add_argument('-Y','--yml','--yaml', action='store_true', help='Print as YAML')
    
    parser.add_argument('-S','--silent', action='store_true', help='silent output')
    
    #view list
    parser.add_argument('-V','--view', action='store_true', help='View settings list')
    
    #add -O --output to specify the env file to export to instead of the default
    parser.add_argument('-O','--output', help='Specify the output env file to export to')
    
    args = jgtcommon.parse_args(parser)
    return args


def _init_dotenv_jgt_export_file(env_file=None):
    
    try:
        jgt_batch_path = get_dotenv_jgtset_export_path() if not env_file else env_file
        with open(jgt_batch_path,"w") as f:
            #f.write("#!/bin/bash\n")
            f.write("# This file is generated by JGTSettingsCLI (jgtset)\n")
            f.write("# It should not be edited manually\n" if not env_file else f"# It normally should not be edited manually but it is a custom file, therefore you might if you know what you are doing\n")
            #f.write("# This file is used to fix the list export issue in the environment variables\n")
            #f.write("# Load this file first and then load the .env or other environment variable files to ovveride.  This fixes the list export issue\n")
            
    except:
        exit(JGTFILES_EXIT_ERROR_CODE)



def _add_value_to_jgt_export_file(key,value,quiet=True,env_file=None):
    try:
        enquote = False
        var_type = type(value).__name__
        #print("key is of type:",var_type)
        fixed_value = value 
        if var_type == "bool":
            fixed_value = str(value).lower()
        else:
            if var_type == "list":
                fixed_value = __format_list_to_string(value)
                enquote = True
                
        jgt_batch_path = get_dotenv_jgtset_export_path() if not env_file else env_file
        with open(jgt_batch_path,"a") as f:
            if enquote:
                append_line = f"{key}=\"{fixed_value}\"\n"
            else:
                append_line = f"{key}={fixed_value}\n"
            if not quiet:print(f"export {key}={fixed_value}")
            f.write(append_line.replace('""','"'))
    except:
        exit(JGTFILES_EXIT_ERROR_CODE)        

def _process_keys_to_env(_settings,keys=None,quiet=True,env_file=None):
    _init_dotenv_jgt_export_file(env_file=env_file)
    _what_to_export = _get_filtered_exportable_keys(_settings, keys)
    for key, value in _what_to_export.items():
        if key not in _JGTSET_EXCLUDED_ENV_EXPORT_KEYS:
            if keys is None:
                _export_key(key, value,quiet,env_file=env_file)
            else:
                if key in keys:
                    _export_key(key, value,quiet,env_file=env_file)
    #run the batch file to fix the list export issue
    #os.system(f"source {_get_jgt_batch_filepath()}")
    #load using dotenv
    # for key in os.environ : 
    #     if key in settings:
    #         print(f"export {key}={os.getenv(key)}")
    # print("-------------------")
    #dotenv.load_dotenv(dotenv_path=get_jgt_env_export_path())
    # test_passed=True
    # for key in settings.keys():
    #     if not key in os.environ:
    #         test_passed=False
   
    # for key in os.environ : 
    #     if key in settings:
    #         value = os.getenv(key)
    #         os.environ[key] =value
    #         print(f"export {key}={value}")
    #         os.system(f"export {key}={value}")
    #print("Test passed:" if test_passed else "Test failed:")
    #print(os.getenv("columns_to_remove"))

def _export_key(key, value,quiet=True,is_subkey=False,env_file=None):
    if isinstance(value, dict): 
        #export key of the value as a string coma separated
        subkey_str_val='"' if not is_subkey else ""
        c=0
        for subkey, subvalue in value.items():
            delimiter = "," if c < len(value)-1 else ""
            subkey_var_name = f"{key}_{subkey}"
            subkey_str_val+=subkey+delimiter
            if isinstance(subvalue, dict):                
                _export_key(subkey_var_name, subvalue,quiet,is_subkey=True,env_file=env_file)
            else:
                os.environ[subkey_var_name] = str(subvalue)
                _export_key(subkey_var_name, subvalue,quiet,is_subkey=True,env_file=env_file)
                #if not quiet:print(f"export {key}_{subkey}={subvalue}")
            c+=1
        #os.environ[key] = subkey_str_val
        subkey_str_val+='"' if not is_subkey else ""
        if  not is_subkey and subkey_str_val != "":
            #if not quiet:print(f"export {key}={subkey_str_val}")
            _add_value_to_jgt_export_file(key,subkey_str_val,quiet,env_file=env_file)
    else:
        if isinstance(value, list):
            #if list contains dict, dont export
            if len(value) > 0 and isinstance(value[0], dict):
                for i in range(len(value)):
                    for subkey, subvalue in value[i].items():
                        subkey_var_name = f"{key}_{i}_{subkey}"
                        os.environ[subkey_var_name] = str(subvalue)
                        _export_key(subkey_var_name, subvalue,quiet,is_subkey=True,env_file=env_file)
                        #if not quiet:print(f"export {key}_{i}_{subkey}={subvalue}")
                return
            list_fixed = __format_list_to_string(value)
            os.environ[key] = list_fixed
            _add_value_to_jgt_export_file(key,value,quiet,env_file=env_file)
            #if not quiet:print(f"export {key}={list_fixed}")
        else:
            os.environ[key] = str(value)
            _add_value_to_jgt_export_file(key,value,quiet,env_file=env_file)
            #if not quiet:print(f"export {key}={value}")

def __format_list_to_string(value,enquote=True,single_quote=False):
    list_fixed='"' if not single_quote else "'"
    if not enquote:
        list_fixed=""
    c=0
    for v in value:
        delimiter = ","
        if c == len(value)-1:
            delimiter = ""
        list_fixed+=str(v)+delimiter
        c+=1
    list_fixed+='"' if not single_quote and enquote  else "'" if single_quote and enquote else ""
    
    return list_fixed


def dump_as_json_output(_settings,keys=None):
    _what_to_export = _get_filtered_exportable_keys(_settings, keys)
    return json.dumps(_what_to_export, indent=2)

def dump_as_yaml_output(_settings,keys=None):
    _what_to_export = _get_filtered_exportable_keys(_settings, keys)
    return yaml.dump(_what_to_export, default_flow_style=False)

def _get_filtered_exportable_keys(_settings, keys=None):
    _what_to_export = {}
    try:#jgtset_included
        if 'jgtset_included' in _settings and keys is None:
            keys=_settings['jgtset_included'].split(",")
    except:
        pass    
    try:#jgtset_included
        if 'JGTSET_INCLUDED' in os.environ and keys is None:
            keys=os.environ['JGTSET_INCLUDED'].split(",")
    except:
        pass
    if keys is not None:
        for key in keys:
            if key in _settings:
                _what_to_export[key] = _settings[key]
        for key in keys:
            if key not in _what_to_export and key in os.environ:
                _what_to_export[key] = os.environ[key]
        for key in keys:
            if key not in _what_to_export and is_dotjgt_env_sh_exist():
                load_dotjgt_env_sh()
                if key in os.environ:
                    _what_to_export[key] = os.environ[key]
    else:
        _what_to_export =_settings
    #remove keys that should not be exported using _JGTSET_EXCLUDED_ENV_EXPORT_KEYS
    for key in _JGTSET_EXCLUDED_ENV_EXPORT_KEYS:
        if key in _what_to_export:
            _what_to_export.pop(key)
    
    try:
        if os.environ['JGTSET_EXCLUDED']:
            for key in os.environ['JGTSET_EXCLUDED_ENV_EXPORT_KEYS'].split(","):
                if key in _what_to_export:
                    _what_to_export.pop(key)
    except:
        pass
    
    try:
        if 'jgtset_excluded' in _settings:
            for key in _settings['jgtset_excluded'].split(","):
                if key in _what_to_export:
                    _what_to_export.pop(key)
            _what_to_export.pop('jgtset_excluded')
    except:
        pass      
    return _what_to_export




def main():
    args = parse_args()
    env_flag = args.export_env
    json_flag = args.json
    yaml_flag = args.yml
    silent_flag = args.silent
    keys = args.keys
    output_file = args.output
    view_flag = args.view
    
    try:
        
        print_output=   process_env(env_flag,keys=keys,json_flag=json_flag,yaml_flag=yaml_flag,silent_flag=silent_flag,output_file=output_file,view_flag=view_flag)
        
        print(print_output)
        
    except:
        print("Error loading settings")
        sys.exit(JGTSETTING_EXIT_ERROR_CODE)

def process_env(env_flag,keys=None,json_flag=False,yaml_flag=False,silent_flag=False,output_file=None,view_flag=False,custom_path=None):
    
    settings = jgtcommon.get_settings(custom_path=custom_path)
    
    if view_flag:
        for key in settings.keys():
            print(key)
        return ""
    
    if env_flag and not json_flag and not yaml_flag:
        _process_keys_to_env(settings,keys=keys,quiet=False if not silent_flag else True,env_file=output_file)
        return ""
    print_output=""
    if yaml_flag:
        print_output = dump_as_yaml_output(settings,keys )
    else:
        print_output = dump_as_json_output(settings,keys )
    
    if env_flag: #Quiet export with other outputs
        _process_keys_to_env(settings,keys=keys,quiet=True,env_file=output_file)

    return print_output

if __name__ == '__main__':
    main()