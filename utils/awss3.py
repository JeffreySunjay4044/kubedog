import uuid
from pathlib import Path

import boto3

BUCKET_NAME = "ujjawal-test"
POSTERS_BASE_PATH = "assets/wallcontent"
CLOUDFRONT_BASE_URL = "https://xxx.cloudfront.net/"


class S3(object):
    def __init__(self):
        self.client = boto3.client('s3')
        self.bucket_name = BUCKET_NAME
        self.posters_base_path = POSTERS_BASE_PATH

    # def __download_image(self, url):
    #     manager = urllib3.PoolManager()
    #     try:
    #         res = manager.request('GET', url)
    #     except Exception:
    #         print("Could not download the image from URL: ", url)
    #         raise cex.ImageDownloadFailed
    #     return BytesIO(res.data)  # any file-like object that implements read()

    def upload_document(self, idName, depObj):
        # try:
        #     image_file = self.__download_image(url)
        # except cex.ImageDownloadFailed:
        #     raise cex.ImageUploadFailed

        extension = Path(idName).suffix
        id = uuid.uuid1().hex + extension
        final_path = self.posters_base_path + "/" + id
        try:
            self.client.upload_fileobj(depObj,
                                       self.bucket_name, final_path)
        except Exception as exception:
            print("Image Upload Error for URL: ", final_path)
            raise Exception(exception)

        return id