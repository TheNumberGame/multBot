import asyncio
import pprint

import discord
import praw
import logging

logging.basicConfig(level=logging.INFO)


event_loop = asyncio.get_event_loop()

discord_client = discord.Client(loop = event_loop)
reddit = praw.Reddit("multBot")
PINNED_SUBMISSION = reddit.submission(id="8alcez")
submission_stream = reddit.subreddit("multBot").stream.submissions(pause_after = -1)
comment_stream = reddit.subreddit("multBot").stream.comments(pause_after = -1)
DISCORD_USERNAME = "multBot"

def load_discord_token():
	with open("discord_credentials.txt") as fp:
		return fp.read().strip()

def main():
	event_loop.call_later(5, timed_callback)
	discord_client.run(load_discord_token())

async def reddit_task():
	submission = next(submission_stream)
	while submission is not None:
		if not submission.saved:
			await discord_client.send_message(discord_client.get_channel("432274642514739201"), "https://www.reddit.com" + submission.permalink)
			submission.save()
		
		submission = next(submission_stream)
	
	comment = next(comment_stream)
	discord_portal_channel = discord_client.get_channel("432295161301827595")
	member = discord_portal_channel.server.me
	while comment is not None:
		if comment.submission == PINNED_SUBMISSION and comment.author != reddit.config.username and not comment.saved:
			await discord_client.change_nickname(member, comment.author.name)
			await discord_client.send_message(discord_portal_channel, comment.body)
			await discord_client.change_nickname(member, DISCORD_USERNAME)
			comment.save()
		comment = next(comment_stream)
	
	event_loop.call_later(5, timed_callback)

def timed_callback():
	event_loop.create_task(reddit_task())
	
@discord_client.event
async def on_message(message):
	await on_poll(message)
	await on_submission(message, "hot")
	await on_submission(message, "new")
	await on_submission(message, "top")
	await on_submission(message, "random")
	await on_submission(message, "rising")
	await on_submission(message, "controversial")
	await on_submission(message, "gilded")
	await reddit_portal_comment(message)
	

#@discord_client.event
#async def on_reaction_add(reaction, user):
		
	
async def reddit_portal_comment(message):
	if message.channel.id == "432295161301827595" and message.author.name != DISCORD_USERNAME:
		if not message.content == "":
			PINNED_SUBMISSION.reply(message.author.name + ": " + message.content)
		else:
			PINNED_SUBMISSION.reply(message.author.name + ": " + message.attachments[0]['url'])
		
async def on_submission(message, category):
	if message.content.startswith('//' + category):
		tokens = message.content.split(" ", 1)
		
		if len(tokens) == 1:
			await discord_client.send_message(message.channel, "Give us a real subreddit")
		else:
			try:
				subreddit = reddit.subreddit(tokens[1])
				if category == "random":
					submission = subreddit.random()
				else:
					submission = unstickied_submission(subreddit, category)
				await discord_client.send_message(message.channel, "https://www.reddit.com" + submission.permalink)
			except Exception as e:
				await discord_client.send_message(message.channel, "Invalid subreddit")
				print(e)

async def on_poll(message):
	if message.content.startswith('//poll'):
		tokens = message.content.split(" ", 1)
		if len(tokens) == 1:
			await discord_client.send_message(message.channel, "What's the question?")
		else:
			sent_message = await discord_client.send_message(message.channel, tokens[1] + "\n\n \N{THUMBS UP SIGN} YES \n\n \N{THUMBS DOWN SIGN} NO")
			await discord_client.add_reaction(sent_message, '\N{THUMBS UP SIGN}')
			await discord_client.add_reaction(sent_message, '\N{THUMBS DOWN SIGN}')

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