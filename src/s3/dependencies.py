from typing import Annotated

from fastapi import Depends

from .service import S3Service


S3ServiceDependency = Annotated[S3Service, Depends()]
