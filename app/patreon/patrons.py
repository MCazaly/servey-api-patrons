from os import environ
import requests

ROOT = "https://www.patreon.com/api/oauth2/api"
PATRONS = ROOT + "/campaigns/{0}/pledges?fields%5Bpledge%5D=total_historical_amount_cents,is_paused"


def fetch_patrons(campaign: str = None, token: str = None):
    if not campaign:
        campaign = _get_env("PATREON_CAMPAIGN")
    if not token:
        token = _get_env("PATREON_TOKEN")

    headers = {
        "User-Agent": "patron-exporter/1.0.0",
        "From": "https://github.com/Fakas",
        "Authorization": f"Bearer {token}"
    }
    url = PATRONS.format(campaign)

    patrons = []
    while True:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        page = response.json()
        for item in page["data"]:
            if item["type"] == "pledge":
                paused = item["attributes"]["is_paused"]
                lifetime_amount = item["attributes"]["total_historical_amount_cents"] / 100
                user_id = item["relationships"]["patron"]["data"]["id"]
                reward_id = item["relationships"]["reward"]["data"]["id"]
                tier = None
                created = None
                name = None

                for included in page["included"]:
                    if included["id"] == user_id:
                        created = included["attributes"]["created"]
                        name = included["attributes"]["full_name"]
                        continue
                    if included["id"] == reward_id:
                        tier = included["attributes"]["title"]
                    if tier and name:
                        break  # Break early if all information is obtained

                patron = {
                    "paused": paused,
                    "lifetime_amount": lifetime_amount,
                    "user_id": user_id,
                    "reward_id": reward_id,
                    "tier": tier,
                    "created": created,
                    "name": name
                }
                patrons.append(patron)
            else:
                continue
        if "next" in page["links"].keys():
            url = page["links"]["next"]
        else:
            break

    return patrons


def _get_env(key):
    try:
        return environ[key]
    except KeyError:
        raise EnvironmentError(f"Environment variable \"{key}\" is not set!") from None
