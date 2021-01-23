from typing import Any

from models.UrlMap import UrlMapUpdateRecord, UrlMap


async def set_urlmap_update(user_id: int, urlmap_id: int):
    result = await UrlMap.get_or_none(id=urlmap_id, deleted=False)
    if not result:
        return
    r = await UrlMapUpdateRecord.create(user_id=result.user_id, urlmap_id=result.pk, title=result.title,
                                        origin_url=result.origin_url)
    await r.save()
    return
