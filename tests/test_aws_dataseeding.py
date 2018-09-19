from osmosis_driver_interface.osmosis import Osmosis
from osmosis_aws_driver.data_plugin import Plugin
from filecmp import cmp
import os
import logging
import time
import sys

logger = logging.getLogger(__name__)


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

# os.environ['AWS_PROFILE'] = 'ocean'
aws = Osmosis('./tests/aws.ini').data_plugin()
logging.debug("AWS Osmosis object created {}".format(aws))

def test_complete(caplog):
    caplog.set_level(logging.DEBUG)

    dpl = Plugin()
    bucket_name=f'ocean-test-osmosis-data-plugin-dataseeding-{int(time.time())}'
    dpl.create_directory(f's3://{bucket_name}/test')
    dpl.upload('./LICENSE', f's3://{bucket_name}/test/LICENSE')
    files = dpl.list(f's3://{bucket_name}/test/')
    assert len(files) == 2  # /test and /test/LICENSE
    assert files[0]['Key'] == 'test/'
    assert files[1]['Key'] == 'test/LICENSE'
    dpl.download(f's3://{bucket_name}/test/LICENSE', '/tmp/test_osmosis_data_plugin_license')
    assert cmp('./LICENSE', '/tmp/test_osmosis_data_plugin_license')
    dpl.delete(f's3://{bucket_name}/test/LICENSE')
    files = dpl.list(f's3://{bucket_name}/test/')
    assert len(files) == 1
    assert files[0]['Key'] == 'test/'
    dpl.delete_bucket(bucket_name)


#test_complete()