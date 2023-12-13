import pytest
from unittest.mock import patch
from scapy.all import ICMP, IP, UDP, RandShort
from ..udp_scanner import single_udp_scan

@pytest.fixture
def mock_gethostbyname(mocker):
    return mocker.patch('socket.gethostbyname', return_value='192.168.101.1')

@pytest.fixture
def mock_sr1(mocker):
    return mocker.patch('scapy.all.sr1')

def test_single_udp_scan_open_port(mock_gethostbyname, mock_sr1):
    """
    Test single_udp_scan function with an open port.
    """
    # Mock the response to simulate no response (open|filtered)
    mock_sr1.return_value = None
    
    assert single_udp_scan('example.com', 53) == 'Open|Filtered'

def test_single_udp_scan_closed_port(mock_gethostbyname, mock_sr1):
    """
    Test single_udp_scan function with a closed port.
    """
    # Mock the response to simulate a closed port
    icmp_response = ICMP(type=3, code=3)  # Adjust type and code as needed
    mock_sr1.return_value = IP()/icmp_response
    
    assert single_udp_scan('example.com', 53) == 'Closed'

def test_single_udp_scan_filtered_port(mock_gethostbyname, mock_sr1):
    """
    Test single_udp_scan function with a filtered port.
    """
    # Mock the response to simulate a filtered port (non-matching ICMP type/code)
    icmp_response = ICMP(type=5, code=1)  # Non-matching type/code
    mock_sr1.return_value = IP()/icmp_response
    
    assert single_udp_scan('example.com', 53) == 'Filtered'

def test_single_udp_scan_exception(mock_gethostbyname, mock_sr1):
    """
    Test single_udp_scan function with an exception.
    """
    # Mock socket.gethostbyname to raise an exception
    mock_gethostbyname.side_effect = Exception('Test exception')
    
    assert single_udp_scan('example.com', 53) == 'Error: Test exception'
