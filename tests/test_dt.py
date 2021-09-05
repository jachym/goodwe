import asyncio
import os
from datetime import datetime
from unittest import TestCase

from goodwe.dt import DT
from goodwe.exceptions import RequestFailedException
from goodwe.protocol import ProtocolCommand


class DtMock(TestCase, DT):

    def __init__(self, methodName='runTest'):
        TestCase.__init__(self, methodName)
        DT.__init__(self, "localhost", 8899)
        self.sensor_map = {s.id_: s.unit for s in self.sensors()}
        self._mock_responses = {}

    def mock_response(self, command: ProtocolCommand, filename: str):
        self._mock_responses[command] = filename

    async def _read_from_socket(self, command: ProtocolCommand) -> bytes:
        """Mock UDP communication"""
        root_dir = os.path.dirname(os.path.abspath(__file__))
        filename = self._mock_responses.get(command)
        if filename is not None:
            with open(root_dir + '/sample/dt/' + filename, 'r') as f:
                response = bytes.fromhex(f.read())
                if not command.validator(response):
                    raise RequestFailedException
                return response
        else:
            self.request = command.request
            return bytes.fromhex("010203040506070809")

    def assertSensor(self, sensor, expected_value, expected_unit, data):
        self.assertEqual(expected_value, data.get(sensor))
        self.assertEqual(expected_unit, self.sensor_map.get(sensor))

    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.get_event_loop()


class GW6000_DT_Test(DtMock):

    def __init__(self, methodName='runTest'):
        DtMock.__init__(self, methodName)
        self.mock_response(self._READ_DEVICE_RUNNING_DATA, 'GW6000-DT_running_data.hex')

    def test_GW6000_DT_runtime_data(self):
        data = self.loop.run_until_complete(self.read_runtime_data(True))
        self.assertEqual(76, len(data))

        self.assertSensor('timestamp', datetime.strptime('2021-08-31 12:03:02', '%Y-%m-%d %H:%M:%S'), '', data)
        self.assertSensor('vpv1', 320.8, 'V', data)
        self.assertSensor('ipv1', 3.1, 'A', data)
        self.assertSensor('ppv1', 994, 'W', data)
        self.assertSensor('vpv2', 324.1, 'V', data)
        self.assertSensor('ipv2', 3.2, 'A', data)
        self.assertSensor('ppv2', 1037, 'W', data)
        self.assertSensor('xx14', -1, '', data)
        self.assertSensor('xx16', -1, '', data)
        self.assertSensor('xx18', -1, '', data)
        self.assertSensor('xx20', -1, '', data)
        self.assertSensor('xx22', -1, '', data)
        self.assertSensor('xx24', -1, '', data)
        self.assertSensor('xx26', -1, '', data)
        self.assertSensor('xx28', -1, '', data)
        self.assertSensor('vline1', -0.1, 'V', data)
        self.assertSensor('vline2', -0.1, 'V', data)
        self.assertSensor('vline3', -0.1, 'V', data)
        self.assertSensor('vgrid1', 225.6, 'V', data)
        self.assertSensor('vgrid2', 229.7, 'V', data)
        self.assertSensor('vgrid3', 231.0, 'V', data)
        self.assertSensor('igrid1', 2.7, 'A', data)
        self.assertSensor('igrid2', 2.6, 'A', data)
        self.assertSensor('igrid3', 2.7, 'A', data)
        self.assertSensor('fgrid1', 49.98, 'Hz', data)
        self.assertSensor('fgrid2', 49.98, 'Hz', data)
        self.assertSensor('fgrid3', 49.98, 'Hz', data)
        self.assertSensor('pgrid1', 609, 'W', data)
        self.assertSensor('pgrid2', 597, 'W', data)
        self.assertSensor('pgrid3', 624, 'W', data)
        self.assertSensor('xx54', 0, '', data)
        self.assertSensor('ppv', 1835, 'W', data)
        self.assertSensor('work_mode', 1, '', data)
        self.assertSensor('work_mode_label', 'Normal', '', data)
        self.assertSensor('xx60', 0, '', data)
        self.assertSensor('xx62', 0, '', data)
        self.assertSensor('xx64', 0, '', data)
        self.assertSensor('xx66', -1, '', data)
        self.assertSensor('xx68', -1, '', data)
        self.assertSensor('xx70', -1, '', data)
        self.assertSensor('xx72', -1, '', data)
        self.assertSensor('xx74', -1, '', data)
        self.assertSensor('xx76', -1, '', data)
        self.assertSensor('xx78', 0, '', data)
        self.assertSensor('xx80', -1, '', data)
        self.assertSensor('temperature', 41.3, 'C', data)
        self.assertSensor('xx84', -1, '', data)
        self.assertSensor('xx86', -1, '', data)
        self.assertSensor('e_day', 6.0, 'kWh', data)
        self.assertSensor('e_total', 13350.2, 'kWh', data)
        self.assertSensor('h_total', 8451, 'h', data)
        self.assertSensor('safety_country', 20, '', data)
        self.assertSensor('safety_country_label', 'Holland', '', data)
        self.assertSensor('xx100', 0, '', data)
        self.assertSensor('xx102', -1, '', data)
        self.assertSensor('xx104', 0, '', data)
        self.assertSensor('xx106', -1, '', data)
        self.assertSensor('xx108', 0, '', data)
        self.assertSensor('xx110', -1, '', data)
        self.assertSensor('xx112', 0, '', data)
        self.assertSensor('xx114', -1, '', data)
        self.assertSensor('xx116', -1, '', data)
        self.assertSensor('xx118', -1, '', data)
        self.assertSensor('xx120', -1, '', data)
        self.assertSensor('xx122', -1, '', data)
        self.assertSensor('funbit', 0, '', data)
        self.assertSensor('vbus', 601.2, 'V', data)
        self.assertSensor('vnbus', 305.4, 'V', data)
        self.assertSensor('xx130', -1, '', data)
        self.assertSensor('xx132', -1, '', data)
        self.assertSensor('xx134', 207, '', data)
        self.assertSensor('xx136', 355, '', data)
        self.assertSensor('xx138', 752, '', data)
        self.assertSensor('xx140', 0, '', data)
        self.assertSensor('xx142', 0, '', data)
        self.assertSensor('xx144', 100, '', data)


