import types


# 3адание №1
class FlatIterator:
    def __init__(self, list_of_lists):
        self.list_of_lists = list_of_lists
        self.flat_list = [item for sublist in list_of_lists for item in sublist]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.flat_list):
            item = self.flat_list[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration


def test_1():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    for flat_iterator_item, check_item in zip(FlatIterator(list_of_lists_1),
                                              ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


# Задание #2
def flat_generator(list_of_lists):
    for item in list_of_lists:
        if isinstance(item, list):
            yield from flat_generator(item)
        else:
            yield item


def test_2():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    for flat_iterator_item, check_item in zip(flat_generator(list_of_lists_1),
                                              ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == "__main__":

    list_of_lists_test = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    result_1 = list(FlatIterator(list_of_lists_test))
    print(result_1)
    test_1()

    result_2 = list(flat_generator(list_of_lists_test))
    print(result_2)
    test_2()
