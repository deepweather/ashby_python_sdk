"""Files API resource."""

from __future__ import annotations

import requests

from .base import BaseResource
from ..exceptions import AshbyNotFoundError


class FilesResource(BaseResource):
    """API resource for files."""

    def get_url(self, file_handle: str) -> str:
        """
        Get the download URL for a file.

        Args:
            file_handle: The file handle string

        Returns:
            Signed URL for downloading the file
        """
        response = self._request("file.info", {"fileHandle": file_handle})
        return response.get("results", {}).get("url", "")

    def download(self, file_handle: str) -> tuple[bytes, str]:
        """
        Download a file by its handle.

        Args:
            file_handle: The file handle string

        Returns:
            Tuple of (file content bytes, filename)
        """
        url = self.get_url(file_handle)
        if not url:
            raise AshbyNotFoundError("Could not get URL for file handle")

        response = requests.get(url)
        response.raise_for_status()

        # Try to get filename from content-disposition header
        content_disp = response.headers.get("content-disposition", "")
        filename = "downloaded_file"
        if "filename=" in content_disp:
            filename = content_disp.split("filename=")[-1].strip('"')

        return response.content, filename
