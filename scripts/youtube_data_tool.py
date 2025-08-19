from typing import Any

from googleapiclient.discovery import build

YOUTUBE_API_KEY = pyscript.config.get("youtube_api_key")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

if not YOUTUBE_API_KEY:
    raise ValueError("You need to configure your YouTube API key")


@pyscript_executor
def youtube_search(
    query: str,
    results: int = 5,
    search_type: str = "video,channel,playlist",
    page_token: str = "",
) -> dict[str, Any]:
    """
    Performs a search on YouTube.

    Args:
        query: The search query string.
        results: The maximum number of results to return.
        search_type: The type of content to search for.
        page_token: The page token to get other pages that could be retrieved.

    Returns:
        A dictionary containing the search results from the YouTube API.
    """
    youtube = build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY
    )
    search_response = (
        youtube.search()
        .list(
            q=query,
            part="id,snippet",
            maxResults=results,
            type=search_type,
            pageToken=page_token,
        )
        .execute()
    )

    return search_response


@service(supports_response="only")
def youtube_search_tool(query: str, **kwargs) -> dict[str, Any]:
    """
    yaml
    name: YouTube Search Tool
    description: Tool for searching YouTube videos, channels, and playlists
    fields:
      query:
        name: Query
        description: The search query string.
        example: Cuộc đời và sự nghiệp của Hồ Chí Minh
        required: true
        selector:
          text: {}
      search_type:
        name: Search Type
        description: The type of content to search for.
        example: video
        required: true
        selector:
          select:
            options:
              - video
              - channel
              - playlist
            multiple: true
        default:
          - video
      results:
        name: Results
        description: The maximum number of results to return.
        example: 5
        selector:
          number:
            min: 0
            max: 50
        default: 5
      page_token:
        name: Page Token
        description:  The page token to get other pages that could be retrieved.
        selector:
          text: {}
    """
    if not query:
        return {"error": "Missing required argument: query"}
    try:
        results = int(kwargs.get("results", 5))
        search_type = list(kwargs.get("search_type", ["video"]))
        page_token = kwargs.get("page_token", "")
        response = youtube_search(
            query,
            results=results,
            search_type=",".join(search_type),
            page_token=page_token,
        )
        return response
    except Exception as error:
        return {"error": f"An unexpected error occurred during processing: {error}"}
