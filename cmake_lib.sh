#!/usr/bin/env bash
set -e


build()
{
    local dst="$1"; shift
    if [[ -d "${dst}" ]]; then
        echo "Skip existing: ${dst}"
        return
    fi
    rm -rf build
    mkdir -p build
    cd build && cmake \
        -DCMAKE_INSTALL_PREFIX=../${dst} \
        -DCMAKE_C_COMPILER=mpicc \
        -DCMAKE_CXX_COMPILER=mpic++ \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo "$@" ..
    make -j
    make install
    cd ..
}

dst='gnu3D_DP'
build ${dst}

dst='gnu3D_SP'
build ${dst} -DENABLE_DP=NO

# Classical make
# build()
# {
#     local dst="$1"; shift
#     local dim="$1"; shift
#     ./configure --prefix ${dst} --comp gnu --dim ${dim}
#     make -j "$@"
#     make install
#     make clean
# }

# dst='gnu3D_DP'
# rm -rf ${dst}
# mkdir -p ${dst}
# build ${dst} 3 PRECISION=DOUBLE

# dst='gnu3D_SP'
# rm -rf ${dst}
# mkdir -p ${dst}
# build ${dst} 3 PRECISION=FLOAT
