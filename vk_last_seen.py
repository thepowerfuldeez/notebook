"""Spy at defined users every 5 min and append dataframe file with last_seen time and platform"""

import vk_api
import pandas as pd
import itertools
import time
import os

if __name__ == "__main__":
    vk_session = vk_api.VkApi()
    vk = vk_session.get_api()

    if not os.path.exists("vk_last_seen.csv"):
        df = pd.DataFrame(columns=['first_name', 'last_name', 'id', 'time', 'platform'])
    else:
        df = pd.read_csv("vk_last_seen.csv")
    user_ids = vk.friends.get(user_id=134070307)['items'] + [32178649]

    x = df.index.max()
    if str(x) == 'nan':
        x = 0
    c = itertools.count(x)

    while 1:
        data = vk.users.get(user_ids=",".join(map(str, user_ids)), fields='last_seen')
        for item in data:
            d = {**item, **item['last_seen']}
            _ = d.pop("last_seen")
            _ = d.pop("hidden", None)
            i = next(c)
            for k in d:
                df.loc[i, k] = d[k]
        time.sleep(300)
