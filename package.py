name = "maya_usd"

authors = [
    "Autodesk"
]

# NOTE: version = <mayausd_version>.sse.<sse_version>
version = "0.22.0.sse.1.0.1"

description = """Maya USD plugin"""

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


# NOTE: Ptex from USD used to cause Maya to crash.
# To fix that, USD is built with ptex and without ptex.
# Up to Maya-Usd version 0.19, we have been building it forcing no Ptex.
# Also, it could be Arnold (Maya plugin) that is causing it to crash.
# This version (0.22) will be build allowing Ptex to see how it respond.
requires = [
    # "!ptex",
]

private_build_requires = [
    "PyOpenGL",
    "Jinja2",
    "PyYAML",
    "pyside2_setup",
]

variants = [
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2023.0", "maya_devkit-2023.0", "python-3.9.7", "usd-22.11"],
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2023.2", "maya_devkit-2023.2", "python-3.9.7", "usd-22.11"],
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

def post_commands():

    # For Maya to locate the .mod file to setup env variables for plugins and libraries
    # NOTE: We are prepending because the REZ package "maya" is appending the
    # out-of-the-box modules, which includes mayaUSD.mod as well. We want us to be
    # loaded as priority.
    env.MAYA_MODULE_PATH.prepend("{root}")
