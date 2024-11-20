from constant import AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME, BUCKET_NAME
import boto3
from io import BytesIO
import cv2
import numpy as np
import json

class S3Utils:
    def __init__(self, aws_access_key, aws_secret_key, region_name, bucket_name):
        self.s3 = boto3.client(
            service_name='s3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        self.bucket_name = bucket_name

    def list_files(self, prefix=''):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            if 'Contents' in response:
                return [obj['Key'] for obj in response['Contents']]
            else:
                print("No files found in the bucket.")
                return []
        except:
            print("Issue in fetching the files.")
            return []

    def fetch_file_content(self, s3_key):
        try:
            file_obj = self.s3.get_object(Bucket=self.bucket_name, Key=s3_key)
            file_stream = BytesIO(file_obj['Body'].read())
            return file_stream
        except:
            print("Issue in fetching the file.")
            return None

    def stream_to_img(self, file_stream):
        if file_stream is not None:
            try:
                file_bytes = np.frombuffer(file_stream.read(), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                if img is not None:
                    return img
                else:
                    raise ValueError("Decoded image is None.")
            except:
                print("Error in decoding image.")
                return None
        print("File stream is None.")
        return None

    def stream_to_json(self, file_stream):
        if file_stream is not None:
            try:
                json_data = json.load(file_stream)
                return json_data
            except:
                print("Error in decoding JSON.")
                return None
        print("File stream is None.")
        return None
    
    def fetch_image(self, image_key):
        try:
            image_stream = self.fetch_file_content(image_key)
            image = self.stream_to_img(image_stream)
            return image
        except:
            return None

if __name__ == "__main__":
    s3_utils = S3Utils(AWS_ACCESS_KEY, AWS_SECRET_KEY, REGION_NAME, BUCKET_NAME)

    uttanasana_file_key = 'data/sun_salutation_poses/ideals/Uttanasana.jpg'
    img = s3_utils.fetch_image(uttanasana_file_key)
    if img is not None:
        cv2.imshow('Uttanasana Ideal Pose Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Failed to display the image.")

    json_file_key = 'data/poses_data.json'
    json_stream = s3_utils.fetch_file_content(json_file_key)
    json_data = s3_utils.stream_to_json(json_stream)
    if json_data is not None:
        print("Fetched JSON Data:")
        print(json.dumps(json_data, ensure_ascii=False, indent=4))
    else:
        print("Failed to fetch or parse the JSON file.")