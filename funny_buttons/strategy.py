
class Sort(object):
    def __init__(self, alghoritm):
        self.alghoritm = alghoritm

    def sort(self, object_list):
        return self.alghoritm.sort(object_list)

class SortAlghoritm(object):
    def sort(self, object_list):
        return object_list

class TimSort(SortAlghoritm):
    def sort(self, object_list):
        return sorted(object_list)

class QuickSort(SortAlghoritm):
    def sort(self, object_list):
        return self.qsort(object_list)

    def qsort(self, L):
        if L == []: return []
        return self.qsort([x for x in L[1:] if x< L[0]]) + L[0:1] + \
            self.qsort([x for x in L[1:] if x>=L[0]])


if __name__ == "__main__":
    L = [1,6,2,74,2,75,2,98,3,75,3,86,2,3,87,87,9,32,12,8,443,6, 52]

    print L
    for Alg in [TimSort, QuickSort]:
        s = Sort(Alg())
        print s.sort(L)
