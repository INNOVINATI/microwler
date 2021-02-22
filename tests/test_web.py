# TODO: https://pgjones.gitlab.io/quart/how_to_guides/testing.html
import os
import sys

import pytest

sys.path.append(os.getcwd())

from microwler.web.backend import app



class TestWebservice:

    @pytest.mark.asyncio
    def setup_class(self):
        self.client = app.test_client()

    @pytest.mark.asyncio
    async def test_index(self):
        response = await self.client.get('/')
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_status(self):
        response = await self.client.get('/status')
        assert response.status_code == 200
        data = await response.get_json()
        assert data
        assert len(data['projects']) == 1

    @pytest.mark.asyncio
    async def test_project_status(self):
        response = await self.client.get('/status/quotes')
        assert response.status_code == 200
        data = await response.get_json()
        assert data
        assert data['name'] == 'quotes' and data['start_url'] == 'https://quotes.toscrape.com/'

    @pytest.mark.asyncio
    async def test_crawl(self):
        response = await self.client.get('/crawl/quotes')
        assert response.status_code == 200
        data = await response.get_json()
        assert data
        assert len(data['data']) == 214

    @pytest.mark.asyncio
    async def test_cache(self):
        response = await self.client.get('/data/quotes')
        assert response.status_code == 200
        data = await response.get_json()
        assert data
        assert len(data['data']) == 214
