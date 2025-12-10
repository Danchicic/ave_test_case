from fastapi import HTTPException, status, APIRouter
from fastapi.params import Depends
from redis.asyncio import Redis

from application.redis_service import get_redis, get_phone_key
from application.schemas import PhoneAddressSchema
from application.response_schemas import PhoneAddressResponse

router = APIRouter(prefix='/api/phones')


@router.get(
    "/{phone}",
    response_model=PhoneAddressSchema,
)
async def get_address(phone: str, redis_client: Redis = Depends(get_redis)):
    """
    Аргументы:
        phone: Номер телефона для поиска
    Returns:
        JSON с телефоном и адресом (HTTP 200)
    Raises:
        HTTPException 404: Если номер телефона не найден в Redis
    """
    try:
        PhoneAddressSchema.check_phone(phone)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(ex))

    key = get_phone_key(phone)

    if not (address := await redis_client.get(key)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись для телефона '{phone}' не найдена"
        )
    # возвращает dict вместо pydantic schema, потому что, если мы возвращаем схему, fastapi сериализует ее дважды
    return PhoneAddressResponse(
        phone=phone,
        address=address
    )


@router.post(
    "/",
    response_model=PhoneAddressSchema,
)
async def create_phone_address(record: PhoneAddressSchema, redis_client: Redis = Depends(get_redis)):
    """
    Returns:
        HTTP 201 - Created

    Raises:
        HTTPException 409: Если номер телефона уже существует в системе
    """

    key = get_phone_key(record.phone)

    if await redis_client.exists(key):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Запись для телефона '{record.phone}' уже существует."
                   f"Используйте PUT для обновления."
        )

    await redis_client.set(key, record.address)

    raise HTTPException(status_code=status.HTTP_201_CREATED)


@router.put(
    "/",
    response_model=PhoneAddressSchema,
)
async def update_address(
        update_data: PhoneAddressSchema,
        redis_client: Redis = Depends(get_redis)
):
    """
    Returns:
        JSON с обновленной записью (HTTP 200)

    Raises:
        HTTPException 404: Если номер телефона не найден в системе
    """
    phone: str = update_data.phone

    key = get_phone_key(phone)

    if not await redis_client.exists(key):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись для телефона '{phone}' не найдена. "
                   f"Используйте POST для создания новой записи."
        )

    await redis_client.set(key, update_data.address)
    address: str = await redis_client.get(key)

    return PhoneAddressResponse(
        phone=phone,
        address=address
    )


@router.delete(
    "/{phone}",
)
async def delete_phone_address(phone: str, redis_client: Redis = Depends(get_redis)) -> None:
    """
    Аргументы:
        phone: Номер телефона для удаления
    Raises:
        HTTPException 404: Если номер телефона не найден в системе
    """

    key = get_phone_key(phone)

    if not await redis_client.exists(key):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Запись для телефона '{phone}' не найдена"
        )

    await redis_client.delete(key)
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
