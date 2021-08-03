from requests import post

from board.api.base import BaseWrapper

API_IGDB_URL = "https://api.igdb.com/v4/"


class IgdbWrapper(BaseWrapper):
    def __init__(self, client_id, auth_token):
        super().__init__(API_IGDB_URL)
        self._auth_token = auth_token
        self._client_id = client_id
        self._requests_method = post

    def get_game_by_id(self, game_id):
        query = {
            "fields": "id, cover.image_id, name, "
            "summary, screenshots.image_id, "
            "genres.name, release_dates, "
            "platforms.name, "
            "aggregated_rating, aggregated_rating_count, "
            "rating, rating_count, slug ",
            "filter[id][eq]": game_id,
        }
        response = self._post("games", query)
        return response[0] if response else None

    def get_games(self, platforms, genres, rating, limit, offset):
        query = {
            "filter[screenshots][not_eq]": "null",
            "filter[genres][not_eq]": "null",
        }
        if platforms:
            query["filter[platforms][eq]"] = self._build_filter_string(platforms)
        if genres:
            query["filter[genres][eq]"] = self._build_filter_string(genres)
        if rating:
            query['filter[rating][gte]'] = self._build_filter_string(rating)
        if limit:
            query['limit'] = self._build_filter_string(limit)
        if offset:
            query['offset'] = self._build_filter_string(offset)
        return self._post('games', query)

    def get_genres(self, query):
        return self._post("genres", query)

    def get_platforms(self, query):
        return self._post("platforms", query)

    @staticmethod
    def get_img_url(image_id, size="screenshot_big"):
        return "https://images.igdb.com/igdb/image/upload/t_{}/{}.jpg".format(
            size, image_id
        )

    @staticmethod
    def _build_filter_string(item):
        if len(item) > 1:
            string = "(" + ",".join(item) + ")"
        else:
            string = f"{item[0]}"
        return string

    def _post(self, endpoint, query):
        response = self._api_request(endpoint, query, post)
        if response:
            return response
        else:
            return None

    def _compose_request(self, query):
        request_params = {
            "headers": {
                "Authorization": f"Bearer {self._auth_token}",
                "Client-ID": f"{self._client_id}",
            }
        }
        request_params["params"] = query
        return request_params
