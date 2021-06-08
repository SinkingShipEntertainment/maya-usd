!/usr/bin/bash

root_dir=$1

# build
echo "----------------------------------------------------------------------"
echo "Running build.py..."
echo "----------------------------------------------------------------------"

python ${root_dir}/build.py ${root_dir} \
    --verbosity 2 \
    --build-location ${REZ_BUILD_PATH} \
    --install-location ${REZ_BUILD_INSTALL_PATH} \
    --maya-location ${MAYA_LOCATION} \
    --pxrusd-location ${USD_LOCATION} \
    --devkit-location ${DEVKIT_LOCATION} \
    --qt-location ${QT_LOCATION} \
    --build-release
