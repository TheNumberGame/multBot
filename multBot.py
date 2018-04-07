import asyncio
import pprint

import discord
import praw

event_loop = asyncio.get_event_loop()

discord_client = discord.Client(loop = event_loop)
reddit = praw.Reddit("multBot")
mult_subreddit_stream = reddit.subreddit("multBot").stream.submissions(pause_after = -1)

def load_discord_token():
	with open("discord_credentials.txt") as fp:
		return fp.read().strip()

def main():
	event_loop.call_later(5, timed_callback)
	discord_client.run(load_discord_token())

async def reddit_task():
	submission = next(mult_subreddit_stream)
	while submission is not None:
		await discord_client.send_message(discord_client.get_channel("432274642514739201"), "https://www.reddit.com" + submission.permalink)
		submission = next(mult_subreddit_stream)
		
	event_loop.call_later(5, timed_callback)

def timed_callback():
	event_loop.create_task(reddit_task())
	
@discord_client.event
async def on_message(message):
	await on_submission(message, "hot")
	await on_submission(message, "new")
	await on_submission(message, "top")


async def on_submission(message, category):
	if message.content.startswith('//' + category):
		tokens = message.content.split(" ", 1)
		
		if len(tokens) == 1:
			await discord_client.send_message(message.channel, "Give us a real subreddit")
		else:
			try:
				subreddit = reddit.subreddit(tokens[1])
				submission = unstickied_submission(subreddit, category)
				await discord_client.send_message(message.channel, "https://www.reddit.com" + submission.permalink)
			except:
				await discord_client.send_message(message.channel, "Invalid subreddit")
	

def unstickied_submission(subreddit, listing):
	for submission in getattr(subreddit, listing)():
		if not submission.stickied:
			break
	return submission

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