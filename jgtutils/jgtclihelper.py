import json
def print_jsonl_message(msg,extra_dict:dict=None,scope=None):
    o={}
    o["message"]=msg
    if extra_dict:
        o.update(extra_dict)
    if scope:
        o["scope"]=scope
    print(json.dumps(o))
