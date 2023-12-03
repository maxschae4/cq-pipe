import json
import unittest

from cq_pipe.transform import Host


class TestHostFromCrowdstrike(unittest.TestCase):
    def setUp(self):
        with open("tests/crowdstrike_aws_host.json", "r") as aws_host:
            self.aws_host = json.load(aws_host)
        with open("tests/crowdstrike_apple_host.json", "r") as apple_host:
            self.apple_host = json.load(apple_host)

    def test_aws_host_from_crowdstrike(self):
        """
        Regression test against expected results of marshaling an AWS Host.
        """
        test_host = Host.from_crowdstrike(self.aws_host)
        expected_host = Host(
            crowdstrike_device_id="e64d9e3eb9f24f44818240d7f9ad4ebc",
            kind="AWS",
            kind_id="i-086fc5a571e41b095",
        )
        self.assertEqual(test_host, expected_host)

    def test_apple_host_from_crowdstrike(self):
        """
        Regression test against expected results of marshaling an Apple Host.
        """
        test_host = Host.from_crowdstrike(self.apple_host)
        expected_host = Host(
            crowdstrike_device_id="3023b0ecd1444cf3b0b0958cb437964c",
            kind="Apple",
            kind_id="ABC1234567",
        )
        self.assertEqual(test_host, expected_host)


class TestHostFromQualys(unittest.TestCase):
    def setUp(self):
        with open("tests/qualys_aws_host.json", "r") as aws_host:
            self.aws_host = json.load(aws_host)

    def test_aws_host_from_qualys(self):
        """
        Regression test against expected results of marshaling an AWS Host.
        """
        test_host = Host.from_qualys(self.aws_host)
        expected_host = Host(
            qualys_device_id="305003660",
            kind="AWS",
            kind_id="i-0f74daf3d7225083a",
        )
        self.assertEqual(test_host, expected_host)
