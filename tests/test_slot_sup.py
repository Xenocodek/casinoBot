from utils.slot_sup import format_number



class TestSlotSup:
    def test_valid_input(self):
        assert format_number(3.14) == "3.1"
        assert format_number(2.0) == "2"
        assert format_number(5) == "5"