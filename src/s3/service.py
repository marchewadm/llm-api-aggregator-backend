import os
import uuid
import boto3
import logging
import urllib.parse

from pathlib import Path

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
        self.s3_resource = self.session.resource("s3")

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

            unique_filename = (
                f"{uuid.uuid4()}{os.path.splitext(file.filename)[1]}"
            )
            key = f"{folder}/{unique_filename}"

            self.s3_resource.Bucket(settings.AWS_S3_BUCKET_NAME).put_object(
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

    def download_file_to_local(self, filename: str) -> str:
        """
        Download a file from AWS S3.

        Args:
            filename (str): The name of the file to download.

        Returns:
            str: The path to the downloaded file.
        """

        try:
            download_path = (
                Path(settings.AWS_S3_DOWNLOAD_PATH) / Path(filename).name
            )
            download_path.parent.mkdir(parents=True, exist_ok=True)

            self.s3_resource.Bucket(settings.AWS_S3_BUCKET_NAME).download_file(
                filename, str(download_path)
            )

            return str(download_path)
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
            key = self.extract_s3_key_from_url(file_url)

            self.s3_resource.Bucket(settings.AWS_S3_BUCKET_NAME).delete_objects(
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

    def delete_local_file(self, local_path: str) -> None:
        """
        Delete a local file from the specified download path.

        Args:
            local_path (str): The path to the local file to delete.
        """

        try:
            file_path = Path(local_path)
            file_path.unlink(missing_ok=True)
        except Exception as e:
            self._handle_exception("Failed to delete local file {filename}.", e)

    @staticmethod
    def extract_s3_key_from_url(file_url: str) -> str:
        """
        Extracts the S3 key from a URL.

        Args:
            file_url (str): The URL to extract the key from.

        Returns:
            str: The extracted S3 key.
        """

        parsed_url = urllib.parse.urlparse(file_url)
        return parsed_url.path.lstrip("/")

    def get_clean_filename_from_url(self, file_url: str) -> str:
        """
        Extracts the filename without extension from a URL.

        Args:
            file_url (str): The URL to extract the filename from.

        Returns:
            str: The filename without the extension.
        """

        filename = os.path.basename(self.extract_s3_key_from_url(file_url))
        return Path(filename).stem

    @staticmethod
    def _handle_exception(message: str, exception: Exception) -> None:
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
