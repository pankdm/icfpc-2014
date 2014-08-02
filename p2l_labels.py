

MAIN_LABEL = '__main_label__'
LAPSHA_LOAD_LABEL = '__lapsha_load_label__'
LAPSHA_SAVE_LABEL = '__lapsha_save_label__'

class LabelProvider:
    WHILE_PREFIX = 'while'
    IF_PREFIX = 'if'
    ANY_PREFIX = 'any'

    def __init__(self):
        self.counter = 0
        # self.f = open('labels.txt', 'wt')

    def next_generic_label(self, prefix, suffix):
        result = '__{}_{}_{}__'.format(
            prefix, suffix, self.counter)
        self.counter += 1
        # print >> self.f, result
        return result

    def next_while_label(self, suffix):
        return self.next_generic_label(self.WHILE_PREFIX, suffix)

    def next_if_label(self, suffix):
        return self.next_generic_label(self.IF_PREFIX, suffix)

    def next_any_label(self, suffix):
        return self.next_generic_label(self.ANY_PREFIX, suffix)


LABEL_PROVIDER = LabelProvider()

