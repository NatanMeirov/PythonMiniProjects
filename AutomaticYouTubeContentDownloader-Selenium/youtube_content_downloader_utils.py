# This algorithm is not the final version - NOT PERFECT YET...
def find_correct_item_element_index_by_title(all_item_names: list, wanted_item_name: str) -> int:
    wanted_item_name_words = wanted_item_name.strip("\\/").split(" ") # Cleaning the titles from Youtube
    all_item_names_words_lists = [[title.strip("\\/").split(" ")] for title in all_item_names]
    item_compare_list = ItemCompareObjectsList()

    max_words_count = len(wanted_item_name_words)
    counter = 0
    for i in range(len(all_item_names_words_lists)):
        current_title_index = i # Saving its index in the macro list
        title_words = all_item_names_words_lists[i]

        for word in wanted_item_name_words:
            if word in title_words:
                counter += 1
                title_words.remove(word)

        frequency = counter / max(max_words_count, len(title_words))

        item_compare_list.add_new_item_compare_object(ItemCompareObject(current_title_index, frequency))

    return item_compare_list.find_most_frequent_item().get_index()


class ItemCompareObject:
    def __init__(self, index_of_title: int, frequency: float):
        self.__index_of_title = index_of_title
        self.__frequency = frequency

    def get_frequency(self):
        return self.__frequency

    def get_index(self):
        return self.__index_of_title

    # Comparison Operators Overloading:
    def __le__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.__frequency <= other.get_frequency()
        return NotImplemented

    def __ge__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return self.__frequency >= other.get_frequency()
        return NotImplemented


class ItemCompareObjectsList:
    def __init__(self):
        self.__item_compare_objects_list = []

    def add_new_item_compare_object(self, item_compare_object: ItemCompareObject) -> None:
        self.__item_compare_objects_list.append(item_compare_object)

    def find_most_frequent_item(self) -> ItemCompareObject:
        most_frequent_item = self.__item_compare_objects_list[0]

        for i in range(len(self.__item_compare_objects_list)):
            item = self.__item_compare_objects_list[i]
            if item is not self.__item_compare_objects_list[-1]: # Item is not the last item
                if item >= most_frequent_item:
                    most_frequent_item = item

        return most_frequent_item