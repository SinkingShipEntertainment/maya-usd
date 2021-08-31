name = "maya_usd"

authors = [
    "Autodesk"
]

# NOTE: version = <mayausd_version>.sse.<sse_version>
version = "0.10.0.sse.1.0.0"

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
    "PyOpenGL",
    "Jinja2",
    "PyYAML",
    "PySide2",
    "maya_devkit-2022",
    "qtbase-5.15.2",
]

variants = [
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2022.0.sse.2", "python-2", "usd-20.08.sse.1", "!ptex"],
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2022.0.sse.3", "python-3", "usd-20.08.sse.1", "!ptex"],
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2022.0.sse.2", "python-2", "usd-21.05.sse.1", "!ptex"],
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2022.0.sse.3", "python-3", "usd-21.05.sse.1", "!ptex"],
]

# If want to use Ninja, run:
# rez-build -i --cmake-build-system "ninja"
# rez-release --cmake-build-system "ninja"
#
# Pass cmake arguments:
# rez-build -i -- -DBoost_NO_BOOST_CMAKE=On -DBoost_NO_SYSTEM_PATHS=True
# rez-release -- -DBoost_NO_BOOST_CMAKE=On -DBoost_NO_SYSTEM_PATHS=True

uuid = "repository.maya-usd"

def pre_build_commands():
    command("source /opt/rh/devtoolset-6/enable")

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
    env.MAYA_MODULE_PATH.append("{root}")
