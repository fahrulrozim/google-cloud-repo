import os
from google.cloud import storage
import requests

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'psychic-force-362917-f897bf215a19.json'
storage_client = storage.Client()

# Create a new bucket
def create_new_bucket(bucket_name):
    bucket = storage_client.bucket(bucket_name)
    bucket.location = 'US'
    bucket = storage_client.create_bucket(bucket)
    return bucket

bucket_name = 'test-fellowship7'
bucket = create_new_bucket(bucket_name)

# print bucket details
#vars(bucket)

# accessing specific bucket details
#my_bucket = storage_client.get_bucket(bucket_name) # Change your bucket name if you have different bucket name
#vars(my_bucket)

# Get multiple files from internet url to upload later
def get_files_from_url(url):
    data = requests.get(url)
    content_type = data.headers['Content-Type']

    # Note: This code is only for jpg, png, csv and txt files
    if 'image' in content_type:
        if 'png' in content_type:
            open('file/data_url.png', 'wb').write(data.content)
        elif 'jpg' in content_type:
            open('file/data_url.jpg', 'wb').write(data.content)
    elif 'text' in content_type:
        if 'csv' in content_type:
            open('file/data_url.csv', 'wb').write(data.content)
        elif 'plain' in content_type:
            open('file/data_url.txt', 'wb').write(data.content)
    else:
        print(f"TYPE: {content_type} TYPE NOT SUPPORTED")

urls = [
    'https://awsimages.detik.net.id/community/media/visual/2019/11/18/b90ff92b-1980-4558-b068-26605f535480_43.png?w=700&q=90',
    'https://filesamples.com/samples/document/txt/sample3.txt',
    'https://stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2021-financial-year-provisional/Download-data/annual-enterprise-survey-2021-financial-year-provisional-csv.csv'
]
for i in urls:
    get_files_from_url(i)

# Upload files from url to bucket
def upload_to_bucket(blob_name, file_path, bucket_name):
    """Upload files from local/url to bucket"""
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return

directory = os.path.join(os.getcwd(), 'file')

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if 'data_url.jpg' in f:
        upload_to_bucket('uploaded_image_jpg', f, bucket_name)
        print(f'Success upload {filename}')
    elif 'data_url.png' in f:
        upload_to_bucket('uploaded_image_png', f, bucket_name)
        print(f'Success upload {filename}')
    elif 'data_url.csv' in f:
        upload_to_bucket('upload_csv_file', f, bucket_name)
        print(f'Success upload {filename}')
    elif 'data_url.txt' in f:
        upload_to_bucket('upload_txt_file', f, bucket_name)
        print(f'Success upload {filename}')
    else:
        print(f'{filename} is not uploaded')

# Get list of objects in bucket
def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        print(blob.name)
    return blobs

blob_list = list_blobs(bucket_name)

# Download files from bucket to local
def download_file_from_bucket(blob_name, file_path, bucket_name):
    """Downloads a public blob from the bucket"""
    # bucket_name = "your-bucket-name"
    # blob_name = "storage-object-name"
    # file_path = "local/path/to/file"

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(file_path)

    print(
        "Downloaded public blob {} from bucekt {} to {}.".format(
            blob_name, bucket.name, file_path
        )
    )

download_file_from_bucket('upload_csv_file', os.path.join(os.getcwd(), 'download/data_csv.csv'), bucket_name)
download_file_from_bucket('upload_txt_file', os.path.join(os.getcwd(), 'download/txt_file.csv'), bucket_name)