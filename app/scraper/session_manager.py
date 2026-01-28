import httpx

class NCLTSession:
    def __init__(self):
        self.client = None

    async def __aenter__(self):
        # persistent cookies & headers
        self.client = httpx.AsyncClient(
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
        )
        return self.client

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()
