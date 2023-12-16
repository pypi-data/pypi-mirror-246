import asyncio
from aioimaplib import aioimaplib
import imap_tools


async def check_mailbox():
    imap_client = aioimaplib.IMAP4_SSL(host="imap.gmail.com", port=993)
    await imap_client.wait_hello_from_server()

    print(await imap_client.login("tigran.saluev@gmail.com", "qris tqgo rzpg mhgf"))

    res, data = await imap_client.select("INBOX")
    print(res, data)

    res, msg = await imap_client.fetch("0", "(RFC822)")
    print(res, msg)

    # TODO https://github.com/ikvk/imap_tools — will need to make async

    # TODO https://www.atmail.com/blog/imap-commands/
    # openssl s_client -host imap.gmail.com -port 993 -crlf

    await imap_client.logout()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_mailbox())
