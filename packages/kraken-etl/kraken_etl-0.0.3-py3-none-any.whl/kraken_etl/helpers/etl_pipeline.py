
import os
import requests
from urllib.request import urlretrieve
import shutil
import zipfile
import requests
import datetime



from kraken_etl.helpers import etl_extract, etl_transform, etl_load, etl_io





def pipeline_file_to_json(source_url, headers, delimiter, map,  destination_path):
    """
    """


    job_no = f'job_{str(datetime.datetime.now())}'
    base_path = f'temp_etl/data/{job_no}/'




    if 1==1:
        # Download file
        step1_destination_path = base_path + 'step1'
        filepath = etl_extract.download_file(source_url, step1_destination_path)

        
        # if zip, Unzip file
        if step1_destination_path.endswith('.zip'):
            source_path = filepath
            step2_destination_path = base_path + 'step2'
            etl_extract.unzip_file(source_path, step2_destination_path)
        else:
            step2_destination_path = step1_destination_path

        
        # Load from csv and convert to json
        source_path = step2_destination_path
        step3_destination_path = base_path + 'step3'
        etl_extract.csv_to_json(source_path, step3_destination_path, headers, delimiter)


        # Convert records
        source_path = step3_destination_path
        step4_destination_path = base_path + 'step4'
        etl_transform.transform(source_path, step4_destination_path, map)


        # Load records
        source_path = step4_destination_path
        step5_destination_path = destination_path
        etl_load.load(source_path, step5_destination_path)

        # Delete temp records
        etl_io.delete_temp(base_path)


def pipeline_file_to_db(source_url, headers, delimiter, map,  destination_path):
    """
    """


    job_no = f'job_{str(datetime.datetime.now())}'
    base_path = f'temp_etl/data/{job_no}/'


    if 1==1:
        # Download file
        step1_destination_path = base_path + 'step1'
        filepath = etl_extract.download_file(source_url, step1_destination_path)


        # if zip, Unzip file
        if source_url.endswith('.zip'):
            source_path = filepath
            step2_destination_path = base_path + 'step2'
            etl_extract.unzip_file(source_path, step2_destination_path)
        else:
            step2_destination_path = step1_destination_path


        # Load from csv and convert to json
        source_path = step2_destination_path
        step3_destination_path = base_path + 'step3'
        etl_extract.csv_to_json(source_path, step3_destination_path, headers, delimiter)


        # Convert records
        source_path = step3_destination_path
        step4_destination_path = base_path + 'step4'
        etl_transform.transform(source_path, step4_destination_path, map)


        # Load records
        source_path = step4_destination_path
        step5_destination_path = destination_path
        etl_load.load_to_db(source_path, step5_destination_path)


        # Delete temp records
        etl_io.delete_temp(base_path)