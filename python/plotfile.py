#!/usr/bin/env python
# File       : plotfile.py
# Created    : Thu Mar 26 2020 09:45:41 PM (+0100)
# Author     : Fabian Wermelinger
# Description: Plotfile tool
# Copyright 2020 ETH Zurich. All Rights Reserved.
import numpy as np
import argparse
import os

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--files', nargs='+', type=str, help='Input file(s)', required=True)
    parser.add_argument('--header', action='store_true', help='Print header information')
    parser.add_argument('--nan', action='store_true', help='Check for NaN values')

    return parser.parse_known_args()

def readHeader(f):
    hdr = {}
    with open(os.path.join(f, 'Header')) as header:
        hdr['versionName'] = header.readline().strip()
        nvars = int(header.readline().strip())
        hdr['variables'] = []
        for i in range(nvars):
            hdr['variables'].append(header.readline().strip())
        hdr['dim'] = int(header.readline().strip())
        hdr['time'] = float(header.readline().strip())
        hdr['finestLevel'] = int(header.readline().strip())
        hdr['domainBegin'] = np.array([float(x) for x in header.readline().strip().split()])
        hdr['domainEnd'] = np.array([float(x) for x in header.readline().strip().split()])
        hdr['refRatio'] = np.array([float(x) for x in header.readline().strip().split()])
        domains = header.readline().strip().split()
        hdr['indexDomains'] = []
        for i in range(hdr['finestLevel'] + 1):
            d = {}
            d['begin'] = np.array([int(x) for x in domains[i * 3 + 0].replace('(', '').replace(')', '').split(',')])
            d['end']   = np.array([int(x) for x in domains[i * 3 + 1].replace('(', '').replace(')', '').split(',')])
            d['type']  = np.array([int(x) for x in domains[i * 3 + 2].replace('(', '').replace(')', '').split(',')])
            hdr['indexDomains'].append(d)
        hdr['levelSteps'] = np.array([int(x) for x in header.readline().strip().split()])
        hdr['dx'] = []
        for i in range(hdr['finestLevel'] + 1):
            hdr['dx'].append(np.array([float(x) for x in header.readline().strip().split()]))
        hdr['coordinateSystem'] = int(header.readline().strip())
        header.readline() # padding zero
        # read levels
        hdr['levelData'] = []
        for i in range(hdr['finestLevel'] + 1):
            level = {}
            items = header.readline().strip().split()
            level['level']  = int(items[0])
            level['nBoxes'] = int(items[1])
            level['time']   = float(items[2])
            level['levelSteps'] = int(header.readline().strip())
            level['box'] = []
            for b in range(level['nBoxes']):
                lo = []
                hi = []
                for dim in range(hdr['dim']):
                    dims = header.readline().strip().split()
                    lo.append(float(dims[0]))
                    hi.append(float(dims[1]))
                level['box'].append({
                    'begin' : np.array(lo),
                    'end' : np.array(hi)
                    })
            level['levelPath'] = header.readline().strip()
            hdr['levelData'].append(level)
    return hdr

def printHeader(f):
    hdr = readHeader(f)
    spacing = ''
    for dx in hdr['dx']:
        spacing += '('
        spacing += ' '.join(['{:e}'.format(x) for x in dx])
        spacing += ') '
    print("""
    File:              {file}
    Version:           {version}
    Time:              {time}
    Variables:         [{nvars}] {variables}
    Dimension:         {dim}
    Domain begin:      {domainBegin}
    Domain end:        {domainEnd}
    Finest level:      {finestLevel}
    Refinement ratios: {refRatio}
    Grid spacings:     {dx}
    """.format(
        file = f,
        version = hdr['versionName'],
        nvars = len(hdr['variables']),
        variables = ' '.join(hdr['variables']),
        dim = hdr['dim'],
        time = hdr['time'],
        domainBegin = ' '.join(['{:e}'.format(x) for x in hdr['domainBegin']]),
        domainEnd = ' '.join(['{:e}'.format(x) for x in hdr['domainEnd']]),
        finestLevel = hdr['finestLevel'],
        refRatio = ' '.join(['{:e}'.format(x) for x in hdr['refRatio']]),
        dx = spacing.strip()
        ))

def checkNan(f):
    pass

def main():
    args, _ = parseArgs()

    for f in args.files:
        print('Processing: {}'.format(f))

        if args.header:
            printHeader(f)
        elif args.nan:
            checkNan(f)

if __name__ == "__main__":
    main()
