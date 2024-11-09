
def parse_sources_list(doc_list: list[any]) -> list[dict[str, str]]:
    """
    Parse a list of Document objects with metadata and page_content.

    Args:
    - doc_list (list[any]): The list of Document objects.

    Returns:
    - list[dict[str, str]]: A list of dictionaries where each dict contains 'source' and 'content'.
    """

    parsed_docs = []

    for doc in doc_list:
        # Extract link and title from metadata
        link = doc.metadata.get('link')
        title = doc.metadata.get('title')

        parsed_docs.append((link, title))

    return parsed_docs


def format_parsed_sources(parsed_docs: list[tuple[str, str]]) -> str:
    """
    Formats the parsed documents for display, similar to the example provided.

    Args:
    - parsed_docs (list[dict[str, str]]): The list of parsed documents.

    Returns:
    - str: A formatted string.
    """

    formatted_sources: list = []

    unique_outputs: set = set(parsed_docs)
    for i, source in enumerate(unique_outputs, start=1):
        url, title = source
        formatted_doc = f"{i}. *[{title}]({url})*\n"
        formatted_sources.append(formatted_doc)

    return "\n".join(formatted_sources)
