from collections.abc import Iterator
from typing import Any, Optional

from oryks_google_oauth import GoogleOAuth, YouTubeScopes
from pydantic import BaseModel

from .models import Video
from .resources import YouTubeSearch
from .schemas import VideoReportAbuse, YouTubeRequest, YouTubeResponse


class YouTube(BaseModel):
    """Provides methods for interacting with the YouTube API.

    This class acts as an interface to the YouTube API, providing methods for interacting with
    the YouTube V3 API.

    Attributes
    ----------
    client_secret_file: str
        The path to the json file containing your authentication information.
    """

    client_secret_file: Optional[str] = None
    authenticated: Optional[bool] = False
    youtube_client: Optional[Any] = None

    def authenticate(self, client_secret_file: Optional[str] = None) -> None:
        """Authenticate the requests made to youtube.

        Used to generate the credentials that are used when authenticating requests to youtube.

        Parameters
        ----------
        client_secret_file: str
            The path to clients secret json file from Google

        Raises
        ------
        ValueError:
            When the client secrets file is not provided
        FileNotFoundError:
            When the secrets file path is not found
        """
        if client_secret_file:
            self.client_secret_file = client_secret_file
        if not self.client_secret_file:
            raise ValueError('The client secret file must be provided.')
        api_service_name: str = 'youtube'
        api_version: str = 'v3'
        credentials_dir: str = '.youtube'
        scopes: list[str] = [YouTubeScopes.youtube.value]
        oauth: GoogleOAuth = GoogleOAuth(
            secrets_file=self.client_secret_file,
            scopes=scopes,
            api_service_name=api_service_name,
            api_version=api_version,
            credentials_dir=credentials_dir,
        )
        self.youtube_client = oauth.authenticate_google_server()

    def search(self, search_schema: YouTubeRequest) -> YouTubeResponse:
        """Used to search through youtube for videos, playlists and channels.

        Parameters
        ----------
        search_schema: YouTubeRequest
            An instance of YouTubeRequest that contains all the details needed to search.
        Returns
        -------
        YouTubeResponse:
            An instance of YouTubeResponse that has al the search results.
        """
        search: YouTubeSearch = YouTubeSearch(youtube_client=self.youtube_client)
        search_results: YouTubeResponse = search.search(search_schema)
        return search_results

    def get_search_iterator(self, search_schema: YouTubeRequest) -> Iterator:
        """Return an iterator that can be used to iterate over search results.

        Parameters
        ----------
        search_schema: YouTubeRequest
            An instance of YouTubeRequest that contains all the details needed to search.
        Returns
        -------
        Iterator:
            An iterator that can be used to iterate over the search results.
        """
        pass

    def find_channel_by_name(self, display_name: str) -> YouTubeResponse:
        """Find a channel's details when given the channel title.

        Parameters
        ----------
        display_name: str
            The name of the youtube channel.
        Returns
        -------
        YouTubeResponse:
            A youtube response consisting of channels whose names match the provided names
        """
        pass

    def get_video_ratings(self, video_ids: list[str]) -> list[str]:
        """Find out whether or not you liked the videos whose ids are provided.

        You provide it with a list of video ids and for each video it will tell you whether
        or not you have liked that video.

        Parameters
        ----------
        video_ids: list[str]:
            A list of strings of video ids
        Returns
        -------
        list[str]:
            A list of strings showing whether or not you liked a given video.
        """
        pass

    def find_video_by_id(self, video_id: str) -> Video:
        """Find a single video by providing the video's id.

        Parameters
        ----------
        video_id: str
            The video's id
        Returns
        -------
        Video:
            A Video instance
        """
        pass

    def find_videos(self, video_ids: list[str]) -> list[Video]:
        """Find a many videos by providing a list of video ids.

        Parameters
        ----------
        video_ids: list[str]
            A list of video ids
        Returns
        -------
        list[Video]:
            A list of Video instances
        """
        pass

    def find_most_popular_video_by_region(
        self, region_code: str = 'US', category_id: str = ''
    ) -> list[Video]:
        """Get the most popular videos in a given region and category.

        Parameters
        ----------
        region_code: str
            A string representing the region code.
        category_id: str
            The category to find. This is a string number i.e '22'
        Returns
        -------
        list[Video]:
            A list of the most popular videos
        """
        pass

    def report_video_abuse(self, abuse_report: VideoReportAbuse) -> None:
        """Report a video that you deem as harmful or infringing on copyrights.

        Parameters
        ----------
        abuse_report: VideoReportAbuse
            An instance of VideoReportAbuse with all the details needed to report.
        """
        pass
