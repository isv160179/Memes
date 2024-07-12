from datetime import datetime

from miniopy_async import Minio


class MinioHandler:
    def __init__(
        self,
        minio_endpoint: str,
        access_key: str,
        secret_key: str,
        bucket: str,
        secure: bool = False
    ):
        self.client = Minio(
            endpoint=minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket = bucket

    async def upload_file(
        self,
        file
    ):
        datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        object_name = f'{datetime_prefix}_{file.filename}'
        resp = await self.client.put_object(
            self.bucket,
            object_name,
            file.file,
            length=-1,
            part_size=10 * 1024 * 1024
        )
        return resp.object_name

    async def delete(self, name: str):
        return await self.client.remove_object(self.bucket, name)

    async def get(self, name: str, path: str):
        f_name = path + name
        return await self.client.fget_object(self.bucket, name, f_name)
