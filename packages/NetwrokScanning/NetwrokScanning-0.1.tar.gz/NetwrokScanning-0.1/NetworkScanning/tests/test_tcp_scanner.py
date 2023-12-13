import pytest
from unittest.mock import patch
from scapy.layers.inet import TCP
from ..tcp_scanner import single_tcp_scan

@pytest.fixture
def mock_gethostbyname(mocker):
    return mocker.patch('socket.gethostbyname', return_value='192.168.101.1')

@pytest.fixture
def mock_sr1(mocker):
    return mocker.patch('NetworkScanning.tcp_scanner.sr1')

def test_single_tcp_scan_with_open_port(mock_gethostbyname, mock_sr1):
    """
    Test single_tcp_scan function with an open port.
    """
    mock_sr1.return_value = TCP(flags='SA')
    assert single_tcp_scan('google.com', 80) == 'Open'

def test_single_tcp_scan_with_closed_port(mock_gethostbyname, mock_sr1):
    """
    Test single_tcp_scan function with a closed port.
    """
    mock_sr1.return_value = TCP(flags='R')
    assert single_tcp_scan('google.com', 80) == 'Closed'

def test_single_tcp_scan_with_filtered_port(mock_gethostbyname, mock_sr1):
    """
    Test single_tcp_scan function with a filtered port.
    """
    mock_sr1.return_value = None
    assert single_tcp_scan('google.com', 80) == 'Filtered'

def test_single_tcp_scan_with_exception(mock_gethostbyname, mock_sr1):
    """
    Test single_tcp_scan function with an exception.
    """
    mock_gethostbyname.side_effect = Exception('Test exception')
    assert single_tcp_scan('example.com', 80) == 'Exception occurred'
