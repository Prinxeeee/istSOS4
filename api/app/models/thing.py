# Copyright 2025 SUPSI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0 
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.sqlalchemy_db import get_db
from app.models.thing import Thing

router = APIRouter()


@router.get("/Things", response_model=None)
async def get_things(
    request: Request,
    db: AsyncSession = Depends(get_db),
    count_param: bool = Query(False, alias="$count"),
):
    """
    Get Things collection or count if $count=true
    """

    # Return count in OData-compliant format
    if count_param:
        result = await db.execute(select(func.count(Thing.id)))
        return {"@iot.count": result.scalar()}

    # Fetch Things
    result = await db.execute(select(Thing))
    things = result.scalars().all()

    return things