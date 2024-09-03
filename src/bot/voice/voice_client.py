"""

Yone Discord Bot Server Administrator

Copyright (C) よね/Yone

Licensed under the Apache License 2.0.

"""

from discord.gateway import DiscordVoiceWebSocket
from discord import VoiceClient

class MyVoiceWebSocket(DiscordVoiceWebSocket):
    def __init__(self, socket, loop):
        super().__init__(socket, loop)
        self.record_ready = False


    async def received_message(self, msg):
        await super(MyVoiceWebSocket, self).received_message(msg)
        op = msg["op"]

        if op == self.SESSION_DESCRIPTION:  # op 5
            self.record_ready = True


class MyVoiceClient(VoiceClient):
    def __init__(self, client, channel):
        super().__init__(client, channel)
        self.record_task = None


    async def recv_voice_packet(self):
        if not self.ws.record_ready:
            raise ValueError("Not Record Ready")

        while True:
            recv = await self.loop.sock_recv(self.socket, 2**16)


    async def connect_websocket(self) -> MyVoiceWebSocket:
        ws = await MyVoiceWebSocket.from_client(self)
        self._connected.clear()
        while ws.secret_key is None:
            await ws.poll_event()
        self._connected.set()
        return ws


    def decrypt_xsalsa20_poly1305(self, data: bytes) -> tuple:
        box = nacl.secret.SecretBox(bytes(self.secret_key))
        is_rtcp = 200 <= data[1] < 205
        if is_rtcp:
            header, encrypted = data[:8], data[8:]
            nonce = bytearray(24)
            nonce[:8] = header
        else:
            header, encrypted = data[:12], data[12:]
            nonce = bytearray(24)
            nonce[:12] = header
        return header, box.decrypt(bytes(encrypted), bytes(nonce))


    def decrypt_xsalsa20_poly1305_suffix(self, data: bytes) -> tuple:
        box = nacl.secret.SecretBox(bytes(self.secret_key))
        is_rtcp = 200 <= data[1] < 205
        if is_rtcp:
            header, encrypted, nonce = data[:8], data[8:-24], data[-24:]
        else:
            header, encrypted, nonce = data[:12], data[12:-24], data[-24:]
        return header, box.decrypt(bytes(encrypted), bytes(nonce))


    def decrypt_xsalsa20_poly1305_lite(self, data: bytes) -> tuple:
        box = nacl.secret.SecretBox(bytes(self.secret_key))
        is_rtcp = 200 <= data[1] < 205
        if is_rtcp:
            header, encrypted, _nonce = data[:8], data[8:-4], data[-4:]
        else:
            header, encrypted, _nonce = data[:12], data[12:-4], data[-4:]
        nonce = bytearray(24)
        nonce[:4] = _nonce
        return header, box.decrypt(bytes(encrypted), bytes(nonce))
