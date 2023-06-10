import time
import traceback
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def lambda_handler(event, context):
    try:
        token = event['Token']  # Slack API Token
        channels = event['Channels']  # Channel IDs
        term = event.get('Term', 60 * 60 * 24 * 30)  # Delete messages older than 30 days
        sleep = event.get('Sleep', 5)  # 5 seconds
        botonly = event.get('BotOnly', False)  # Delete only bot messages

        client = WebClient(token=token)
        latest = int(time.time() - term)

        for channel in channels:
            print('Channel:', channel)
            cursor = None
            while True:
                try:
                    response = client.conversations_history(
                        channel=channel,
                        latest=latest,
                        cursor=cursor
                    )
                except SlackApiError as e:
                    print(e.response['error'])
                    return {
                        'statusCode': 500,
                        'message': e.response['error']
                    }

                if 'messages' in response:
                    for message in response['messages']:
                        if botonly == 'True' and 'bot_id' not in message.keys():
                            continue
                        else:
                            try:
                                client.chat_delete(
                                    channel=channel, ts=message['ts']
                                )
                            except SlackApiError as e:
                                if e == 'ratelimited':
                                    time.sleep(sleep)
                                    try:
                                        client.chat_delete(
                                            channel=channel, ts=message['ts']
                                        )
                                    except SlackApiError as e:
                                        print(e.response['error'])
                                else:
                                    print(e.response['error'])

                if 'has_more' not in response or response['has_more'] is not True:
                    break

                if (
                        'response_metadata' in response
                        and 'next_cursor' in response['response_metadata']
                ):
                    cursor = response['response_metadata']['next_cursor']
                else:
                    break
                time.sleep(sleep)

        return {
            'statusCode': 200,
            'message': 'Finished Slack Message Delete.'
        }
    except:
        print(traceback.format_exc())
        return {
            'statusCode': 500,
            'message': traceback.format_exc()
        }
