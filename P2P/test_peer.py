import unittest
from unittest.mock import MagicMock
from io import StringIO
import sys
from colorama import Fore, Back
import peer

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()  # replace with your class name
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def test_login_success(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'login-success'

        # Act
        result = self.peer_instance.login(username, password, peerServerPort)

        # Assert
        self.assertEqual(result, 1)

    def test_login_account_not_exist(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'login-account-not-exist'

        # Act
        result = self.peer_instance.login(username, password, peerServerPort)

        # Assert
        self.assertEqual(result, 0)

    def test_login_account_is_online(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'login-online'

        # Act
        result = self.peer_instance.login(username, password, peerServerPort)

        # Assert
        self.assertEqual(result, 2)

    def test_login_account_is_online(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'login-wrong-password'

        # Act
        result = self.peer_instance.login(username, password, peerServerPort)

        # Assert
        self.assertEqual(result, 3)

    

class TestGetOnlinePeers(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def test_get_online_peers(self):
        mock_list = ['testUser1', 'testUser2', 'testUser3']

        expected_output = "Online Peers: " + str(mock_list)
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = str(mock_list).encode('utf-8')

        # Act
        result = self.peer_instance.getOnlinePeers()

        # Assert
        self.assertEqual(result, expected_output)


class TestCreateAccount(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain() 
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def test_create_account_success(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        self.peer_instance.tcpClientSocket.recv.return_value = b'join-success'
        sys.stdout = StringIO()  # redirect stdout to a string buffer

        # Act
        self.peer_instance.createAccount(username, password)

        # Assert
        self.peer_instance.tcpClientSocket.send.assert_called_once_with(b'JOIN testUser testPassword')
        output = sys.stdout.getvalue().strip()  # get stdout content
        self.assertEqual(output, Fore.LIGHTGREEN_EX + "Account created...")


    def test_create_account_exist(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        self.peer_instance.tcpClientSocket.recv.return_value = b'join-exist'

        # Act
        self.peer_instance.createAccount(username, password)

        # Assert
        self.peer_instance.tcpClientSocket.send.assert_called_once_with(b'JOIN testUser testPassword')

    