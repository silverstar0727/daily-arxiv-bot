import logging
import os

from slack_bolt import BoltResponse
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from src.daily_arxiv import get_daily_arxiv
from src.configurations import Settings

config = Settings()

logger = logging.getLogger(__name__)

response_body = '''<html>
<head>
</head>
<body>Redirecting...</body>
</html>
'''
# Callback to run on successful installation
async def success(args: SuccessArgs) -> BoltResponse:
    return BoltResponse(status=200, body=response_body, headers={"Content-Type": "text/html; charset=utf-8"})


# Callback to run on failed installation
def failure(args: FailureArgs) -> BoltResponse:
    return args.default.failure(args)
    # return BoltResponse(status=args.suggested_status_code, body=args.reason)


app = AsyncApp(
    signing_secret=config.slack_signing_secret,
    installation_store=FileInstallationStore(),
    oauth_settings=AsyncOAuthSettings(
        client_id=config.slack_client_id,
        client_secret=config.slack_client_secret,
        scopes=[
            "chat:write",
            "app_mentions:read",


            "app_mentions:read",
            "channels:history",
            "channels:join",
            "channels:read",
            "chat:write",
            "im:history",
            "im:read",
            "im:write",
            "users:read"
        ],
        user_scopes=[],
        redirect_uri=None,
        install_path="/slack/install",
        redirect_uri_path="/slack/oauth_redirect",
        state_store=FileOAuthStateStore(expiration_seconds=600),
        callback_options=CallbackOptions(success=success, failure=failure),
        install_page_rendering_enabled=True
    ),
)
app_handler = AsyncSlackRequestHandler(app)


@app.event("app_mention")
async def handle_app_mentions(event, client, say, logger):
    print(1)
    channel_id = ...
    message_ts = ...
    answer = get_daily_arxiv()
    
    await client.chat_postMessage(
        channel=channel_id, 
        thread_ts=message_ts, 
        text=answer
    )


# Example event listener for app mentions
@app.event("app_mention")
async def handle_app_mention(event, say):
    user = event['user']
    await say(f"Hello, <@{user}>! How can I assist you today?")