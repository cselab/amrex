#!/usr/bin/env bash
set -e

rm -rf build
mkdir -p build
cd build && cmake \
    -DCMAKE_C_COMPILER=mpicc \
    -DCMAKE_CXX_COMPILER=mpic++ \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo "$@" ..
