import pprint
import praw

def main():
	reddit = praw.Reddit("multBot")
	subreddit = reddit.subreddit("multBot")
	for submission in subreddit.stream.submissions():
		print(submission.title)
		submission.reply("A Comment")
	
if __name__ == "__main__":
	main()