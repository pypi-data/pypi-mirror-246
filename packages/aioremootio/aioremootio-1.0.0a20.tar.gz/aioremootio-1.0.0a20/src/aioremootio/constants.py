# Copyright 2021 Gergö Gabor Ilyes-Veisz
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from voluptuous import Schema, Required, All, Coerce, Match, Upper, REMOVE_EXTRA, Optional
import re

CONNECTION_OPTION_KEY_HOST = "host"
CONNECTION_OPTION_KEY_API_SECRET_KEY = "api_secret_key"
CONNECTION_OPTION_KEY_API_AUTH_KEY = "api_auth_key"
CONNECTION_OPTION_KEY_CONNECT_AUTOMATICALLY = "connect_automatically"
CONNECTION_OPTION_REGEX_HOST = re.compile(
    r"^(" +
    r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" +
    r"|" +
    r"(([a-zA-Z0-9][a-zA-Z0-9\-]{0,62})(?:\.([a-zA-Z0-9][a-zA-Z0-9\-]{0,62}))*){1,255}" +
    r")$"
)
CONNECTION_OPTION_REGEX_CREDENTIAL = re.compile(r"[0-9A-Z]{64}")
CONNECTION_OPTION_REGEX_API_SECRET_KEY = CONNECTION_OPTION_REGEX_CREDENTIAL
CONNECTION_OPTION_REGEX_API_AUTH_KEY = CONNECTION_OPTION_REGEX_CREDENTIAL
CONNECTION_OPTIONS_VOLUPTUOUS_SCHEMA = Schema(
    {
        Required(CONNECTION_OPTION_KEY_HOST, msg="Host is required"): All(
            Coerce(str),
            Match(CONNECTION_OPTION_REGEX_HOST),
            msg="Host appears to be invalid",
        ),
        Required(CONNECTION_OPTION_KEY_API_SECRET_KEY, msg="API Secret Key is required"): All(
            Coerce(str),
            Upper,
            Match(CONNECTION_OPTION_REGEX_API_SECRET_KEY),
            msg="API Secret Key appears to be invalid",
        ),
        Required(CONNECTION_OPTION_KEY_API_AUTH_KEY, msg="API Auth Key is required"): All(
            Coerce(str),
            Upper,
            Match(CONNECTION_OPTION_REGEX_API_AUTH_KEY),
            msg="API Auth Key appears to be invalid",
        ),
        Optional(CONNECTION_OPTION_KEY_CONNECT_AUTOMATICALLY): All(
            Coerce(bool),
            msg="Flag to control whether the client should establish a connection to the device during its "
                "initialization appears to be invalid"
        )
    },
    extra=REMOVE_EXTRA)
CONNECTION_OPTION_DEFAULT_VALUE_CONNECT_AUTOMATICALLY = True
MESSAGE_HANDLER_HEARTBEAT = 5
PING_SENDER_HEARTBEAT = 60
WAITING_DELAY = 1
WAITING_FOR_SAID_HELLO_DELAY = WAITING_DELAY
WAITING_FOR_DEVICE_ANSWERED_TO_HELLO_DELAY = WAITING_DELAY
LOCK_DELAY = 0.5
LIFECYCLE_LOCK_DELAY = LOCK_DELAY
CONNECTING_LOCK_DELAY = LOCK_DELAY
DISCONNECTING_LOCK_DELAY = LOCK_DELAY
AUTHENTICATING_LOCK_DELAY = LOCK_DELAY
TERMINATING_LOCK_DELAY = LOCK_DELAY
INITIALIZING_LOCK_DELAY = LOCK_DELAY
SAYING_HELLO_LOCK_DELAY = LOCK_DELAY
UPDATING_LAST_ACTION_ID_LOCK_DELAY = LOCK_DELAY
INVOKING_STATE_CHANGE_LISTENERS_LOCK_DELAY = LOCK_DELAY
ADDING_STATE_CHANGE_LISTENER_LOCK_DELAY = LOCK_DELAY
INVOKING_EVENT_LISTENERS_LOCK_DELAY = LOCK_DELAY
ADDING_EVENT_LISTENERS_LOCK_DELAY = LOCK_DELAY
ENCODING = "latin-1"
TASK_NAME_MESSAGE_RECEIVER_AND_HANDLER = "MessageReceiverAndHandler"
TASK_NAME_PING_SENDER = "PingSender"
TASK_NAME_CONNECTOR = "Connector"
TASK_NAME_DISCONNECTOR = "Disconnector"
TASK_STOPPED_DELAY = 5
TASK_STARTED_DELAY = 0.5
TASK_STOPPED_TIMEOUT = 10