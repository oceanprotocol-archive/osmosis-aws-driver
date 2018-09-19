from osmosis_driver_interface.osmosis import Osmosis
from osmosis_aws_driver.data_plugin import Plugin
from filecmp import cmp
import os
import logging
import sys

################################### SETUP LOGGING! ###################################
loggers_dict = logging.Logger.manager.loggerDict

logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.DEBUG)

# Create formatter

# FORMAT = "%(asctime)s - %(levelno)s - %(module)-15s - %(funcName)-15s - %(message)s"
FORMAT = "%(asctime)s L%(levelno)s: %(message)s"

DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
#logger.critical("Logging started")

print("Loggers:")
for l in logging.Logger.manager.loggerDict:
    print("\t",l)
################################### SETUP LOGGING! ###################################

logger.debug("Started logging in test module".format())
#raise
# logging.getLogger('boto3').setLevel(logging.WARNING)
# logging.getLogger('botocore').setLevel(logging.WARNING)
# logging.getLogger('nose').setLevel(logging.WARNING)
# logging.getLogger('s3transfer').setLevel(logging.CRITICAL)




# os.environ['AWS_PROFILE'] = 'ocean'
aws = Osmosis('./tests/aws.ini').data_plugin()

# A live connection to S3 is establish
print("LEVEL DEBUG", logging.getLogger().isEnabledFor(logging.DEBUG))

logging.warning("Started warning logging in test module".format())
logging.error("Started error logging in test module".format())
logging.info("Started info logging in test module".format())
logging.debug("Started error logging in test module".format())


# logging.getLogger('boto3').setLevel(logging.WARNING)
# logging.getLogger('botocore').setLevel(logging.WARNING)
# logging.getLogger('nose').setLevel(logging.WARNING)
# logging.getLogger('s3transfer').setLevel(logging.CRITICAL)


def test_complete(caplog):
    caplog.set_level(logging.DEBUG)

    # Create folder, upload file, list files, download file, delete file
    x = 1 + 1
    print(x)

    dpl = Plugin()
    logging.error("Started logging ERROR in test module".format())
    logging.debug("Started logging DEBUG in test module".format())

    #dpl.create_directory(f's3://ocean-test-osmosis-data-plugin/test')
    #dpl.upload('./LICENSE', f's3://ocean-test-osmosis-data-plugin/test/LICENSE')
    #files = dpl.list(f's3://ocean-test-osmosis-data-plugin/test/')
    #assert len(files) == 2  # /test and /test/LICENSE
    #assert files[0]['Key'] == 'test/'
    # assert files[1]['Key'] == 'test/LICENSE'
    # dpl.download(f's3://ocean-test-osmosis-data-plugin/test/LICENSE', '/tmp/test_osmosis_data_plugin_license')
    # assert cmp('./LICENSE', '/tmp/test_osmosis_data_plugin_license')
    # dpl.delete(f's3://ocean-test-osmosis-data-plugin/test/LICENSE')
    # files = dpl.list(f's3://ocean-test-osmosis-data-plugin/test/')
    # assert len(files) == 1
    # assert files[0]['Key'] == 'test/'
    # dpl.delete_bucket('ocean-test-osmosis-data-plugin')


#test_complete()