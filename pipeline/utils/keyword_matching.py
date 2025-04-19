import re

# [TODO]
# - Add support for fuzzy type matching by defining variations of the keyword


class KeywordMatchingUtils:
    """Utility class containing shared keyword matching logic."""

    @staticmethod
    def build_keyword_matching_pattern(keyword: str) -> str:
        """Generate the appropriate regex pattern based on keyword type"""
        # Strip version number from keyword for matching, e.g. HTML5 matches HTML, CSS3 matches CSS
        keyword_base = re.sub(r"\d+$", "", keyword)

        # (HACKY WAY TO HANDLE TECHNOLOGY NAMES)
        if keyword.endswith("js") or keyword.lower().endswith(".js"):
            return rf"\b{re.escape(keyword_base.replace('.js', '').replace('js', ''))}(?:\.?js|\s+js)?\b"

        # Default case - match base keyword with optional version number
        return rf"\b{re.escape(keyword_base)}\d*\b"

    @staticmethod
    def regex_based_keyword_matcher(
        keyword: str,
        text: str,
        case_sensitive: bool = False,
        use_partial_matching: bool = True,
    ) -> tuple[bool, str | None]:
        """
        Check if a keyword exists in the text using the configured matching method.
        Matches base keywords ignoring version numbers (e.g. HTML5 matches HTML).

        Args:
            keyword: The keyword to search for
            text: The text to search in
            case_sensitive: Whether to use case-sensitive matching
            use_partial_matching: Whether to use regex pattern matching or exact match

        Returns:
            tuple: (bool, str | None) - (True if keyword found, matched text if found else None)
        """
        if not case_sensitive:
            keyword = keyword.lower()
            text = text.lower()

        if use_partial_matching:
            # Match the base keyword followed by optional version number
            pattern = KeywordMatchingUtils.build_keyword_matching_pattern(keyword)
            match = re.search(pattern, text)
            if match:
                return True, match.group(0)
            return False, None
        else:
            # print("Exact matching:", keyword)
            # For exact matching
            if keyword in text:
                return True, keyword
            return False, None
