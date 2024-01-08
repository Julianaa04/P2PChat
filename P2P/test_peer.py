import unittest
from unittest.mock import MagicMock, patch
import threading
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

    def tearDown(self):
        print("login")
        self.peer_instance.tcpClientSocket.close()

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

    def test_login_wrong_password(self):
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

    def tearDown(self):
        print("online peers")
        self.peer_instance.tcpClientSocket.close()

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

    def tearDown(self):
        print("create account")
        self.peer_instance.tcpClientSocket.close()

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
        print("test_create_account_success completed")

    def test_create_account_exist(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        self.peer_instance.tcpClientSocket.recv.return_value = b'join-exist'

        # Act
        self.peer_instance.createAccount(username, password)

        # Assert
        self.peer_instance.tcpClientSocket.send.assert_called_once_with(b'JOIN testUser testPassword')


class TestSearchUser(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("search user")
        self.peer_instance.tcpClientSocket.close()

    def test_search_user(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'search-success 1234:5678'
        # Act
        output = self.peer_instance.searchUser(username)

        # Assert
        self.assertEqual(output, '1234:5678')

    def test_search_user_notOnline(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'search-user-not-online 1234:5678'

        # Act
        output = self.peer_instance.searchUser(username)

        # Assert
        self.assertEqual(output, 0)

    def test_search_user_notFound(self):
        # Arrange
        username = 'testUser'
        password = 'testPassword'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'search-user-not-found 1234:5678'
        # sys.stdout = StringIO()  # redirect stdout to a string buffer print in console

        # Act
        output = self.peer_instance.searchUser(username)

        # Assert
        # self.peer_instance.tcpClientSocket.send.assert_called_once_with(b'JOIN testUser testPassword') #check function get called
        # output = sys.stdout.getvalue().strip()  # get stdout content
        self.assertEqual(output, None)


class TestJoinChatroom(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()  # replace with your class name
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("login")
        self.peer_instance.tcpClientSocket.close()

    def test_chatroom_success(self):
        # Arrange
        chatroomName = 'testChatroomName'
        username = 'testUser'
        self.peer_instance.tcpClientSocket.recv.return_value = b'join-success'
        sys.stdout = StringIO()  # redirect stdout to a string buffer print in console

        # Act
        self.peer_instance.joinchatRoom(chatroomName, username)

        # Assert
        output = sys.stdout.getvalue().strip()  # get stdout content
        self.assertEqual(output, f'joined {chatroomName} successfully')

    def test_chatroom_exist(self):
        # Arrange
        chatroomName = 'testChatroomName'
        username = 'testUser'
        self.peer_instance.tcpClientSocket.recv.return_value = b'join-exist'
        sys.stdout = StringIO()  # redirect stdout to a string buffer print in console

        # Act
        self.peer_instance.joinchatRoom(chatroomName, username)

        # Assert
        output = sys.stdout.getvalue().strip()  # get stdout content
        self.assertEqual(output, 'you are already in chat room')

    # 
    @patch('threading.Timer')  # Remove autospec=True
    def test_chatroom_notfound(self, mock_timer):
        # Arrange
        chatroomName = 'testChatroomName'
        username = 'testUser'
        password = 'testPassword'
        self.peer_instance.loginCredentials = ('testUser', 'testPassword')
        self.peer_instance.tcpClientSocket.recv.return_value = b'Roomnotfound'
        sys.stdout = StringIO()  # redirect stdout to a string buffer print in console

        # Act
        self.peer_instance.joinchatRoom(chatroomName, username)

        # Assert
        output = sys.stdout.getvalue().strip()  # get stdout content

        # Assert
        # Ensure that logout is called with option=1
        self.assertEqual(output, 'Room not found\nlogging out')

class TestCreateChatroom(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("create chatroom")
        self.peer_instance.tcpClientSocket.close()

    def test_create_chatroom_success(self):
        # Arrange
        chatroomName = 'testChatroomName'
        RoomCreator = 'testUser'

        self.peer_instance.tcpClientSocket.recv.return_value = b'chatroom-success'
        sys.stdout = StringIO()  # redirect stdout to a string buffer

        # Act
        self.peer_instance.createChatroom(chatroomName, RoomCreator)

        # Assert
        self.peer_instance.tcpClientSocket.send.assert_called_once_with(b'CHATROOM testChatroomName testUser')
        output = sys.stdout.getvalue().strip()  # get stdout content
        self.assertEqual(output, Fore.LIGHTGREEN_EX + "Chatroom is created...")
        print("test_create_chatroom_success completed")

    def test_create_chatroom_exists(self):
        # Arrange
        chatroomName = 'testChatroomName'
        RoomCreator = 'testUser'

        self.peer_instance.tcpClientSocket.recv.return_value = b'chatroom-exist'
        sys.stdout = StringIO()  # redirect stdout to a string buffer

        # Act
        self.peer_instance.createChatroom(chatroomName, RoomCreator)

        # Assert
        self.peer_instance.tcpClientSocket.send.assert_called_once_with(b'CHATROOM testChatroomName testUser')
        output = sys.stdout.getvalue().strip()  # get stdout content
        self.assertEqual(output, Fore.LIGHTYELLOW_EX + "Chatroom name already existed, choose another name...")
        # self.peer_instance.tcpClientSocket.close()


class TestSearchChatroom(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("search chatroom")
        self.peer_instance.tcpClientSocket.close()

    def test_search_chatroom(self):
        # Arrange
        chatroomName = 'testChatroomName'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'search-success 1234:5678'
        # sys.stdout = StringIO()  # redirect stdout to a string buffer print in console

        # Act
        output = self.peer_instance.SearchchatRoom(chatroomName)

        # Assert
        # self.peer_instance.tcpClientSocket.send.assert_called_once_with(b'JOIN testUser testPassword') #check function get called
        # output = sys.stdout.getvalue().strip()  # get stdout content
        self.assertEqual(output, '1234:5678')

    def test_chatroom_notFound(self):
        # Arrange
        chatroomName = 'testChatroomName'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'chatroom-not-found 1234:5678'

        # Act
        output = self.peer_instance.SearchchatRoom(chatroomName)

        # Assert
        self.assertEqual(output, None)


class TestGetListUsersInChatroom(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("list user in chatrooms")
        self.peer_instance.tcpClientSocket.close()

    def test_get_list_users(self):
        mock_list = ['testUser1', 'testUser2', 'testUser3']

        expected_output = mock_list
        # Arrange
        chatroomName = 'testChatroomName'
        peerServerPort = 5678
        self.peer_instance.tcpClientSocket.recv.return_value = b'onlineusers:testUser1:testUser2:testUser3'

        # Act
        result = self.peer_instance.list_Chatrooms(chatroomName)

        # Assert
        self.assertEqual(result, expected_output)


class TestLeaveChatroom(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()  # replace with your class name
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("leave")
        self.peer_instance.tcpClientSocket.close()

    def test_Leave_chatroom_success(self):
        # Arrange
        chatroomName = 'testChatroomName'
        username = 'testUser'
        self.peer_instance.tcpClientSocket.recv.return_value = b'Left room successfully'

        # Act
        output = self.peer_instance.LeaveRoom(chatroomName, username)

        self.assertEqual(output, 'Left room successfully')

    def test_Leave_chatroom_user_notExists(self):
        # Arrange
        chatroomName = 'testChatroomName'
        username = 'testUser'
        self.peer_instance.tcpClientSocket.recv.return_value = b'User not in the chatroom'

        # Act
        output = self.peer_instance.LeaveRoom(chatroomName, username)

        self.assertEqual(output, 'User not in the chatroom')


class TestDeleteChatroom(unittest.TestCase):
    def setUp(self):
        self.peer_instance = peer.peerMain()  # replace with your class name
        self.peer_instance.tcpClientSocket = MagicMock()
        self.peer_instance.registryName = 'testRegistry'
        self.peer_instance.registryPort = 1234

    def tearDown(self):
        print("leave")
        self.peer_instance.tcpClientSocket.close()

    def test_delete_chatroom_success(self):
        # Arrange
        chatroomName = 'testChatroomName'
        username = 'testUser'

        # Act
        self.peer_instance.tcpClientSocket.recv.return_value = b'delete room successfully'
        sys.stdout = StringIO()  # redirect stdout to a string buffer
        output = self.peer_instance.deleteChatRoom(chatroomName, username)

        # Assert
        self.peer_instance.tcpClientSocket.send.assert_called_once_with(b'DeleteCHATROOM testChatroomName testUser')
        # output = sys.stdout.getvalue().strip()  # get stdout content
        self.assertEqual(output, f"delete room successfully")

    def test_delete_chatroom_user_notCreator(self):
        # Arrange
        chatroomName = 'testChatroomName'
        username = 'testUser'
        self.peer_instance.tcpClientSocket.recv.return_value = b'User is not the creator of the chatroom'

        # Act
        output = self.peer_instance.deleteChatRoom(chatroomName, username)
        self.assertEqual(output, 'User is not the creator of the chatroom')

    def test_delete_chatroom_user_notExists(self):
        # Arrange
        chatroomName = 'testChatroomName'
        username = 'testUser'
        self.peer_instance.tcpClientSocket.recv.return_value = b'Chatroom does not exist'

        # Act
        output = self.peer_instance.deleteChatRoom(chatroomName, username)
        self.assertEqual(output, 'Chatroom does not exist')
