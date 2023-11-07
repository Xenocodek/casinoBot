from utils.slot_sup import format_number



class TestSlotSup:
    def test_valid_input(self):
        assert format_number(3.14) == "3.1"
        assert format_number(2.0) == "2"
        assert format_number(5) == "5"

    def test_negative_input(self):
        assert format_number(-3.14) == "-3.1"
        assert format_number(-2.0) == "-2"
        assert format_number(-5) == "-5"

    def test_none_input(self):
        assert format_number(None) == None

    def test_zero_input(self):
        assert format_number(0) == "0"