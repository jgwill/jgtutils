#%% Imports
import jgtutils.jgtos as jos
import os 
#%% Pov
i="EUR/USD";t="H4"
tlid_range = "231010_240105"


#%% Get data path v1

def get_data_path(nsdir):
  defpath= os.path.join(os.getcwd(),'data')
  data_path = os.environ.get('JGTPY_DATA', defpath)

  defpath= os.path.join(
    os.path.join(os.getcwd(),".."),
    'data')
  if not os.path.exists(data_path):
    data_path = os.environ.get('JGTPY_DATA', defpath)
    
  defpath= os.path.join(
    os.path.join(
      os.path.join(os.getcwd(),".."),
      ".."),
    'data')
  if not os.path.exists(data_path):
    data_path = os.environ.get('JGTPY_DATA', defpath)
    
  defpath= os.path.join(
    os.path.join(
      os.path.join(
        os.path.join(os.getcwd(),".."),
        ".."),
      ".."),
    'data')
  if not os.path.exists(data_path):
    data_path = os.environ.get('JGTPY_DATA', defpath)
    
  if os.name == "nt":
    data_path = data_path.replace("/", "\\")
    
  if not os.path.exists(data_path):
    raise Exception("Data directory not found. Please create a directory named 'data' in the current, parent directory (up to 3 levels), or set the JGTPY_DATA environment variable.")
  
  data_path = os.path.join(data_path, nsdir)
  return data_path

#%% Test the new and old datapath
print(f"{get_data_path('pds')} {jos.get_data_path('pds')} ")
  

#%% DateStart End of tlid_range
start_dt, end_dt = jos.tlid_range_to_start_end_datetime(tlid_range=tlid_range)

#%% Create path of the full range

p3=jos.mk_fn_range(i,t,start=start_dt,end=end_dt)
p3
#%% Test

path2=jos.create_filestore_path(i,t,quiet=False,compressed=False,tlid_range=None,output_path=None,nsdir="pds")
path2

fpath = jos.mk_fullpath(i, t, ext, data_path, tlid_range=tlid_range)
#%% Test
p3a=jos.mk_fn(i,t)
jos.get_data_path("pds")

jos.create_filestore_path(i,t,quiet=False,compressed=False,tlid_range=tlid_range,output_path="/data",nsdir="pds")

# %%
