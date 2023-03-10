import requests as r
import threading
import time
from sys import stdout


def conquistar(xuid, auth, ide, scid):
    payload = {
        "titles": [{"expiration": 600, "id": ide, "state": "active", "sandbox": "RETAIL"}]
    }

    payload2 = {
        "action": "progressUpdate", "serviceConfigId": scid, "titleId": ide,
        "userId": xuid, "achievements": [{"id": 1, "percentComplete": 100}, {"id": 2, "percentComplete": 100},
                                         {"id": 3, "percentComplete": 100}, {"id": 4, "percentComplete": 100},
                                         {"id": 5, "percentComplete": 100}, {"id": 6, "percentComplete": 100},
                                         {"id": 7, "percentComplete": 100}, {"id": 8, "percentComplete": 100}]}

    headers1 = {
        'Accept-Encoding': 'gzip, deflate',
        'x-xbl-contract-version': '3',
        'Authorization': auth,
        'Cache-Control': 'no-cache'
    }

    headers2 = {
        'Accept-Encoding': 'gzip, deflate',
        'x-xbl-contract-version': '2',
        'Cache-Control': 'no-cache',
        'User-Agent': 'XboxServicesAPI/2021.04.20210610.3 c',
        'accept': 'application/json',
        'accept-language': 'en-GB',
        'Content-Type': 'text/plain; charset=utf-8',
        'Authorization': auth,
        'Host': 'achievements.xboxlive.com',
        'Connection': None,
    }

    response = r.post(f"https://presence-heartbeat.xboxlive.com/users/xuid({xuid})/devices/current", json=payload,
                      headers=headers1, verify=False)
    if response.status_code != 200:
        p = 1
        while response.status_code != 200:
            stdout.write("\r" + "Um Erro foi Encontrado, Esperando " + str(p) + " segundos e tentando executar novamente")
            stdout.flush()
            time.sleep(p)
            response = r.post(f"https://presence-heartbeat.xboxlive.com/users/xuid({xuid})/devices/current",
                              json=payload,
                              headers=headers1, verify=False)
            p = p+1



    responsi = r.post(f"https://achievements.xboxlive.com/users/xuid(" + xuid + ")/achievements/" + scid + "/update?",
                      json=payload2, headers=headers2, verify=False)
    if responsi.status_code == 200 or responsi.status_code == 304:
        pass
    else:
        print(f"Algo deu errado, {responsi.status_code} ???")


def conquista(xuid, auth):
    ids = [2013672301, 1967883584, 1884090207]
    scid = ["00000000-0000-0000-0000-00007806336d", "00000000-0000-0000-0000-0000754b8540", "00000000-0000-0000-0000-0000704cef5f"]
    threads = []
    for i, s in zip(ids, scid):
        t = threading.Thread(target=conquistar, args=(xuid, auth, i, s))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == '__main__':
    conquista()
