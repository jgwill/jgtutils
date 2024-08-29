import json
def print_jsonl_message(msg,extra_dict:dict=None,scope=None,state:str=None,msg_key_name = "message",state_key_name = "state",scope_key = "scope",use_short=False):
    o={}
    if use_short:
        msg_key_name="msg"
        state_key_name="s"
        scope_key="sc"
    o[msg_key_name]=msg
    if extra_dict:
        o.update(extra_dict)
    if scope:
        
        o[scope_key]=scope
    if state:
        
        o[state_key_name]=state
    print(json.dumps(o))
