from osmosis_driver_interface.osmosis import Osmosis
from osmosis_aws_driver.data_plugin import S3_Plugin
from filecmp import cmp
import os
import time
from osmosis_aws_driver.config_parser import load_config_section

# os.environ['AWS_PROFILE'] = 'ocean'
# Why was this needed???
#aws = Osmosis('./tests/aws.ini').data_plugin()



# def test_plugin_type():
#     assert aws.type == 'AWS'


def test_complete():
    # Create folder, upload file, list files, download file, delete file
    # TODO: Add finally to clean s3 bucket

    config = load_config_section(file_path='aws.ini', section='S3')

    dpl = S3_Plugin(config)

    #dpl = S3_Plugin()
    bucket_name=f'ocean-test-osmosis-data-plugin-{int(time.time())}'
    print(f'Test bucket: {bucket_name}')
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


test_complete()