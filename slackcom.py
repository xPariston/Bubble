from onboardingtutorial import OnboardingTutorial
import os
from boto.s3.connection import S3Connection
import logging
import slack
import ssl as ssl_lib
import certifi
import twitterscraper

pairs = {}

pairs["[kK]nock[, -]*[kK]nock"] = "Who's there?"
pairs["help"] = "YOUR INSTRUCTIONS HERE"

onboarding_tutorials_sent = {}


# ================ Team Join Event =============== #
# When the user first joins a team, the type of the event will be 'team_join'.
# Here we'll link the onboarding_message callback to the 'team_join' event.
@slack.RTMClient.run_on(event="team_join")
def onboarding_message(**payload):
    """Create and send an onboarding welcome message to new users. Save the
    time stamp of this message so we can update this message in the future.
    """
    # Get WebClient so you can communicate back to Slack.
    web_client = payload["web_client"]

    # Get the id of the Slack user associated with the incoming event
    user_id = payload["data"]["user"]["id"]

    # Open a DM with the new user.
    response = web_client.im_open(user_id)
    channel = response["channel"]["id"]

    # Post the onboarding message.
    start_onboarding(web_client, user_id, channel)


# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
@slack.RTMClient.run_on(event="reaction_added")
def update_emoji(**payload):
    """Update the onboarding welcome message after recieving a "reaction_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data["item"]["channel"]
    user_id = data["user"]

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

    # Mark the reaction task as completed.
    onboarding_tutorial.reaction_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]


# =============== Pin Added Events ================ #
# When a users pins a message the type of the event will be 'pin_added'.
# Here we'll link the update_pin callback to the 'reaction_added' event.
@slack.RTMClient.run_on(event="pin_added")
def update_pin(**payload):
    """Update the onboarding welcome message after recieving a "pin_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data["channel_id"]
    user_id = data["user"]

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

    # Mark the pin task as completed.
    onboarding_tutorial.pin_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]


@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    print("Reimann")
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")
    thread_ts = data['ts']

    if text and text.lower() == "start":
        return start_onboarding(web_client, user_id, channel_id)

    if text and text.lower() == "hi bot":
        web_client.chat_postMessage(channel=channel_id,
                text=f"Hi <@{user_id}>!",
                thread_ts=thread_ts)

    if text and text.lower() == "tweettest":
        posttwittermessages(420,web_client,channel_id)


def posttwittermessages(time, web_client, channel_id):
    twitterslacks = []
    tweets = twitterscraper.scrapetweets(time)
    for tweet in tweets:
        msg = "%s posted on Twitter:" % tweet.user
        att = [
            {
                "fallback": "Go to Tweet: %s" %tweet.url,
                "color": "#00acee",
                "text": tweet.tweet["text"] ,
                "actions": [
                    {
                        "type": "button",
                        "text": "Support 🚀",
                        "url": tweet.url
                    }
                ]
            }
        ]

        web_client.chat_postMessage(channel=channel_id,
                                    text=msg,
                                    attachments = att)




def start_onboarding(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    onboarding_tutorial = OnboardingTutorial(channel)

    # Get the onboarding message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    onboarding_tutorial.timestamp = response["ts"]

    # Store the message sent in onboarding_tutorials_sent
    if channel not in onboarding_tutorials_sent:
        onboarding_tutorials_sent[channel] = {}
    onboarding_tutorials_sent[channel][user_id] = onboarding_tutorial


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())

s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])
os.environ["DEBUSSY"]="LOL"
slack_token = os.environ["SLACK_BOT_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
rtm_client.start()
