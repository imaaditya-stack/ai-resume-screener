import re


class TextProcessingUtils:
    """Utility class for text processing operations"""

    @staticmethod
    def process_content(content: str, preserve_chars: str = ".@+\\-,:/ ") -> str:
        """
        Clean and normalize text content

        Args:
            content: Raw text to process
            preserve_chars: Additional characters to preserve (besides alphanumerics)

        Returns:
            Cleaned and normalized text
        """
        if not content:
            return ""

        # Replace multiple newlines with a single space
        content = re.sub(r"\n+", " ", content)

        # Replace multiple spaces with a single space
        content = re.sub(r"\s+", " ", content)

        # Remove any non-alphanumeric characters that aren't in the preserve list
        pattern = f"[^\\w\\s{re.escape(preserve_chars)}]"
        content = re.sub(pattern, " ", content)

        # Final cleanup and normalization
        return content.strip()
