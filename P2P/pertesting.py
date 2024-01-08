import threading
import logging
import time
import random
from peer import peerMain
from socket import *

totaltimetojoin = 0
totaltimetocreate = 0
def generate_username():
    adjectives = ['happy', 'funny', 'smart', 'creative', 'awesome', 'crazy', 'colorful', 'beauty']
    nouns = ['cat', 'dog', 'bird', 'unicorn', 'wizard', 'dragon', 'robot', 'panda']
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    number = random.randint(0, 999)
    username = f'{adjective}_{noun}_{number}'
    return username

class testPerformanceThread(threading.Thread):
    """
    A class representing a performance testing thread.

    Args:
        user_id (int): The ID of the user.

    Attributes:
        user_id (int): The ID of the user.
        peer (peerMain): An instance of the peerMain class.
        logger (logging.Logger): The logger object for logging performance information.

    Methods:
        setup_logger: Sets up the logger object.
        run: Runs the performance testing for creating and joining a chatroom.
    """
    def __init__(self, user_id):
        self.user_id = user_id
        threading.Thread.__init__(self)
        new_logger = self.setup_logger()
        self.peer = peerMain()
        self.logger = new_logger

    def setup_logger(self):
        """
        Sets up the logger object.

        Returns:
            logging.Logger: The logger object.
        """
        logger = logging.getLogger(f"user_{self.user_id}")
        logger.setLevel(logging.INFO)
        return logger

    def run(self):
        """
        Runs the performance testing for creating and joining a chatroom.
        """
        global totaltimetojoin
        global totaltimetocreate
        username = generate_username()
        password = "pass123"
        self.peer.createAccount(username,password)
        sock = socket()
        sock.bind(('', 0))
        peerServerPort = sock.getsockname()[1]
        self.peer.login(username, password, peerServerPort)
        self.logger.info(f"Username: {username}")
        starttime=time.time()
        self.peer.createChatroom("testingperformance1",username)
        endtime = time.time()
        self.logger.info(f"Time to create chatroom: {endtime - starttime} seconds")
        totaltimetocreate += endtime - starttime
        starttime = time.time()
        self.peer.joinchatRoom("testingperformance1",username)
        endtime = time.time()
        self.logger.info(f"Time to join chatroom: {endtime - starttime} seconds")
        totaltimetojoin += endtime - starttime

        
def main():
    num_threads = 500
    threads = [testPerformanceThread(user_id=i) for i in range(num_threads)]
    for thread in threads:
        thread.start()
        time.sleep(.2)

    # Waiting for all users to join the chatroom
    time.sleep(2)  

    for thread in threads:
        thread.join()
    print('============================================================')
    print('Results of performance testing:')
    print("Avg time to join chatroom: ", totaltimetojoin / num_threads)
    print("Avg time to create a chatroom: ", totaltimetocreate / num_threads)
        

if __name__ == "__main__":
    main()
