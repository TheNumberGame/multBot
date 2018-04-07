import asyncio
import pprint

import discord
import praw

discord_client = discord.Client()
reddit = praw.Reddit("multBot")

def load_discord_token():
	with open("discord_credentials.txt") as fp:
		return fp.read().strip()

def main():
	discord_client.run(load_discord_token())

@discord_client.event
async def on_message(message):
	if message.content.startswith('//hot'):
		tokens = message.content.split(" ", 1)
		
		if len(tokens) == 1:
			await discord_client.send_message(message.channel, "Give us a real subreddit")
		else:
			subreddit = reddit.subreddit(tokens[1])
			submission = next(subreddit.hot())
			await discord_client.send_message(message.channel, "https://www.reddit.com" + submission.permalink)
	
def main_reddit():
	subreddit = reddit.subreddit("multBot")
	for submission in subreddit.stream.submissions():
		if submission.saved:
			continue
		print(submission.title)
		submission.reply("A Comment")
		submission.save()
	
if __name__ == "__main__":
	main()