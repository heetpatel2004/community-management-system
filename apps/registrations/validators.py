"""
File upload validators for result documents.
Validates file extension, MIME type, and file size.
"""

import os
import mimetypes

from django.conf import settings
from django.core.exceptions import ValidationError


def validate_document_extension(value):
    """Validate that the uploaded file has an allowed extension."""
    ext = os.path.splitext(value.name)[1].lower()
    allowed = getattr(settings, 'ALLOWED_DOCUMENT_EXTENSIONS', ['.pdf', '.jpg', '.jpeg', '.png'])
    if ext not in allowed:
        raise ValidationError(
            f'File type "{ext}" is not allowed. '
            f'Allowed types: {", ".join(allowed)}'
        )


def validate_document_size(value):
    """Validate that the uploaded file does not exceed the maximum size."""
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE_BYTES', 5 * 1024 * 1024)
    max_mb = max_size / (1024 * 1024)
    if value.size > max_size:
        raise ValidationError(
            f'File size ({value.size / (1024 * 1024):.1f} MB) exceeds '
            f'the maximum allowed size ({max_mb:.0f} MB).'
        )


def validate_document_mime_type(value):
    """Validate the MIME type of the uploaded file (not just the extension)."""
    allowed_mimes = getattr(
        settings, 'ALLOWED_DOCUMENT_MIME_TYPES',
        ['application/pdf', 'image/jpeg', 'image/png']
    )

    # Try to determine MIME type from the file content
    mime_type = None

    # Check using mimetypes module (based on extension)
    mime_type_guess, _ = mimetypes.guess_type(value.name)

    # Read magic bytes for more reliable detection
    value.seek(0)
    header = value.read(16)
    value.seek(0)

    if header[:4] == b'%PDF':
        mime_type = 'application/pdf'
    elif header[:3] == b'\xff\xd8\xff':
        mime_type = 'image/jpeg'
    elif header[:8] == b'\x89PNG\r\n\x1a\n':
        mime_type = 'image/png'
    else:
        mime_type = mime_type_guess

    if mime_type not in allowed_mimes:
        raise ValidationError(
            f'File type is not allowed. '
            f'Please upload a PDF, JPG, or PNG file.'
        )


def validate_result_document(value):
    """Run all document validations."""
    validate_document_extension(value)
    validate_document_size(value)
    validate_document_mime_type(value)
