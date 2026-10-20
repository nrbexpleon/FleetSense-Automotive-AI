from __future__ import annotations
from math import sqrt
from statistics import median

def mean(values:list[float])->float:return sum(values)/len(values) if values else 0.0
def variance(values:list[float])->float:
    if len(values)<2:return 0.0
    average=mean(values);return sum((value-average)**2 for value in values)/(len(values)-1)
def stdev(values:list[float])->float:return sqrt(variance(values))
def mad(values:list[float])->float:
    if not values:return 0.0
    centre=median(values);return median(abs(value-centre) for value in values)
def percentile(values:list[float],probability:float)->float:
    if not values:return 0.0
    ordered=sorted(values);index=max(0,min(len(ordered)-1,int((len(ordered)-1)*probability+0.999999)));return ordered[index]
def correlation(left:list[float],right:list[float])->float:
    if len(left)!=len(right) or len(left)<2:return 0.0
    left_mean,right_mean=mean(left),mean(right);numerator=sum((a-left_mean)*(b-right_mean) for a,b in zip(left,right));denominator=sqrt(sum((a-left_mean)**2 for a in left)*sum((b-right_mean)**2 for b in right));return numerator/denominator if denominator else 0.0
