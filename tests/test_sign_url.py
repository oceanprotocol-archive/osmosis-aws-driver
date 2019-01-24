from osmosis_aws_driver.data_S3_plugin import S3_Plugin
import requests


def test_generate_url():
    config = dict()  #
    s3_plugin = S3_Plugin(config)

    sasl_url = s3_plugin.generate_url(
        's3://tutorials.bigchaindb.com/data.txt')
    print(sasl_url)
    assert requests.get(sasl_url).content == b'1 2\n2 3\n3 4\n'

