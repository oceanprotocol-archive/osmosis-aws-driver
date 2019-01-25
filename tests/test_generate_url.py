import requests

from osmosis_aws_driver.data_plugin import Plugin


def test_generate_url():
    config = dict()  #
    s3_plugin = Plugin(config)

    sign_url = s3_plugin.generate_url(
        's3://ocean-test-osmosis-data-plugin-dataseeding-1537375953/data.txt')
    assert requests.get(sign_url).content == b'1 2\n2 3\n3 4\n'
