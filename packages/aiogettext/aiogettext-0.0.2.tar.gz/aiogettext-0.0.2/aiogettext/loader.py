# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import gettext
import os
from typing import Any

import aiofiles


_translations: Any = gettext._translations # type: ignore


async def translation(
    domain: str,
    localedir: str | None = None,
    languages: list[str] | None = None,
    class_: type[gettext.NullTranslations] | None = None,
    fallback: bool = False
):
    if class_ is None:
        class_ = gettext.GNUTranslations
    mofiles = gettext.find(domain, localedir, languages, all=True)
    if not mofiles:
        if fallback:
            return gettext.NullTranslations()
        from errno import ENOENT
        raise FileNotFoundError(ENOENT,
                                'No translation file found for domain', domain)
    # Avoid opening, reading, and parsing the .mo file after it's been done
    # once.
    result = None
    for mofile in mofiles:
        key = (class_, os.path.abspath(mofile))
        t = _translations.get(key)
        if t is None:
            # :(
            async with aiofiles.open(mofile, 'rb') as fp: # type: ignore
                t = _translations.setdefault(key, class_(fp)) # type: ignore
        # Copy the translation object to allow setting fallbacks and
        # output charset. All other instance data is shared with the
        # cached object.
        # Delay copy import for speeding up gettext import when .mo files
        # are not used.
        import copy
        t = copy.copy(t)
        if result is None:
            result = t
        else:
            result.add_fallback(t)
    return result