import os
import requests
from third_parties import scrape_cache


def scrape_linkedin_profile(profile_url: str):
    """Scrape information from given linkedin profile"""

    scrape_cache.init_db()
    data = scrape_cache.get_cached_profile(profile_url)

    if data == None:
        data = scrape(profile_url)
        scrape_cache.save_to_cache(profile_url, data)

    return remove_unwanted_fields(data)


def scrape(profile_url: str):
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f'Bearer {""}'}
    rsp = requests.get(
        api_endpoint,
        params={"url": profile_url},
        headers=header_dic,
        timeout=10,
    )

    return rsp.json()


def remove_unwanted_fields(data):
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            profile_url="https://www.linkedin.com/in/hubert-liberacki-07183580/"
        )
    )
