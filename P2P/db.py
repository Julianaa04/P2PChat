from pymongo import MongoClient

class DB:
    # Constructor method
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['p2p-chat']

    # checks if an account with the username exists
    def is_account_exist(self, username):
        user_exists = self.db.accounts.find_one({'username': username})
        if user_exists is not None:
            return True
        else:
            return False

    def is_chatroom_exist(self, chatroomName):
        chatroom_exists = self.db.chatrooms.find_one({'chatroomName': chatroomName})
        if chatroom_exists is not None:
            return True
        else:
            return False

    # adds a chatroom to the database
    def addChatroom(self, chatroomName, RoomCreator):
        if not self.is_chatroom_exist(chatroomName):
            chatroom = {
                "chatroomName": chatroomName,
                "RoomCreator": RoomCreator,
                "peers": [RoomCreator]  # list of peers where beginning of list is hostname
            }
            self.db.accounts.update_one(
                {"username": RoomCreator}, {"$push": {"ChatRooms": chatroomName}}
            )
            self.db.chatrooms.insert_one(chatroom)

    def JoinChatRoom(self, chatroomName, username):  # add members to chatroom and update if new peer joined
        if not self.FindUserinChatroom(chatroomName,username):
            self.db.chatrooms.update_one(
                {"chatroomName": chatroomName}, {"$push": {"peers": username}}
            )
            self.db.accounts.update_one(
                {"username": username}, {"$push": {"ChatRooms": chatroomName}}
            )

    def FindUserinChatroom(self,chatroomName, username):
        return self.db.chatrooms.count_documents({'chatroomName': chatroomName, 'peers': username}) > 0

    def get_users(self, chatroomName):
        ChatRoom = self.db.chatrooms.find_one({"chatroomName": chatroomName})
        if ChatRoom and 'peers' in ChatRoom:
            # Return the list of users
            return ChatRoom['peers']

    def userDetails(self, chatroomName,roomCreator):
        ChatRoom = self.db.chatrooms.find_one({"chatroomName": chatroomName})
        if ChatRoom:
            peers = ChatRoom.get("RoomCreator", [])

            if roomCreator in peers:
                return roomCreator  # Return the room creator if found

    def register(self, username, password):
        account = {
            "username": username,
            "password": password
        }
        self.db.accounts.insert_one(account)

    # retrieves the password for a given username
    def get_password(self, username):
        return self.db.accounts.find_one({"username": username})["password"]

    # checks if an account with the username online
    def is_account_online(self, username):
        if self.db.online_peers.count_documents({"username": username}) > 0:
            return True
        else:
            return False

    # logs in the user
    def user_login(self, username, ip, port):
        online_peer = {
            "username": username,
            "ip": ip,
            "port": port
        }
        self.db.online_peers.insert_one(online_peer)

    # logs out the user
    def user_logout(self, username):
        self.db.online_peers.delete_one({"username": username})

    # retrieves the ip address and the port number of the username
    def get_peer_ip_port(self, username):
        res = self.db.online_peers.find_one({"username": username})
        return res["ip"], res["port"]

    def leave_Chatroom(self, chatroom, username):
        chatroom_exists = self.db.chatrooms.find_one({'chatroomName': chatroom})

        updated_peers = [
            user
            for user in chatroom_exists.get('peers', [])
            if user != username
        ]

        self.db.chatrooms.update_one(
            {"chatroomName": chatroom},
            {'$set': {'peers': updated_peers}}
        )
        #print(f"User {username} removed from chatroom {chatroom} successfully.")

    def delete_chatroom(self, chatroom, RoomCreator):
        # Check if the chatroom exists
        if self.is_chatroom_exist(chatroom):
            # Check if the requesting user is the creator of the chatroom
            chatroom_data = self.db.chatrooms.find_one({"chatroomName": chatroom})
            if chatroom_data and chatroom_data["RoomCreator"] == RoomCreator:
                # Delete the chatroom
                self.db.chatrooms.delete_one({"chatroomName": chatroom})
                print("Chatroom deleted successfully")
            else:
                print("You are not the creator of the chatroom. Deletion failed.")
        else:
            print("Chatroom does not exist. Deletion failed.")
