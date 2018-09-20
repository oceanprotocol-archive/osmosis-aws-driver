from osmosis_driver_interface.osmosis import Osmosis
from osmosis_aws_driver.data_plugin import S3_Plugin
from filecmp import cmp
import os, sys
import time
from osmosis_aws_driver.config_parser import load_config_section
import logging

################################### SETUP LOGGING! ###################################
loggers_dict = logging.Logger.manager.loggerDict

logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.DEBUG)

# Create formatter
FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
#FORMAT = "%(asctime)s L%(levelno)s: %(message)s"

DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logger.debug("Started logging in test module".format())
################################### SETUP LOGGING! ###################################

# Why was this needed???

# os.environ['AWS_PROFILE'] = 'ocean'
#aws = Osmosis('./tests/aws.ini').data_plugin()
# def test_plugin_type():
#     assert aws.type == 'AWS'


def test_complete():
    # Create folder, upload file, list files, download file, delete file
    # TODO: Add finally to clean s3 bucket

    # Get the configuration from file, OR from environment
    path_config = ''
    #path_config = 'aws.ini'

    if os.path.exists(path_config):
        config = load_config_section(file_path=path_config, section='S3')
    else:
        config = dict()
        #config['module'] = os.environ['AWS_S3_MODULE']
        #config['module.path'] = os.environ['AWS_S3_PATH']
        config['region'] = os.environ['AWS_S3_REGION']

    s3_plugin = S3_Plugin(config)

    # Create bucket
    bucket_name=f'ocean-test-osmosis-data-plugin-{int(time.time())}'
    print(f'Test bucket: {bucket_name}')
    s3_plugin.create_directory(f's3://{bucket_name}/test')

    # List buckets
    s3_plugin.list_buckets()

    # Upload a file
    s3_plugin.upload('./LICENSE', f's3://{bucket_name}/test/LICENSE')
    files = s3_plugin.list(f's3://{bucket_name}/test/')
    print(f'Files in bucket {bucket_name}')
    for f in files:
        print('\t',f)
    assert len(files) == 2  # /test and /test/LICENSE
    assert files[0]['Key'] == 'test/'
    assert files[1]['Key'] == 'test/LICENSE'

    # Download a file
    s3_plugin.download(f's3://{bucket_name}/test/LICENSE', '/tmp/test_osmosis_data_plugin_license')
    assert cmp('./LICENSE', '/tmp/test_osmosis_data_plugin_license')

    # Delete the file
    s3_plugin.delete(f's3://{bucket_name}/test/LICENSE')
    files = s3_plugin.list(f's3://{bucket_name}/test/')
    assert len(files) == 1
    assert files[0]['Key'] == 'test/'

    # Delete the bucket
    s3_plugin.delete_bucket(bucket_name)

#test_complete()