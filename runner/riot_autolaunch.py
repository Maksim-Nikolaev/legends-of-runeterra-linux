import base64
import glob
import http.client
import json
import ntpath
import os
import ssl
import threading
import time

READY_PHASE = "WaitForLaunch"
POLL_SECONDS = 1.0
GIVE_UP_SECONDS = 600.0
CLIENT_GONE_SECONDS = 60.0
DISABLE_ENV = "PROTON_RIOT_AUTOLAUNCH"


class ClientApi:
    def __init__(self, port, password):
        self.port = port
        self.authorization = "Basic " + base64.b64encode(f"riot:{password}".encode()).decode()
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

    def request(self, method, path):
        connection = http.client.HTTPSConnection("127.0.0.1", self.port, timeout=5, context=self.context)

        try:
            connection.request(method, path, headers={"Authorization": self.authorization})
            response = connection.getresponse()
            body = response.read()
        finally:
            connection.close()

        if response.status != 200:
            return None

        return json.loads(body) if body else None


def _argument(argv, name):
    prefix = f"--{name}="

    for argument in argv:
        if argument.startswith(prefix):
            return argument[len(prefix):]

    return None


def _is_riot_client(executable):
    return ntpath.basename(executable.replace("/", "\\")).lower() == "riotclientservices.exe"


def _read_lockfile(prefix_dir, not_before):
    pattern = os.path.join(prefix_dir, "drive_c/users/*/AppData/Local/Riot Games/Riot Client/Config/lockfile")

    for path in glob.glob(pattern):
        try:
            if os.path.getmtime(path) < not_before:
                continue

            with open(path, encoding="utf-8") as lockfile:
                fields = lockfile.read().strip().split(":")
        except OSError:
            continue

        if len(fields) == 5 and fields[4] == "https":
            return fields[2], fields[3]

    return None


def _game_running(api, product):
    sessions = api.request("GET", "/product-session/v1/external-sessions") or {}

    return any(session.get("productId") == product for session in sessions.values())


def _try_launch(api, product, patchline):
    if _game_running(api, product):
        return True

    if api.request("GET", "/riot-client-lifecycle/v1/product-context-phase") != READY_PHASE:
        return False

    context = api.request("GET", "/riot-client-lifecycle/v1/product-context") or {}

    if context.get("productId") != product or context.get("willAutoLaunch"):
        return False

    launch_path = f"/product-launcher/v1/products/{product}/patchlines/{patchline}"

    if api.request("GET", launch_path + "/eligibility") is not True:
        return False

    return api.request("POST", launch_path) is not None


def _watch(prefix_dir, product, patchline, log):
    started = time.time()
    deadline = time.monotonic() + GIVE_UP_SECONDS
    last_seen = time.monotonic()

    while time.monotonic() < deadline:
        time.sleep(POLL_SECONDS)

        lock = _read_lockfile(prefix_dir, started - 1)

        if lock is None:
            if time.monotonic() - last_seen > CLIENT_GONE_SECONDS:
                log("Riot autolaunch: the Riot Client is gone, stopping")
                return

            continue

        last_seen = time.monotonic()

        try:
            if _try_launch(ClientApi(*lock), product, patchline):
                log(f"Riot autolaunch: {product}.{patchline} started")
                return
        except (OSError, http.client.HTTPException, ValueError):
            continue

    log(f"Riot autolaunch: {product}.{patchline} not ready after {GIVE_UP_SECONDS:.0f} s, stopping")


def start(prefix_dir, argv, log):
    if os.environ.get(DISABLE_ENV) == "0" or not argv or not _is_riot_client(argv[0]):
        return

    product = _argument(argv, "launch-product")
    patchline = _argument(argv, "launch-patchline") or "live"

    if not product:
        return

    log(f"Riot autolaunch: waiting for the Riot Client to start {product}.{patchline}")

    threading.Thread(target=_watch, args=(prefix_dir, product, patchline, log), name="riot-autolaunch").start()
