import logging
import os

import boto3
import botocore
from osmosis_driver_interface.data_plugin import AbstractPlugin
from osmosis_driver_interface.exceptions import OsmosisError


class Plugin(AbstractPlugin):
    """
    """
    def __init__(self, config=None):
        """Initialize a :class:`~.Plugin`.
        """
        self.logger = logging.getLogger('Plugin')
        logging.basicConfig(level=logging.INFO)
        self.s3 = boto3.client('s3')
        """ :type : pyboto3.s3 """
        self.s3meta = boto3.resource('s3')

        self.location = os.getenv('AWS_DEFAULT_REGION', 'EU')

    @property
    def type(self):
        """str: the type of this plugin (``'AWS'``)"""
        return 'AWS'

    @staticmethod
    def validate_s3_path(path):
        """Validate a path if it represents correctly a S3 path
        Args:
             path(str): The path to check.
        Raises:
            :exc:`~..OsmosisError`: if the file is not uploaded correctly."""
        return path.startswith('s3://')

    def parse_s3_path(self, path):
        """Validate a path if it represents correctly a S3 path
        Args:
             path(str): The path to check.
        Raises:
            :exc:`~..OsmosisError`: if the file is not uploaded correctly."""
        if self.validate_s3_path(path):
            bucket = path[5:].split('/', 1)[0]
            try:
                path = path[5:].split('/', 1)[1]
            except IndexError:
                path = ''
            return bucket, path
        else:
            self.logger.error(f"Path {path} must be a s3 url (format s3://my_bucket/my_file)")
            raise OsmosisError

    @staticmethod
    def validate_local_path(path):
        """Validate a path if it represents correctly a local path
        Args:
             path(str): The path to check.
        Raises:
            :exc:`~..OsmosisError`: if the file is not uploaded correctly."""
        return not path.startswith('s3://')

    def upload(self, local_file, remote_file):
        """Upload file to a remote resource manager
         Args:
             local_file(str): The path of the file to upload.
             remote_file(str): The path of the resource manager where the file is going to be allocated.
         Raises:
             :exc:`~..OsmosisError`: if the file is not uploaded correctly.

        """
        self.copy(local_file, remote_file)

    def download(self, remote_file, local_file):
        """Download file from a remote resource manager
        Args:
             remote_file(str): The path in the resource manager of the file to download from.
             local_file(str): The path to the file to download to..
        Raises:
             :exc:`~..OsmosisError`: if the file is not downloaded correctly.
        """
        self.copy(remote_file, local_file)

    def list(self, remote_folder):
        """List all the files of a cloud directory.
        Args:
             remote_folder(str): Name of the directory to list.
        Returns:
            dict: List with the name of the file of a directory.
        Raises:
             :exc:`~..OsmosisError`: if the directory does not exist.
        """
        bucket, path = self.parse_s3_path(remote_folder)
        try:
            paginator = self.s3.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=path)
            return page_iterator.build_full_result()['Contents']
        except Exception as e:
            raise OsmosisError

    def copy(self, source_path: str, dest_path: str):
        """Copy file from a path to another path.
         Args:
             source_path(str): The path of the file to be copied.
             dest_path(str): The destination path where the file is going to be allocated.
         Raises:
             :exc:`~..OsmosisError`: if the file is not uploaded correctly.
        """
        # XOR Check
        # if source_path.startswith('s3://') != dest_path.startswith('s3://'):
        #     self.logger.error("Either local or remote file must be a s3 url and the other must be a local reference")
        #     raise OsmosisError
        if not (source_path.startswith('s3://') or dest_path.startswith('s3://')):
            self.logger.error("Source or destination must be a s3 url (format s3://my_bucket/my_file)")
            raise OsmosisError
        if source_path.startswith('s3://') and dest_path.startswith('s3://'):
            self.logger.error("Source or destination must be a local directory")
            raise OsmosisError

        # Check if resources exists and can read
        if source_path.startswith('s3://'):
            bucket = source_path[5:].split('/', 1)[0]
            path = source_path[5:].split('/', 1)[1]
            try:
                # src_file = self.s3.Object(bucket, path).load()
                self.s3meta.meta.client.download_file(bucket, path, dest_path)
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    self.logger.error(f"Source file {path} in bucket {bucket} not found")
                    raise OsmosisError
                # else:
                #     if not os.path.isfile(source_path):
                #         self.logger.error(f"Source file {source_path} not found or cannot be read")
                #         raise OsmosisError

        elif dest_path.startswith('s3://'):
            bucket = dest_path[5:].split('/', 1)[0]
            path = dest_path[5:].split('/', 1)[1]
            try:
                # self.s3meta.meta.client.head_bucket(Bucket=bucket)
                self.s3meta.meta.client.upload_file(source_path, bucket, path)
            except botocore.exceptions.ClientError:
                # self.logger.error("The destination bucket {} does not exist or you have no access".format(bucket))
                self.logger.error(
                    f"There were a problem uploading local file {source_path}. Please check file exists and bucket "
                    f"{bucket} is accesible")

    def generate_url(self, remote_file):
        """Generate a signed url that give access for a period of time to the resource
        Args:
            remote_file(str): The path in the resource manager of the file to give access.
        Raises:
             :exc:`~..OsmosisError`: if the file does not exist or if the action could not be done.
        """
        pass

    def delete(self, remote_file):
        """Delete a file of a remote resource manager
        Args:
             remote_file(str): The path in the resource manager of the file to delete..
        Raises:
             :exc:`~..OsmosisError`: if the path does not exist or if the action could not be done.
        """

        bucket, path = self.parse_s3_path(remote_file)
        try:
            self.s3.delete_object(Bucket=bucket, Key=path)
        except Exception as e:
            raise OsmosisError

    def create_bucket(self, bucket):
        """Create a bucket in S3
        Args:
            bucket(str): The name of the bucket
        Raises:
             :exc:`~..OsmosisError`
        """
        try:
            self.s3meta.meta.client.head_bucket(Bucket=bucket)
        except botocore.exceptions.ClientError:
            try:
                self.s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={'LocationConstraint': self.location})
            except Exception:
                logging.error(f"Error creating bucket {bucket} in region {self.location}")
                raise OsmosisError

    def delete_bucket(self, bucket_name):
        """Delete a bucket in S3
        Args:
            bucket_name(str): The name of the bucket
        Raises:
             :exc:`~..OsmosisError`
        """
        try:
            self.s3meta.meta.client.head_bucket(Bucket=bucket_name)
            bucket = self.s3meta.Bucket(bucket_name)
            for key in bucket.objects.all():
                key.delete()
            bucket.delete()
        except Exception:
            logging.error(f"Error deleting bucket {bucket_name} in region {self.location}")
            raise OsmosisError

    def list_buckets(self):
        """List the S3 buckets
        Args:
            bucket_name(str): The name of the bucket
        Raises:
             :exc:`~..OsmosisError`
        """
        try:
            response = self.s3.list_buckets()
            return response['Buckets']
        except Exception:
            logging.error(f"Error listing buckets")
            raise OsmosisError

    def create_directory(self, remote_folder):
        """Create a directory in S3
        Args:
            remote_folder(str): The path of the remote directory
        Raises:
             :exc:`~..OsmosisError`: if the directory already exists.
        """
        bucket, path = self.parse_s3_path(remote_folder)
        if bucket == '' or path == '':
            self.logger.error("Remote folder can not be empty")
            raise OsmosisError
        path = path + '/' if not path.endswith('/') else path
        try:
            self.create_bucket(bucket)
            self.s3.put_object(Bucket=bucket, Body='', Key=path)
        except Exception:
            raise OsmosisError

    def retrieve_availability_proof(self):
        """TBD"""
        pass

