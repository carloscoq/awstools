import os
import boto3
from botocore.exceptions import NoCredentialsError

def copy_to_s3(local_folder_path, s3_bucket_name):
    # Ensure the specified folder exists
    if not os.path.exists(local_folder_path):
        print(f"The specified folder '{local_folder_path}' does not exist.")
        return
    
    # Get the folder name from the local path
    folder_name = os.path.basename(local_folder_path)

    # Initialize the S3 client
    s3_client = boto3.client('s3')

    try:
        # Upload files to the S3 bucket
        for root, dirs, files in os.walk(local_folder_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                s3_object_key = os.path.relpath(local_file_path, local_folder_path)
                s3_object_key = os.path.join(folder_name, s3_object_key)
                s3_client.upload_file(local_file_path, s3_bucket_name, s3_object_key)
                print(f"Uploaded '{local_file_path}' to '{s3_object_key}' in S3 bucket '{s3_bucket_name}'.")

        print(f"Folder '{local_folder_path}' and its contents have been copied to '{s3_bucket_name}/{folder_name}'.")

    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your AWS credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Check if the script is being run from the command line
if __name__ == "__main__":
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python copy_to_s3.py <local_folder_path> <s3_bucket_name>")
    else:
        local_folder_path = sys.argv[1]
        s3_bucket_name = sys.argv[2]
        copy_to_s3(local_folder_path, s3_bucket_name)