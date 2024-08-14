import logging
import os

from slack_bolt import BoltResponse
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.oauth.async_oauth_settings import AsyncOAuthSettings
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
from slack_sdk.oauth.installation_store import FileInstallationStore
from slack_sdk.oauth.state_store import FileOAuthStateStore

from daily_arxiv import get_daily_arxiv

logger = logging.getLogger(__name__)

def get_cookie_value(cookie_key, headers):
    if 'cookie' in headers:
        cookies = headers['cookie'][0].split('; ')
        for cookie in cookies:
            key, value = cookie.split('=')
            if key == cookie_key:
                return value
    return None

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
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    installation_store=FileInstallationStore(),
    oauth_settings=AsyncOAuthSettings(
        client_id=os.environ.get("SLACK_CLIENT_ID"),
        client_secret=os.environ.get("SLACK_CLIENT_SECRET"),
        scopes=[
            "chat:write",
        ],
        user_scopes=[],
        redirect_uri=None,
        install_path="/slack/install",
        redirect_uri_path="/slack/oauth_redirect",
        state_store=FileOAuthStateStore(expiration_seconds=600),
        callback_options=CallbackOptions(success=success, failure=failure),
        install_page_rendering_enabled=False
    ),
)
app_handler = AsyncSlackRequestHandler(app)


@app.event("app_mention")
async def handle_app_mentions(event, client, say, logger):
    channel_id = ...
    message_ts = ...
    answer = get_daily_arxiv()
    
    await client.chat_postMessage(
        channel=channel_id, 
        thread_ts=message_ts, 
        text=answer
    )
