"""Support for JPEG image decoding"""

from __future__ import annotations

import displayio
from circuitpython_typing import ReadableBuffer

class JpegDecoder:
    """A JPEG decoder

    A JPEG decoder allocates a few thousand bytes of memory. To reduce memory fragmentation,
    create a single JpegDecoder object and use it anytime a JPEG image needs to be decoded.
    """

    def __init__(self) -> None: ...
    def decode(
        self, data: ReadableBuffer, bitmap: displayio.Bitmap | None = None, scale=0
    ) -> tuple[int, int]:
        """Decode JPEG data

        If ``bitmap`` is None, only the header is decoded.
        Otherwise, the bitmap must be large enough to contain the decoded image.
        The pixel data is stored in the `displayio.Colorspace.RGB565_SWAPPED` colorspace.

        The image is optionally downscaled by a factor of ``2**scale``.
        Scaling by a factor of 8 (scale=3) is particularly efficient in terms of decoding time.

        :param ReadableBuffer data: Data in JPEG format
        :param Bitmap bitmap: Optional output buffer
        :param int scale: Scale factor from 0 to 3.
        :returns: The size of the (possibly scaled) image as ``width, height``
        """
