# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio

import pytest

from aiogettext import LanguageContext


@pytest.mark.asyncio
async def test_set_language():
    async def f1():
        with LanguageContext('nl'):
            await asyncio.sleep(1)
            assert LanguageContext.get() == 'nl'

    async def f2():
        await asyncio.sleep(0.1)
        with LanguageContext('en'):
            assert LanguageContext.get() == 'en'

    await asyncio.gather(f1(), f2())
    assert LanguageContext.get() == None