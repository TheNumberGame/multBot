import asyncio
import pprint

import discord
import praw

discord_client = discord.Client()

def load_discord_token():
	with open("discord_credentials.txt") as fp:
		return fp.read().strip()

def main():
	discord_client.run(load_discord_token())

@discord_client.event
async def on_message(message):
	if message.content.startswith('//top'):
		print(message.content)
		await discord_client.send_message(message.channel, "message received")
	
def main_reddit():
	reddit = praw.Reddit("multBot")
	subreddit = reddit.subreddit("multBot")
	for submission in subreddit.stream.submissions():
		if submission.saved:
			continue
		print(submission.title)
		submission.reply("A Comment")
		submission.save()
	
if __name__ == "__main__":
	main()