class GW8K_DT_Test(DtMock):

    def __init__(self, methodName='runTest'):
        DtMock.__init__(self, methodName)
        self.mock_response(self._READ_DEVICE_RUNNING_DATA, 'GW8K-DT_running_data.hex')
        self.mock_response(self._READ_DEVICE_VERSION_INFO, 'GW8K-DT_device_info.hex')

    def test_GW8K_DT_runtime_data(self):
        data = self.loop.run_until_complete(self.read_runtime_data(True))
        self.assertEqual(76, len(data))

        self.assertSensor('timestamp', datetime.strptime('2021-08-24 16:43:27', '%Y-%m-%d %H:%M:%S'), '', data)
        self.assertSensor('vpv1', 275.5, 'V', data)
        self.assertSensor('ipv1', 0.6, 'A', data)
        self.assertSensor('ppv1', 165, 'W', data)
        self.assertSensor('vpv2', 510.8, 'V', data)
        self.assertSensor('ipv2', 0.8, 'A', data)
        self.assertSensor('ppv2', 409, 'W', data)
        self.assertSensor('xx14', -1, '', data)
        self.assertSensor('xx16', -1, '', data)
        self.assertSensor('xx18', -1, '', data)
        self.assertSensor('xx20', -1, '', data)
        self.assertSensor('xx22', -1, '', data)
        self.assertSensor('xx24', -1, '', data)
        self.assertSensor('xx26', -1, '', data)
        self.assertSensor('xx28', -1, '', data)
        self.assertSensor('vline1', 413.7, 'V', data)
        self.assertSensor('vline2', 413.0, 'V', data)
        self.assertSensor('vline3', 408.0, 'V', data)
        self.assertSensor('vgrid1', 237.2, 'V', data)
        self.assertSensor('vgrid2', 240.5, 'V', data)
        self.assertSensor('vgrid3', 235.2, 'V', data)
        self.assertSensor('igrid1', 1.0, 'A', data)
        self.assertSensor('igrid2', 1.0, 'A', data)
        self.assertSensor('igrid3', 1.0, 'A', data)
        self.assertSensor('fgrid1', 50.08, 'Hz', data)
        self.assertSensor('fgrid2', 50.04, 'Hz', data)
        self.assertSensor('fgrid3', 50.0, 'Hz', data)
        self.assertSensor('pgrid1', 237, 'W', data)
        self.assertSensor('pgrid2', 240, 'W', data)
        self.assertSensor('pgrid3', 235, 'W', data)
        self.assertSensor('xx54', 0, '', data)
        self.assertSensor('ppv', 643, 'W', data)
        self.assertSensor('work_mode', 1, '', data)
        self.assertSensor('work_mode_label', 'Normal', '', data)
        self.assertSensor('xx60', 0, '', data)
        self.assertSensor('xx62', 0, '', data)
        self.assertSensor('xx64', 0, '', data)
        self.assertSensor('xx66', 0, '', data)
        self.assertSensor('xx68', 0, '', data)
        self.assertSensor('xx70', 0, '', data)
        self.assertSensor('xx72', 0, '', data)
        self.assertSensor('xx74', 0, '', data)
        self.assertSensor('xx76', 0, '', data)
        self.assertSensor('xx78', 0, '', data)
        self.assertSensor('xx80', -1, '', data)
        self.assertSensor('temperature', 45.3, 'C', data)
        self.assertSensor('xx84', -1, '', data)
        self.assertSensor('xx86', -1, '', data)
        self.assertSensor('e_day', -0.1, 'kWh', data)
        self.assertSensor('e_total', -0.1, 'kWh', data)
        self.assertSensor('h_total', -1, 'h', data)
        self.assertSensor('safety_country', 32, '', data)
        self.assertSensor('safety_country_label', '50Hz Grid Default', '', data)
        self.assertSensor('xx100', 0, '', data)
        self.assertSensor('xx102', 0, '', data)
        self.assertSensor('xx104', 0, '', data)
        self.assertSensor('xx106', 0, '', data)
        self.assertSensor('xx108', -1, '', data)
        self.assertSensor('xx110', -1, '', data)
        self.assertSensor('xx112', -1, '', data)
        self.assertSensor('xx114', -1, '', data)
        self.assertSensor('xx116', -1, '', data)
        self.assertSensor('xx118', -1, '', data)
        self.assertSensor('xx120', -1, '', data)
        self.assertSensor('xx122', -1, '', data)
        self.assertSensor('funbit', 512, '', data)
        self.assertSensor('vbus', 624.2, 'V', data)
        self.assertSensor('vnbus', 316.8, 'V', data)
        self.assertSensor('xx130', 0, '', data)
        self.assertSensor('xx132', 0, '', data)
        self.assertSensor('xx134', 0, '', data)
        self.assertSensor('xx136', 728, '', data)
        self.assertSensor('xx138', 129, '', data)
        self.assertSensor('xx140', 0, '', data)
        self.assertSensor('xx142', -1, '', data)
        self.assertSensor('xx144', 84, '', data)
