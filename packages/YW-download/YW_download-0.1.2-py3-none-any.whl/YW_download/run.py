





import requests
import pandas as pd
import json, sys, os
import time
from importlib.metadata import version


from .functions import get_access_token, download


# credentials: [username, password]
# images: csv with two columns: image and download. Download is 1 when downloaded
# out_folder: where to download the zip files 

def run(credentials, images, out_folder):
    
    
    
    ### Print all metadata/settings and save them in a txt file
    
    
    # Start logging in txt file
    orig_stdout = sys.stdout
    
    
    log_file = 'download_log_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '.txt'

    log_file = '{}/{}'.format(out_folder, log_file)

    
    class Logger:
        def __init__(self, filename):
            self.console = sys.stdout
            self.file = open(filename, 'w')
            self.file.flush()
        def write(self, message):
            self.console.write(message)
            self.file.write(message)
        def flush(self):
            self.console.flush()
            self.file.flush()

    sys.stdout = Logger(log_file)
        
    
    # Metadata
    print('YW_download version: ' + str(version('YW_download')))
    print('System time: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    print('images: ' + str(images))
    print('out_folder: ' + str(out_folder))
    
    
    
    

    
    df_images = pd.read_csv(images)
    n_row = df_images.shape[0]
    
    # n_row = 10
    
    
    ### Loop through images 
    
    for i in range(n_row):
        

    
    
        scene_id = df_images.iloc[i]['image']
        print('\nscene_id: ' + str(scene_id))
        
        if df_images.iloc[i]['download'] == 1:
            print('Already downloaded, skipping this...')
            continue
        
        
        # Access token 
        access_token = get_access_token(credentials[0],credentials[1])
        print('\Token ready')
        
        
        # Json file 
        value_json = requests.get("https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=contains(Name,'{}')".format(scene_id)).json()
        df_json = pd.DataFrame.from_dict(value_json['value'])
        
        
        # Test if there's only one row 
        if df_json.shape[0] != 1: 
            sys.exit('JSON error')
        
        image_id = df_json['Id'].values[0]
        print('image_id: ' + str(image_id))
    
        
        # Download 
        out_file = ('{}/{}.zip'.format(out_folder,scene_id))
        
        download(image_id, access_token, out_file)
        print('Downloaded: ' + str(scene_id))
        
        
        
        
        ### If successful, write on the csv 
        df_images.at[i, 'download'] = int(1)
        df_images.to_csv(images, index=False)
        
        
    
        ### If not, retry this image by getting token again 
        
        ### If fail 3 times, quit and print error message 
        
        
    
    
    # Stop logging 
    sys.stdout = orig_stdout








