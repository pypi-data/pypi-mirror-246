import pytest
from unittest.mock import patch
import socket
from ..banner_grabber import grab_banner

# Define a fixture to mock socket.socket
@pytest.fixture
def mock_socket(mocker):
    return mocker.patch('socket.socket')

def test_grab_banner_with_tcp_protocol(mock_socket):
    """
    Test grab_banner function with TCP protocol and a received banner.
    """
    # Create a mock socket instance
    mock_socket_instance = mock_socket.return_value
    
    # Configure the mock socket instance to return a banner when recv is called
    mock_socket_instance.recv.return_value = b'This is a banner'
    
    banner = grab_banner('example.com', 80, protocol='TCP')
    
    assert banner == 'This is a banner'

def test_grab_banner_with_udp_protocol(mock_socket):
    """
    Test grab_banner function with UDP protocol and a received banner.
    """
    # Create a mock socket instance
    mock_socket_instance = mock_socket.return_value
    
    # Configure the mock socket instance to return a banner when recvfrom is called
    mock_socket_instance.recvfrom.return_value = (b'This is a banner', ('example.com', 80))
    
    banner = grab_banner('example.com', 80, protocol='UDP')
    
    assert banner == 'This is a banner'

def test_grab_banner_with_tcp_protocol_no_banner(mock_socket):
    """
    Test grab_banner function with TCP protocol and no banner received.
    """
    # Create a mock socket instance
    mock_socket_instance = mock_socket.return_value
    
    # Configure the mock socket instance to return an empty response
    mock_socket_instance.recv.return_value = b''
    
    banner = grab_banner('example.com', 80, protocol='TCP')
    
    assert banner == 'No banner received'

def test_grab_banner_with_exception(mock_socket):
    """
    Test grab_banner function with an exception.
    """
    # Create a mock socket instance and configure it to raise an exception
    mock_socket_instance = mock_socket.return_value
    mock_socket_instance.connect.side_effect = Exception('Test exception')
    
    result = grab_banner('example.com', 80, protocol='TCP')
    
    assert result == 'Error: Test exception'
