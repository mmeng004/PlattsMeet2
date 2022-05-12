from enum import Enum

#Based on the tutorial from #https://codingwithmitch.com/courses/real-time-chat-messenger/-->
class FriendRequestStatus(Enum):
	NO_REQUEST_SENT = -1
	THEM_SENT_TO_YOU = 0
	YOU_SENT_TO_THEM = 1

