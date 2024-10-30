import logging
import urllib.parse

import boto3

from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    NoRegionError,
)

from fastapi import UploadFile, HTTPException, status

from src.core.config import settings


logger = logging.getLogger(__name__)


class S3Service:
    """
    Service for AWS S3 related operations.
    """

    def __init__(self) -> None:
        """
        Initialize the AWS S3 service.
        """

        self.session = boto3.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        self.s3_client = self.session.resource("s3")

    async def upload_file(self, file: UploadFile, folder: str) -> str:
        """
        Upload a file to AWS S3.

        Args:
            file (UploadFile): The file to upload.
            folder (str): The folder to upload the file to.

        Returns:
            str: The URL of the uploaded file.
        """

        try:
            file_content = await file.read()
            key = f"{folder}/{file.filename}"

            self.s3_client.Bucket(settings.AWS_S3_BUCKET_NAME).put_object(
                Key=key, Body=file_content
            )

            file_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

            return file_url
        except (NoCredentialsError, PartialCredentialsError) as e:
            self._handle_exception(
                "AWS credentials not found or incomplete.", e
            )
        except NoRegionError as e:
            self._handle_exception(
                "AWS region not found. Please check your configuration.", e
            )
        except Exception as e:
            self._handle_exception("An unexpected error occurred.", e)

    def delete_file(self, file_url: str) -> None:
        """
        Delete a file from AWS S3.

        Args:
            file_url (str): The URL of the file to delete.

        Returns:
            None
        """

        try:
            parsed_url = urllib.parse.urlparse(file_url)
            key = parsed_url.path.lstrip("/")

            self.s3_client.Bucket(settings.AWS_S3_BUCKET_NAME).delete_objects(
                Delete={
                    "Objects": [
                        {"Key": key},
                    ]
                }
            )
        except (NoCredentialsError, PartialCredentialsError) as e:
            self._handle_exception(
                "AWS credentials not found or incomplete.", e
            )
        except NoRegionError as e:
            self._handle_exception(
                "AWS region not found. Please check your configuration.", e
            )
        except Exception as e:
            self._handle_exception("An unexpected error occurred.", e)

    def _handle_exception(self, message: str, exception: Exception) -> None:
        """
        Handle exceptions raised during AWS S3 operations.

        Args:
            message (str): The error message.
            exception (Exception): The exception raised.

        Raises:
            HTTPException: Raised with status code 500 if an error occurs.

        Returns:
            None
        """

        logger.error(f"{message} Error: {str(exception)}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
