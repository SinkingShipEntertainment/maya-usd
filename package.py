name = "maya_usd"

authors = [
    "Autodesk"
]

# NOTE: version = <mayausd_version>.sse.<sse_version>
version = "0.9.0.sse.1.0.0"

description = \
    """
    Maya USD plugin
    """

with scope("config") as c:
    # Determine location to release: internal (int) vs external (ext)

    # NOTE: Modify this variable to reflect the current package situation
    release_as = "ext"

    # The `c` variable here is actually rezconfig.py
    # `release_packages_path` is a variable defined inside rezconfig.py

    import os
    if release_as == "int":
        c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_INT"]
    elif release_as == "ext":
        c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

    #c.build_thread_count = "physical_cores"

requires = [
]

private_build_requires = [
    "cmake",
    #"usd-20.08.sse.2",
    "PyOpenGL",
    "Jinja2",
    "PyYAML",
    "PySide2",
    "maya_devkit-2022",
    "qtbase-5.15.2",
]

variants = [
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2022.0.sse.2", "~python-2", "usd-20.08.sse.2"],
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2022.0.sse.3", "~python-3", "usd-20.08.sse.3"],
]

build_command = "bash {root}/rez_build.sh {root}"

uuid = "repository.maya-usd"

def pre_build_commands():
    command("source /opt/rh/devtoolset-6/enable")

    # To build against USD from Maya installation
    # NOTE: It's not working at this moment
    #env.MAYA_PXRUSD3_LOCATION = "/usr/autodesk/mayausd/maya2022/0.8.0_202102180129-2f83c8f/mayausd/USD3"
    #env.MAYA_PXRUSD2_LOCATION = "/usr/autodesk/mayausd/maya2022/0.8.0_202102180129-2f83c8f/mayausd/USD2"

def commands():

    # NOTE: REZ package versions can have ".sse." to separate the external
    # version from the internal modification version.
    split_versions = str(version).split(".sse.")
    external_version = split_versions[0]
    internal_version = None
    if len(split_versions) == 2:
        internal_version = split_versions[1]

    env.MAYA_USD_VERSION = external_version
    env.MAYA_USD_PACKAGE_VERSION = external_version
    if internal_version:
        env.MAYA_USD_PACKAGE_VERSION = internal_version

    env.MAYA_USD_ROOT.append("{root}")
    env.MAYA_USD_LOCATION.append("{root}")

    # For Maya to locate the .mod file to setup env variables for plugins and libraries
    env.MAYA_MODULE_PATH.append("{root}/module")
    env.MAYA_LOAD_USD.append("ON")

    env.PATH.append("{root}/module/mayausd/MayaUSD/lib")
    env.PATH.append("{root}/module/mayausd/usd/bin")
    env.PATH.append("{root}/module/mayausd/usd/lib")
