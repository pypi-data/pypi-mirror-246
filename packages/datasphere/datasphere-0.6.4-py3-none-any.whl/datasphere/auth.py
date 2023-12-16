import logging
import os
import subprocess
from typing import List, Optional, Tuple

import grpc

from datasphere.api import env, ServerEnv, iam_endpoint
from datasphere.version import version
from yandex.cloud.iam.v1.iam_token_service_pb2 import CreateIamTokenRequest
from yandex.cloud.iam.v1.iam_token_service_pb2_grpc import IamTokenServiceStub

logger = logging.getLogger(__name__)


def create_iam_token(oauth_token: Optional[str]) -> str:
    if oauth_token:
        return create_iam_token_by_oauth_token(oauth_token)

    # If user does not provide OAuth token, or OAuth token is not applicable (i.e. for YC staff with federations),
    # we consider that `yc` CLI is installed and configured properly (either on prod or preprod installation).
    return create_iam_token_with_yc()


def create_iam_token_by_oauth_token(oauth_token: str) -> str:
    logger.debug('creating iam token using oauth token ...')
    stub = IamTokenServiceStub(grpc.secure_channel(iam_endpoint, grpc.ssl_channel_credentials()))
    req = CreateIamTokenRequest(yandex_passport_oauth_token=oauth_token)
    resp = stub.Create(req)
    return resp.iam_token


def create_iam_token_with_yc() -> str:
    env_token: Optional[str] = os.getenv('YC_TOKEN', None)
    if env_token:
        return env_token
    logger.debug('oauth token is not provided, creating iam token through `yc` ...')
    try:
        # TODO: capture stderr, process return code
        process = subprocess.run(
            ['yc', 'iam', 'create-token', '--no-user-output'],
            stdout=subprocess.PIPE, universal_newlines=True,
        )
    except FileNotFoundError:
        raise RuntimeError('You have not provided OAuth token. You have to install Yandex Cloud CLI '
                           '(https://cloud.yandex.com/docs/cli/) to authenticate automatically.')

    # There may be another output before the token, for example, info about opening the browser.
    # TODO: not sure if token will be last line (update suggestion appears regardless of --no-user-output flag
    return process.stdout.strip().split('\n')[-1]


def get_md(oauth_token: Optional[str]) -> List[Tuple[str, str]]:
    metadata = [("x-client-version", f"datasphere={version}")]
    if env != ServerEnv.DEV:
        iam_token = create_iam_token(oauth_token)
        metadata.append(('authorization', f'Bearer {iam_token}'))
    return metadata
