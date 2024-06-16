import filter_functions as ff
import numpy as np

def get_cov_z_extract(values, sizeOfIntervals, overlapRatio):
        minVal = min(values)
        maxVal = max(values)

        # Calculate the step size between intervals
        stepSize = sizeOfIntervals * (1 - overlapRatio)

        # Generate intervals
        intervals = []
        start = minVal

        while start < maxVal:
            end = start + sizeOfIntervals
            intervals.append([start, end])
            start += stepSize

        return intervals
def get_cov_z_extract_datapts(dataPts, values, paramCov):
    dataPtsCov = []
    for intvl in paramCov:
        minVal=intvl[0]
        maxVal=intvl[1]
        temp = []
        for i in range(0, len(dataPts)):
            if (values[i]>=minVal and values[i]<=maxVal):
                temp.append(dataPts[i])
        dataPtsCov.append(temp)
    return dataPtsCov

def get_cov_y_extract(values, sizeOfIntervals, overlapRatio):
    minVal = min(values)
    maxVal = max(values)

    # Calculate the step size between intervals
    stepSize = sizeOfIntervals * (1 - overlapRatio)

    # Generate intervals
    intervals = []
    start = minVal

    while start < maxVal:
        end = start + sizeOfIntervals
        if(end > maxVal):
            end=maxVal
        intervals.append([start, end])
        start += stepSize

    return intervals
def get_cov_y_extract_datapts(dataPts, values, paramCov):
    dataPtsCov = []
    for intvl in paramCov:
        minVal = intvl[0]
        maxVal = intvl[1]
        temp = []
        for i in range(0, len(dataPts)):
            if (values[i] >= minVal and values[i] <= maxVal):
                temp.append(dataPts[i])
        dataPtsCov.append(temp)
    return dataPtsCov

def get_cov_eccentricity_p(values, sizeOfIntervals, overlapRatio):
    minVal = min(values)
    maxVal = max(values)

    # Calculate the step size between intervals
    stepSize = sizeOfIntervals * (1 - overlapRatio)

    # Generate intervals
    intervals = []
    start = minVal

    while start < maxVal:
        end = start + sizeOfIntervals
        intervals.append([start, end])
        start += stepSize

    return intervals
def get_cov_eccentricity_p_dataPts(dataPts, values, paramCov):
    dataPtsCov = []
    for intvl in paramCov:
        minVal = intvl[0]
        maxVal = intvl[1]
        temp = []
        for i in range(0, len(dataPts)):
            if(values[i]>=minVal and values[i]<=maxVal):
                temp.append(dataPts[i])
        dataPtsCov.append(temp)
    return dataPtsCov






