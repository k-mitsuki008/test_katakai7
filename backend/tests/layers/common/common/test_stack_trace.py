from common.stack_trace import get_stack_trace


class TestStackTrace:
    def test_get_stack_trace(self):
        """
        正常系
        """
        actual = get_stack_trace()
        assert type(actual) is str
