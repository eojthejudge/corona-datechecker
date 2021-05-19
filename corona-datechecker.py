import bs4
import requests
import re
import hashlib
import credentials
from nio import AsyncClient
import asyncio


def get_availability_string():
    url="https://www.gef.be.ch/gef/de/index/Corona/Corona/corona_impfung_bern.html"

    page=requests.get(url).content

    soup = bs4.BeautifulSoup(page, 'lxml')


    # find elements that contain the data we want
    found = soup.find_all("h3", string=re.compile("Sind Termine verfügbar"))

    result = ''
    for x in found:
        result = result + str(x.find_next_sibling('p'))
    return result


async def send_message(message, client):
    await client.login(credentials.login['password'])
    await client.room_send(
        room_id="!WpWbonOZKBOYVPWXkQ:matrix.fortress.ch",
        message_type="m.room.message",
        content = {
            "msgtype": "m.text",
            "body": message
        }
    )
    await client.logout()

async def main():
    result = get_availability_string()
    initial_string = hashlib.sha224(result.encode()).hexdigest()
    client = AsyncClient("https://matrix.fortress.ch", "@coronabot:matrix.fortress.ch")
    print('Initial text: ' + result)
    await send_message('Initial text: ' + result, client)
    while True:
        await asyncio.sleep(600)
        result = get_availability_string()
        if initial_string != hashlib.sha224(result.encode()).hexdigest():
            print('Availability has changed: ' + result)
            await send_message('Availability has changed: ' + result, client)
            initial_string = hashlib.sha224(result.encode()).hexdigest()

loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(main())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()




