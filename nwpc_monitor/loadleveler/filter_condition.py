# coding: utf-8
class FilterCondition(object):
    def __init__(self):
        pass

    def is_fit(self, job_item):
        return True


class PropertyFilterCondition(FilterCondition):
    def __init__(self, property_id, data_checker):
        FilterCondition.__init__(self)
        self.property_id = property_id
        self.data_checker = data_checker

    def get_property_data(self, job_item):
        result = None
        for a_prop in job_item['props']:
            if a_prop['id'] == self.property_id:
                result = a_prop['data']
        return result

    def is_fit(self, job_item):
        value = self.get_property_data(job_item)
        if self.data_checker(value):
            return True
        else:
            return False


def create_equal_value_checker(expect_value):
    def value_checker(value):
        if value == expect_value:
            return True
        else:
            return False

    return value_checker


def create_greater_value_checker(expect_value):
    def value_checker(value):
        if value > expect_value:
            return True
        else:
            return False

    return value_checker


def create_less_value_checker(expect_value):
    def value_checker(value):
        if value < expect_value:
            return True
        else:
            return False

    return value_checker


def create_in_value_checker(expect_values):
    def value_checker(value):
        if value in expect_values:
            return True
        else:
            return False
    return value_checker
