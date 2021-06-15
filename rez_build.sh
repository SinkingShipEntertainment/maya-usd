!/usr/bin/bash

root_dir=$1

# build
echo "----------------------------------------------------------------------"
echo "Running build.py..."
echo "----------------------------------------------------------------------"

echo "REZ_BUILD_PATH: ${REZ_BUILD_PATH}"
echo "REZ_BUILD_INSTALL_PATH: ${REZ_BUILD_INSTALL_PATH}"
echo "MAYA_LOCATION: ${MAYA_LOCATION}"
echo "DEVKIT_LOCATION: ${DEVKIT_LOCATION}"
echo "QT_LOCATION: ${QT_LOCATION}"

export BUILD_NUM_JOBS=1

if [ ${REZ_BUILD_VARIANT_INDEX} = 0 ]
then
    #echo "USD_LOCATION: ${MAYA_PXRUSD2_LOCATION}"
    echo "USD_LOCATION: ${USD_LOCATION}"
    echo "--------------------------"
    echo "Building variant 0 (Maya Python 2)"

    echo "=============================================="
    echo "PATH:"
    echo ${PATH}
    echo "=============================================="
    echo "PYTHONPATH:"
    echo ${PYTHONPATH}
    echo "=============================================="

    python ${root_dir}/build.py \
        --verbosity "2" \
        --build-location ${REZ_BUILD_PATH} \
        --install-location ${REZ_BUILD_INSTALL_PATH} \
        --maya-location ${MAYA_LOCATION} \
        --pxrusd-location ${USD_LOCATION} \
        --devkit-location ${DEVKIT_LOCATION} \
        --qt-location ${QT_LOCATION} \
        --redirect-outstream-file "0" \
        --build-args="-DCMAKE_MAKE_PROGRAM=/usr/bin/ninja,-DBUILD_WITH_PYTHON_3=OFF" \
        --build-release \
        --generator Ninja \
        --jobs ${BUILD_NUM_JOBS} \
        ${root_dir}

elif [ ${REZ_BUILD_VARIANT_INDEX} = 1 ]
then
    #echo "USD_LOCATION: ${MAYA_PXRUSD3_LOCATION}"
    echo "USD_LOCATION: ${USD_LOCATION}"

    echo "--------------------------"
    echo "Building variant 1 (Maya Python 3)"

    echo "=============================================="
    echo "PATH:"
    echo ${PATH}
    echo "=============================================="
    echo "PYTHONPATH:"
    echo ${PYTHONPATH}
    echo "=============================================="

    python ${root_dir}/build.py \
        --verbosity "2" \
        --build-location ${REZ_BUILD_PATH} \
        --install-location ${REZ_BUILD_INSTALL_PATH} \
        --maya-location ${MAYA_LOCATION} \
        --pxrusd-location ${USD_LOCATION} \
        --devkit-location ${DEVKIT_LOCATION} \
        --qt-location ${QT_LOCATION} \
        --redirect-outstream-file "0" \
        --build-args="-DCMAKE_MAKE_PROGRAM=/usr/bin/ninja,-DBUILD_WITH_PYTHON_3=ON" \
        --build-release \
        --generator Ninja \
        --jobs ${BUILD_NUM_JOBS} \
        ${root_dir}

fi
