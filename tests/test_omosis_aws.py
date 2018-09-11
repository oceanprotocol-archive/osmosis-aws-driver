from osmosis_driver_interface.osmosis import Osmosis
from osmosis_aws_driver.data_plugin import Plugin
from filecmp import cmp
import os

# os.environ['AWS_PROFILE'] = 'ocean'
aws = Osmosis('./tests/aws.ini').data_plugin()


def test_plugin_type():
    assert aws.type == 'AWS'


def test_complete():
    # Create folder, upload file, list files, download file, delete file
    bucket = 'ocean-test-osmosis-data-plugin'
    dpl = Plugin()
    print(dpl.list_buckets())
    dpl.create_directory(f's3://{bucket}/test')
    dpl.upload('./LICENSE', f's3://{bucket}/test/LICENSE')
    files = dpl.list(f's3://{bucket}/test/')
    assert len(files) == 2  # /test and /test/LICENSE
    assert files[0]['Key'] == 'test/'
    assert files[1]['Key'] == 'test/LICENSE'
    dpl.download(f's3://{bucket}/test/LICENSE', '/tmp/test_osmosis_data_plugin_license')
    assert cmp('./LICENSE', '/tmp/test_osmosis_data_plugin_license')
    dpl.delete(f's3://{bucket}/test/LICENSE')
    files = dpl.list(f's3://{bucket}/test/')
    assert len(files) == 1
    assert files[0]['Key'] == 'test/'
    dpl.delete_bucket(bucket)
