from utils.user_data import (prepare_rating, 
                            prepare_user_profile, 
                            prepare_weather)
from utils.weather_get_api import GetWeather

class TestPrepareUserProfile:
    def test_prepare_user_profile_empty_data(self):
        # Test case for preparing user profile with empty data
        user_data = {}
        first_name = 'John'
    
        result = prepare_user_profile(user_data, first_name)
        assert result is None

    def test_prepare_user_profile_unknown_username(self):
        # Test case for preparing user profile with unknown username
        user_data = {'user_id': 1, 'username': 'unknown', 'total': 100, 'wins': 20}
        first_name = 'John'
        
        result = prepare_user_profile(user_data, first_name)
        assert result is not None
        assert '1' in result
        assert 'unknown' in result
        assert '20' in result

    def test_prepare_user_profile_no_wins(self):
        # Test case for preparing user profile with no wins
        user_data = {'user_id': 1, 'username': 'test_user', 'total': 100, 'wins': 0}
        first_name = 'John'
    
        result = prepare_user_profile(user_data, first_name)
        assert result is not None
        assert '1' in result
        assert 'test_user' in result
        assert '0' in result

    def test_prepare_user_profile_negative_balance(self):
        # Test case for preparing user profile with negative balance
        user_data = {'user_id': 1, 'username': 'test_user', 'total': -100, 'wins': 20}
        first_name = 'John'
    
        result = prepare_user_profile(user_data, first_name)
        assert result is not None
        assert '1' in result
        assert 'test_user' in result
        assert '-100' in result

    def test_prepare_user_profile_large_negative_balance(self):
        # Test case for preparing user profile with a large negative balance
        user_data = {'user_id': 1, 'username': 'test_user', 'total': -1000000, 'wins': 20}
        first_name = 'John'

        result = prepare_user_profile(user_data, first_name)
        assert result is not None
        assert '1' in result
        assert 'test_user' in result
        assert '-1000000' in result

    def test_prepare_user_profile_large_wins(self):
        # Test case for preparing user profile with large wins
        user_data = {'user_id': 1, 'username': 'test_user', 'total': 100, 'wins': 10000}
        first_name = 'John'
    
        result = prepare_user_profile(user_data, first_name)
        assert result is not None
        assert '1' in result
        assert 'test_user' in result
        assert '10000' in result

    def test_user_data_none(self):
        # Test case for preparing user profile when user data is None
        user_data = None

        first_name = 'John'
    
        result = prepare_user_profile(user_data, first_name)

        assert result is None


class TestPrepareWeather:
    def test_formatted_string_with_weather_info(self, mocker):
        # Test case for creating a formatted string with weather information
        mocker.patch.object(GetWeather, 'get_data_weather', return_value={
            "name": "Moscow",
            "weather": [{"description": "cloudy"}],
            "main": {"temp": 20},
            "wind": {"speed": 10}
        })

        result = prepare_weather()

        assert isinstance(result, str)
        assert "Moscow" in result
        assert "Cloudy" in result
        assert "20°C" in result
        assert "10 м/с" in result

    def test_message_when_weather_data_not_available(self, mocker):
        # Test case for handling when weather data is not available
        mocker.patch.object(GetWeather, 'get_data_weather', return_value=None)

        result = prepare_weather()

        assert isinstance(result, str)
        assert result == "Weather data is not available at the moment."

    def test_message_when_weather_data_is_empty_dict(self, mocker):
        # Test case for handling when weather data is an empty dictionary
        mocker.patch.object(GetWeather, 'get_data_weather', return_value={})

        result = prepare_weather()

        assert isinstance(result, str)
        assert result == "Weather data is not available at the moment."

    def test_formatted_string_with_missing_values(self, mocker):
        # Test case for creating a formatted string with missing values in weather data
        mocker.patch.object(GetWeather, 'get_data_weather', return_value={
            "name": "London",
            "weather": [{"description": "cloudy"}],
            "main": {},
            "wind": {}
        })

        result = prepare_weather()

        assert isinstance(result, str)
        assert "London" in result
        assert "Cloudy" in result

    def test_data_cache_and_update_time(self, mocker):
        # Test case for checking data caching and update time
        mocker.patch.object(GetWeather, 'get_data_weather', return_value={
            "name": "Moscow",
            "weather": [{"description": "cloudy"}],
            "main": {"temp": 20},
            "wind": {"speed": 10}
        })

        result1 = GetWeather().get_data_weather()
        result2 = GetWeather().get_data_weather()

        assert result1 == result2


class TestPrepareRating:

    def test_chips_rating_formatted_message(self):
        # Test case for formatting message with chips rating
        data = [
            {'username': 'user1', 'total': 100},
            {'username': 'user2', 'total': 200},
            {'username': 'user3', 'total': 300}
        ]
        rating_type = 'chips'
        expected_message_text = "<b>🏆 Топ 10 по количеству фишек:</b>\n\n1. 🥇@user1 - имеет 100 фишек\n2. 🥈@user2 - имеет 200 фишек\n3. 🥉@user3 - имеет 300 фишек"

        result = prepare_rating(data, rating_type)

        assert result == expected_message_text

    def test_wins_rating_formatted_message(self):
        # Test case for formatting message with wins rating
        data = [
            {'username': 'user1', 'wins': 5},
            {'username': 'user2', 'wins': 10},
            {'username': 'user3', 'wins': 15}
        ]
        rating_type = 'wins'
        expected_message_text = "<b>🏆 Топ 10 по количеству побед:</b>\n\n1. 🥇@user1 - имеет 5 побед\n2. 🥈@user2 - имеет 10 побед\n3. 🥉@user3 - имеет 15 побед"

        result = prepare_rating(data, rating_type)

        assert result == expected_message_text

    def test_unsupported_rating_type_message(self):
        # Test case for unsupported rating type
        data = []
        rating_type = 'invalid'
        expected_message_text = "Unsupported rating type"

        result = prepare_rating(data, rating_type)

        assert result == expected_message_text

    def test_username_is_none(self):
        # Test case when username is None
        data = [{'username': None, 'total': 100}]
        rating_type = 'chips'
        expected_message_text = "<b>🏆 Топ 10 по количеству фишек:</b>\n\n"

        result = prepare_rating(data, rating_type)

        assert result == expected_message_text

    def test_username_is_empty(self):
        # Test case when username is an empty string
        data = [{'username': '', 'total': 100}]
        rating_type = 'chips'
        expected_message_text = "<b>🏆 Топ 10 по количеству фишек:</b>\n\n"

        result = prepare_rating(data, rating_type)

        assert result == expected_message_text

    def test_username_is_whitespace(self):
        # Test case when username is whitespace
        data = [{'username': '   ', 'total': 100}]
        rating_type = 'chips'
        expected_message_text = "<b>🏆 Топ 10 по количеству фишек:</b>\n\n1. 🥇@    - имеет 100 фишек"

        result = prepare_rating(data, rating_type)

        assert result == expected_message_text