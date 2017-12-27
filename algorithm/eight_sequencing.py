# -*- coding:utf-8 -*-

#author:waiwen
#email:iwaiwen@163.com
#time: 2017/12/18 19:29
import random
import pandas
"""
记录八大算法

"""

random_nums = [random.choice([int(i)  for i in range(1000) ]) for i in range(50)]


"""
快速排序。
使用递归的方法,根据一个判断值，比判断值大的大子集，比判断值小的小子集，不断的去划分子集。
"""

#直接进行快速排序
def quick(l):
    if len(l)<2:
        return l
    m= l[0]
    s = [ i for i in l[1:] if i <= m]
    b = [ i for i in l[1:] if i >  m]
    return  quick(s)+[m]+quick(b)

#根据位置进行快速排序
def QuickSort(myList,start,end):
    #判断low是否小于high,如果为false,直接返回
    if start < end:
        i,j = start,end
        #设置基准数
        base = myList[i]
        while i < j:
            #如果列表后边的数,比基准数大或相等,则前移一位直到有比基准数小的数出现
            while (i < j) and (myList[j] >= base):
                j = j - 1
            #如找到,则把第j个元素赋值给第个元素i,此时表中i,j个元素相等
            myList[i] = myList[j]
            #同样的方式比较前半区
            while (i < j) and (myList[i] <= base):
                i = i + 1
            myList[j] = myList[i]
        #做完第一轮比较之后,列表被分成了两个半区,并且i=j,需要将这个数设置回base
        myList[i] = base
        #递归前后半区
        QuickSort(myList, start, i - 1)
        QuickSort(myList, j + 1, end)
    return myList


"""
归并排序，

"""
def mergesort(seq):
    if len(seq) <= 1:
        return seq
    mid = len(seq)//2
    left = mergesort(seq[:mid])
    print('mergesort_left',left)
    right = mergesort(seq[mid:])
    print('mergesort_right',right)
    return merge(left,right)

def merge(left,right):
    print('merge_left', left)
    print('merge_right',right)
    result=[]
    i,j=0,0
    while i<len(left) and j<len(right):
        if left[i]<=right[j]:       #不断遍历，按顺序添加左右两个集合里面小的元素，直至其中一个集合为空
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1
    print('1',result)
    result+=left[i:]
    result+=right[j:]
    print('2',result)
    return result


"""
选择排序中的简单排序
"""

def select_simple(l):
    for  i in range(0,len(l)-1):
        for j in range(i+1,len(l)):
            if l[i] > l[j]:
                l[i], l[j] = l[j], l[i]
    return l

"""
选择排序的堆排序
"""


if __name__ == '__main__':
    # print(quick(random_nums))
    # print(select_simple(random_nums))
    #
    # print(mergesort([32,54,33,34,89,23]))

    l = [0,1,2,3,4]
    for i in range(0,len(l)-1):
        print (l[i])


