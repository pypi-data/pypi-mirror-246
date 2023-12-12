import json
import os
import sys
import traceback
from multiprocessing.pool import ThreadPool
import time
from urllib.parse import urlencode, quote
from typing import List, Union

from layernext.datalake.constants import MetadataUploadType, REMOVED_OBJECT_UPLOAD

from .keys import DEST_PROJECT_ID, OPERATION_MODE, OPERATION_TYPE, SESSION_ID, TOTAL_IMAGE_COUNT, UPLOADED_IMAGE_COUNT, USERNAME, LABELS, META_UPDATES_ARRAY, IS_NORMALIZED
import requests
import threading

class DatalakeInterface:

    def __init__(self, auth_token: str, dalalake_url: str):
        self.auth_token = auth_token
        self.dalalake_url = dalalake_url
        self.progress: int = 0
        self.count: int = 0
        self.count_lock = threading.Lock()
        self.total_batch_download: int = 0
        self.batch_download_failed_count: int = 0
        self.existing_file_count: int = 0

    def create_datalake_label_coco(self, label, username='Python SDK'):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        payload = {
            USERNAME: username,
            LABELS: label,
        }
        url = f'{self.dalalake_url}/api/client/cocojson/import/label/create'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            return response.json()
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
        

    def find_datalake_label_references(self, label_attribute_values_dict, username='Python SDK'):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        payload = {
            LABELS: label_attribute_values_dict,
            USERNAME: username
        }
        url = f'{self.dalalake_url}/api/client/system/label/references'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return_object = response.json()
                return return_object
            elif status_code == 204:
                return {"isSuccess": False, "message": "No references found"}
            else:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        

    def upload_metadata_updates(self, meta_updates, operation_type, operation_mode, operation_id, is_normalized, 
                                session_id, total_images_count, uploaded_images_count):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        payload = {
            META_UPDATES_ARRAY: json.dumps(meta_updates),
            SESSION_ID : session_id,
            TOTAL_IMAGE_COUNT : total_images_count,
            UPLOADED_IMAGE_COUNT : uploaded_images_count,
            OPERATION_MODE : operation_mode,
            OPERATION_TYPE : operation_type
        }

        params = {
            IS_NORMALIZED: is_normalized,
        }

        url = f'{self.dalalake_url}/api/metadata/operationdata/{operation_id}/update'
        print(url)

        try:
            response = requests.post(url=url, params=params, json=payload, headers=hed)
            return response.json()
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}

    ''''
    Upload meta data collection
    '''

    def upload_metadata_collection(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/uploadMetadataInCollection'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return_object = response.json()
                return_object["isSuccess"] = True
                return return_object
            elif status_code == 204:
                print("Upload meta data | No content is return for the requested resource")
                return {"isSuccess": False, "message": "No content is return for the requested resource"}
            else:
                return {"isSuccess": False, "message": response.json().get("error").get("message")}

        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}

    ''''
    Get file id and key from s3 bucket
    '''

    def get_file_id_and_key(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/fileUpload/initializeMultipartUpload'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code

            if status_code != 204 and status_code != 200:
                return_obj = {"isSuccess": False}
                return return_obj

            return_object = response.json()
            return_object["isSuccess"] = True
            return return_object
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}

    ''''
    Get pre-signed url
    '''

    def get_pre_signed_url(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/fileUpload/getMultipartPreSignedUrls'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code != 204 and status_code != 200:
                return {"isSuccess": False}

            return_object = response.json()
            return_object["isSuccess"] = True
            return return_object
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}


    ''''
    Finalize multipart upload
    '''

    def finalize_upload(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/fileUpload/finalizeMultipartUpload'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 204 or status_code == 200:
                return {"isSuccess": True}
            else:
                return {"isSuccess": False}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}


    def complete_collection_upload(self, upload_id, is_single_file_upload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/collectionUploadingStatus/{upload_id}/complete?isReturnedUniqueName={is_single_file_upload}'

        try:
            response = requests.get(url=url, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return_object = response.json()
                return_object["isSuccess"] = True
                return return_object
            elif status_code == 204:
                return {"isSuccess": True}
            else:
                return {"isSuccess": False}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}

    def get_upload_status(self, collection_name):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/collection/getuploadProgress?collectionName={collection_name}'

        try:
            response = requests.get(url=url, headers=hed)
            status_code = response.status_code
            if status_code == 204 or status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}

    def remove_modelrun_collection_annotation(self, collection_id, model_run_id, session_id):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/collection/deleteAnnotation?collectionId={collection_id}&operationId={model_run_id}'

        payload = {
            SESSION_ID : session_id
        }

        try:
            response = requests.get(url=url, headers=hed, json=payload)
            status_code = response.status_code
            if status_code == 204 or status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False, "message": response.json()}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}



    ''''
    get selection id from query, filter and collectionId
    '''
    def get_selection_id(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/query/getSelectionId'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}

    ''''
    trash selected objects
    ''' 
    def trash_files(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/file/trash'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            # print(response.json())
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
            
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}

    

    def get_object_type_by_id(self, object_id):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/{object_id}/getObjectTypeById'

        try:
            response = requests.get(url=url, json={}, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}

    def get_all_label_list(self, group_id):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/labels/list'
        if group_id != None:
            url += '?groupId=' + group_id
        try:
            response = requests.get(url=url, json={}, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return []
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return []
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return []
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return []
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return []
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return []

    def get_all_group_list(self):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/label_groups/list'

        try:
            response = requests.get(url=url, json={}, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return []
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return []
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return []
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return []
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return []
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return []

    def create_system_label(self, label):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/system/labels/create'
        payload = {
            "label": label,
            "userName": "Python SDK"
        }
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                print(response.text)
                return None
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return None
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return None
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return None
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return None
        
    def create_label_group(self, name, keys):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/label_groups/create'
        payload = {
            "groupName": name,
            "labelKeys": keys
        }
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                print(response.text)
                return {"isSuccess": False, "message": response.json()}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return None
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return None
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return None
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return None

    def add_labels_to_group(self, group_id, label_keys):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/label_groups/{group_id}/addLabels'
        payload = {
            "labelKeys": label_keys
        }
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                print(response.text)
                return {"is_success": False, "message": response.json()}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"is_success": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"is_success": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"is_success": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"is_success": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"is_success": False, "message": "An unexpected exception occurred"}

    def remove_labels_from_group(self, group_id, label_keys):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/label_groups/{group_id}/removeLabels'
        payload = {
            "labelKeys": label_keys
        }
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                print(response.text)
                return {"is_success": False, "message": response.json()}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"is_success": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"is_success": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"is_success": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"is_success": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"is_success": False, "message": "An unexpected exception occurred"}

    def check_job_status(self, job_id):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/jobs/{job_id}/getStatus'
        try:
            response = requests.get(url=url, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                print(response.text)
                return None
            
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return None
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return None
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return None
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return None
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return None

    def check_sdk_version_compatibility(self, sdk_version):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/sdk/compatibility/{sdk_version}'
        try:
            response = requests.get(url=url, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            elif status_code == 401:
                return {
                    "isCompatible": False,
                    "message": "Authentication failed, please check your credentials"
                }
            else:
                print(response.text)
                return {
                    "isCompatible": False,
                    "message": "Failed to connect to MataLake"
                }
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isCompatible": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isCompatible": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isCompatible": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isCompatible": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isCompatible": False, "message": "An unexpected exception occurred"}
        
    def get_file_download_url(self, file_key):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        encoded_key = quote(file_key)
        url = f'{self.dalalake_url}/api/client/downloadUrl?file_key={encoded_key}'

        try:
            response = requests.get(url=url, json={}, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False, "message": response.json()}
            
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        
    """
    Uploads metadata to MataLake
    """    
    def upload_metadata(self, payload, metadata_upload_type: MetadataUploadType):
        hed = {'Authorization': 'Basic ' + self.auth_token}

        if metadata_upload_type == MetadataUploadType.BY_JSON:
            url = f'{self.dalalake_url}/api/client/metadata/uploadMetadataByJson'
        elif metadata_upload_type == MetadataUploadType.BY_META_OBJECT:
            url = f'{self.dalalake_url}/api/client/metadata/uploadMetadataByMetaObject'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            # print(response)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            elif status_code == 406:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
            else:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
        except requests.exceptions.RequestException as e:
            print(f"An request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "Error in uploading metadata1"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)} ")
            traceback.print_exc()
            return {"isSuccess": False, "message": "Error in uploading metadata"}
        
    """
    Validates metadata tags to MataLake
    """
    def validate_tags(self, unique_tags):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/metadata/validateTags'
        payload = {
            "tags": unique_tags
        }
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return {"is_valid": True}
            elif status_code == 204:
                return {"is_valid": True}
            elif status_code == 406:
                return {"is_valid": False, "message":response.json().get("error").get("message")}
            else:
                print(response.text)
                return {"is_valid": False}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"is_valid": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"is_valid": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"is_valid": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"is_valid": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"is_valid": False, "message": "An unexpected exception occurred"}
        
    
    """
    Validates metadata fields to MataLake
    """
    def validate_meta_fields(self, unique_fields):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/metadata/validateMetaFields'
        payload = {
            "fields": unique_fields
        }
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return {"is_valid": True}
            elif status_code == 204:
                return {"is_valid": True}
            elif status_code == 406:
                return {"is_valid": False, "message":response.json().get("error").get("message")}
            else:
                print(response.text)
                return {"is_valid": False}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"is_valid": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"is_valid": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"is_valid": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"is_valid": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"is_valid": False, "message": "An unexpected exception occurred"}

        
    """
    Gets metadata from MataLake by using unique name  
    """
    def get_item_details(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/metadata/getItemDetails'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                print(response.json())
                return {"isSuccess": False, "message": response.json()}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
    

    """
    get item list from collection in datalake
    
    """
    def get_item_list_from_collection(self, payload, collection_id):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/explorer/{collection_id}/objects/list'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            elif status_code == 204:
                return {"isSuccess": False, "message":"No content found"}
            elif status_code == 406:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
            else:
                print(response.text)
                return {"isSuccess": False, "message":f"Error in getting item details: {response.text}"}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        
    """
    get item count from collection in metalake
    """
    def get_item_count_from_collection(self, payload, collection_id):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/explorer/{collection_id}/objects/count'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            elif status_code == 204:
                return {"isSuccess": False, "message":"No content found"}
            elif status_code == 406:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
            else:
                print(response.text)
                return {"isSuccess": False, "message":f"Error in getting item count: {response.text}"}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        
    """
    Gets metadata from MataLake by using collection id  
    """
    def get_collection_details(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/metadata/getCollectionDetails'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False, "message": response.json()}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        
    """  
    Use to get system data | image, video, other count
    """
    def get_system_details(self):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/getDetails/system'

        try:
            response = requests.get(url=url, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return_object = response.json()
                return_object["isSuccess"] = True
                return return_object
            elif status_code == 204:
                return {"isSuccess": True}
            else:
                return {"isSuccess": False}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        
    

    """
    use to this api to get collection id by name
    """    
    def get_collection_id_by_name(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/metadata/getCollectionIdByName'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            elif status_code == 204:
                return {"isSuccess": False, "message":"No content found"}
            elif status_code == 406:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
            else:
                print(response.text)
                return {"isSuccess": False, "message":f"Error in getting item details: {response.text}"}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        

    """
    get item list from datalake
    
    """    
    def get_item_list_from_datalake(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/explorer/objects/list'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            elif status_code == 204:
                return {"isSuccess": False, "message":"No content found"}
            elif status_code == 406:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
            else:
                print(response.text)
                return {"isSuccess": False, "message":f"Error in getting item details: {response.text}"}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        
    """
    get item count from metalake
    
    """    
    def get_item_count_from_metalake(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/explorer/objects/count'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            elif status_code == 204:
                return {"isSuccess": False, "message":"No content found"}
            elif status_code == 406:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
            else:
                print(response.text)
                return {"isSuccess": False, "message":f"Error in getting item count: {response.text}"}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        
    def create_collection_head(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/metadata/collection/create'

        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            elif status_code == 204:
                return {"isSuccess": False, "message":"No content found"}
            elif status_code == 406:
                return {"isSuccess": False, "message":response.json().get("error").get("message")}
            else:
                print(response.text)
                return {"isSuccess": False, "message":f"Error in getting item details: {response.text}"}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}

    """
    insert vector inside the vector database  
    """
    def insert_embeddings_batch(self, payload: dict) -> dict:
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/embeddings/insert/vectors'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "message": "insert request failed"
                }
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Failed to connect with MataLake")
            return {"success": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"success": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"success": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"success": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"success": False, "message": "An unexpected exception occurred"}
        
    def create_or_update_job(self, payload):
  
        hed = {'Authorization': 'Basic ' + self.auth_token}
        call_url = f'{self.dalalake_url}/api/job/updateJob/basicAuthRequest'

        try:
            response = requests.post(url=call_url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return {"isSuccess": False}
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Connection error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"isSuccess": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"isSuccess": False, "message": "An unexpected exception occurred"}
        

    '''
    Count increment
    '''

    def count_increment(self, attribute_name) -> None:
        self.count_lock.acquire()
        try:
            # Use getattr to access the attribute by name
            current_value = getattr(self, attribute_name)
            current_value += 1
            setattr(self, attribute_name, current_value)
        finally:
            self.count_lock.release()

    """
    Write progress to console
    """

    def write_progress(self, count: bool = True) -> None:
        if count:
            self.count_lock.acquire()
            try:
                self.count += 1
                self.progress = 100 * (self.count / self.total_batch_download)
                sys.stdout.write(
                    "\r" + "download files: " + str(
                        self.count) + f"/{self.total_batch_download}" + "     " + "progress: " +
                    str(round(self.progress, 2)) + " %")
                sys.stdout.flush()
            finally:
                self.count_lock.release()
        else:
            print(
                "\r" +
                f"Download files: {self.count} \n" +
                f"Total files: {self.total_batch_download} \n" +
                f"Batch download failed: {self.batch_download_failed_count} \n" +
                f"Existing files: {self.existing_file_count} \n" +
                f"Progress: {self.progress:.2f}% \n")

    '''
    Download a single file from MataLake
    '''

    def download_single_file(self, args: list) -> dict:
        file_data: dict = args[0]
        directory_path: str = args[1]

        if 'url' not in file_data:
            return {"is_success": False, "message": "File url not provided"}

        try:
            if 'uniqueName' in file_data:
                file_path_absolute = os.path.join(directory_path, file_data["uniqueName"])
                if os.path.exists(file_path_absolute):
                    self.count_increment("existing_file_count")
                    return {"is_success": True}

                r = requests.get(file_data["url"], timeout=25)
                with open(file_path_absolute, 'wb') as f:
                    f.write(r.content)

                return {"is_success": True}

            else:
                print("Filename not provided")
                return {"is_success": False, "message": "Filename not provided"}
        except Exception as e:
            print(f'Failed downloading')
            print(e)
            return {"is_success": False, "data": args}

    '''
    Download files from MataLake in parallel
    '''
    def parallel_download(self, data_lake_list: list, custom_download_path: str, folder_name: str) -> dict:

        if not isinstance(data_lake_list, list) or len(data_lake_list) == 0:
            print("No files to download")
            return {"is_success": False, "message": "No files to download"}

        self.total_batch_download = len(data_lake_list)
        directory_path: str = os.path.abspath(
            f'./{folder_name}/') if custom_download_path == '' else custom_download_path

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        argument_list: list = []
        for item in data_lake_list:
            argument_list.append((item, directory_path))

        file_download_failed: bool = False
        message: str = ""

        with ThreadPool(5) as p:
            for res in p.imap(self.download_single_file, argument_list):
                is_success = res["is_success"]

                if not is_success and "data" in res:
                    download_data = res["data"]
                    # try again to download the failed download
                    print(f"Retrying Download - {download_data[0]['fileName']}")
                    res = self.download_single_file(download_data)
                    is_success = res["is_success"]
                    download_data = res["data"]
                if not is_success:
                    file_download_failed = True
                    message = "file download failed"
                    self.count_increment("batch_download_failed_count")
                p.close()

                if is_success:
                    self.write_progress()

        self.write_progress(False)
        return {"is_success": not file_download_failed, "message": message}

    '''
    Download files from metalake
    '''

    def download_files_from_metalake(self, required_info: dict, item_type: str = None) -> dict:

        payload: dict = {
            "pageIndex": required_info['page_index'],
            "pageSize": required_info['page_size'],
            "query": required_info['query'],
            "filterData": required_info['data_filter'],
            "contentType": required_info['contentType'],
            "sortBy": required_info['sortBy']

        }

        custom_download_path: str = required_info['custom_download_path']
        folder_name: str = f"metalake_{item_type}s"
        data_lake_list = self.get_item_list_from_datalake(payload)

        if "isSuccess" in data_lake_list and not data_lake_list["isSuccess"]:
            message: str = ""
            if "message" in data_lake_list:
                message = data_lake_list["message"]
                print(message)
            return {"is_success": False, "message": message}

        if not isinstance(data_lake_list, list):
            print("Error in getting item list from MataLake")
            return {"is_success": False, "message": "data is not in array format"}

        return self.parallel_download(data_lake_list, custom_download_path, folder_name)

    '''
    Download files from metalake collections
    '''

    def download_files_from_collection(self, required_info: dict, collection_id: str) -> dict:

        payload: dict = {
            "pageIndex": required_info['page_index'],
            "pageSize": required_info['page_size'],
            "query": required_info['query'],
            "filterData": required_info['data_filter'],
            "contentType": required_info['contentType'],
            "sortBy": required_info['sortBy']
        }

        custom_download_path: str = required_info['custom_download_path']

        collection_list = self.get_item_list_from_collection(payload, collection_id)

        if "isSuccess" in collection_list and not collection_list["isSuccess"]:
            message: str = ""
            if "message" in collection_list:
                message = collection_list["message"]
                print(collection_list["message"])
            return {"is_success": False, "message": message}

        if not isinstance(collection_list, list):
            print("Error in getting item list from MataLake")
            return {"is_success": False, "message": "Error in getting item list from MataLake"}

        return self.parallel_download(collection_list, custom_download_path, collection_id)

    '''
    This method is used to download files from MataLake batch wise
    '''

    def download_files_batch_wise(self, item_type_enum, query: str, data_filter: dict, page_index: int,
                                  page_size: int,
                                  custom_download_path: str, config: dict, sort_filter: dict,
                                  item_type: str = None) -> dict:
        type_present = False
        collection_id_present = False

        if "item_type" in config and config["item_type"] != 0:
            type_present = True
        if "collection_id" in config:
            collection_id_present = True

        if not type_present and not collection_id_present:
            raise "Either item_type or id_list should be present in config"

        required_info: dict = {
            "page_index": page_index,
            "page_size": page_size,
            "custom_download_path": custom_download_path,
            "query": query,
            "data_filter": data_filter,
            "contentType": item_type_enum,
            "sortBy": sort_filter
        }

        if type_present:
            return self.download_files_from_metalake(required_info, item_type)

        if collection_id_present:
            return self.download_files_from_collection(required_info, config["collection_id"])
        

    """
    create embedding collection
    """
    def create_embedding_collection(self, payload):
        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/embeddings/create/embeddingModel'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return {"success": True}
            else:
                return {
                    "success": False,
                    "message": "create embedding collection failed"
                }
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Connection error from MataLake connection")
            return {"success": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"success": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"success": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"success": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"success": False, "message": "An unexpected exception occurred"}
    

    """
    Use for get the embedding vector
    @payload: dict
    """
    def get_embedding_vector(self, payload: dict) -> Union[List[dict], dict]:

        hed = {'Authorization': 'Basic ' + self.auth_token}
        url = f'{self.dalalake_url}/api/client/embeddings/getVector'
        try:
            response = requests.post(url=url, json=payload, headers=hed)
            status_code = response.status_code
            if status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "message": "get embedding vector failed"
                }
        #Handle connection error
        except requests.exceptions.ConnectionError as e:
            print("Connection error from MataLake connection")
            return {"success": False, "message": "Failed to connect to MataLake"}
        #Handle timeout error
        except requests.exceptions.Timeout as e:
            print("Timeout error from MataLake connection")
            return {"success": False, "message": "Failed to connect to MataLake"}
        #Handle HTTP errors
        except requests.exceptions.HTTPError as e:
            print("HTTP error from MataLake connection")
            return {"success": False, "message": "Failed to connect to MataLake"} 
        except requests.exceptions.RequestException as e:
            print(f"An unexpected request exception occurred: {format(e)}")
            traceback.print_exc()
            return {"success": False, "message": "An unexpected request exception occurred"}
        except Exception as e1:
            print(f"An unexpected exception occurred: {format(e1)}")
            traceback.print_exc()
            return {"success": False, "message": "An unexpected exception occurred"}