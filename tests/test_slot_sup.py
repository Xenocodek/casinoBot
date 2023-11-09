import pytest
from utils.slot_sup import (format_number, 
                            get_str_combo,
                            get_result)


class TestFormatNumber:
    def test_valid_input(self):
        assert format_number(3.14) == "3.1"
        assert format_number(2.0) == "2"
        assert format_number(5) == "5"

    def test_negative_input(self):
        assert format_number(-3.14) == "-3.1"
        assert format_number(-2.0) == "-2"
        assert format_number(-5) == "-5"

    def test_decimal_input(self):
        assert format_number(3.14159) == "3.1"
        assert format_number(2.345) == "2.3"
        assert format_number(5.6789) == "5.7"

    def test_large_number_input(self):
        assert format_number(1000000.12345) == "1000000.1"
        assert format_number(9999999.99999) == "9999999"
        assert format_number(1234567890) == "1234567890"

    def test_small_number_input(self):
        assert format_number(0.12345) == "0.1"
        assert format_number(0.00001) == "0"
        assert format_number(0.000000001) == "0"

    def test_large_negative_number_input(self):
        assert format_number(-1000000.12345) == "-1000000.1"
        assert format_number(-9999999.99999) == "-9999999"
        assert format_number(-1234567890) == "-1234567890"

    def test_none_input(self):
        assert format_number(None) == None

    def test_zero_input(self):
        assert format_number(0) == "0"


class TestGetStrCombo:
    def test_return_type(self):
        result = get_str_combo(1)
        for item in result:
            assert isinstance(item, str)

    def test_returns_list_of_length_3(self):
        result = get_str_combo(1)
        assert len(result) == 3

    def test_all_possible_values(self):
        for i in range(1, 65):
            result = get_str_combo(i)
            assert len(result) == 3

            for item in result:
                assert item in ["BAR", "GRAPES", "LEMON", "SEVEN"]

    def test_raises_type_error_for_non_integer_dice_value(self):
        with pytest.raises(TypeError):
            get_str_combo("1")

    def test_empty_list_for_zero_dice_value(self):
        with pytest.raises(ValueError):
            get_str_combo(0)

    def test_raises_value_error_for_dice_value_over_64(self):
        with pytest.raises(ValueError):
            get_str_combo(65)

    def test_raises_value_error_for_negative_dice_value(self):
        with pytest.raises(ValueError):
            get_str_combo(-1)

    def test_raises_type_error_for_non_integer_dice_value(self):
        with pytest.raises(TypeError):
            get_str_combo("1")

    def test_raises_type_error_for_non_numeric_dice_value(self):
        with pytest.raises(TypeError):
            get_str_combo(1.5)

    def test_raises_type_error_for_non_numeric_dice_value_string(self):
        with pytest.raises(TypeError):
            get_str_combo("1.5")


class TestGetResult:
    def test_get_result(self):
        assert get_result(1, 50) == 150
        assert get_result(22, 20) == 100
        assert get_result(43, 25) == 250
        assert get_result(64, 30) == 600

    def test_get_result_boundary_values(self):
        assert get_result(1, 10) == 30
        assert get_result(64, 500) == 10000

    def test_get_result_invalid_values(self):
        assert get_result(5, 100) == 0
        assert get_result(30, 200) == 0

    def test_get_result_zero_values(self):
        assert get_result(2, 100) == 25
        assert get_result(3, 150) == 37.5
        assert get_result(5, 200) == 0 

    def test_get_result_float_values(self):
        assert get_result(6, 120) == 60
        assert get_result(16, 80) == 120
        assert get_result(32, 180) == 270

    def test_get_result_boundary_value_for_value(self):
        assert get_result(1, 10) == 30
        assert get_result(22, 500) == 2500

    def test_get_result_non_numeric_values(self):
        with pytest.raises(TypeError):
            get_result("test", 50)

        with pytest.raises(TypeError):
            get_result(30, "value")

        with pytest.raises(TypeError):
            get_result("test", "value")