import json
import pandas as pd
from google.cloud import compute_v1
from google.oauth2 import service_account
from google.cloud import storage

# Replace these values with your service account key JSON file path
# Replace with your VM instance name
service_account_key_path = "gcp-sa.json"
project_id = "extreme-quasar-399203"
zone = "us-central1-c"  # Replace with your desired zone
vm_instance_name = "test-vm"
gcs_bucket_name = "gcs-ds-bkt"  # Name of your GCS bucket
source_dir = "source"  # Directory for JSON file in GCS
dest_dir = "dest"  # Directory for Excel file in GCS

def list_vm_disks(project_id, zone, vm_instance_name, service_account_key_path):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_key_path, scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    compute_client = compute_v1.InstancesClient(credentials=credentials)
    instance_name = f'projects/{project_id}/zones/{zone}/instances/{vm_instance_name}'
    request = compute_client.get(project=project_id, zone=zone, instance=vm_instance_name)

    data = {
        "VM Name": vm_instance_name,
        "Disks": []
    }

    if request.disks:
        for disk in request.disks:
            disk_info = {
                "Disk Name": disk.device_name,
                "Disk Type": disk.type,
                "Source": disk.source,
                "Disk Size (GB)": disk.disk_size_gb,
                "mode": disk.mode
                
                
                
            }
            data["Disks"].append(disk_info)

    # Save the data to a JSON file
    with open('sample.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Save the data to an Excel file
    df = pd.DataFrame(data["Disks"])
    df.to_excel('sample.xlsx', index=False, engine='openpyxl')

    # Upload the JSON file to GCS
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(gcs_bucket_name)

    # Specify blob names with the desired directories
    json_blob = bucket.blob(f'{source_dir}/sample.json')
    json_blob.upload_from_filename('sample.json')

    excel_blob = bucket.blob(f'{dest_dir}/sample.xlsx')
    excel_blob.upload_from_filename('sample.xlsx')

if __name__ == '__main__':
    list_vm_disks(project_id, zone, vm_instance_name, service_account_key_path)
