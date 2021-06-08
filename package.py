name = "maya_usd"

authors = [
    "Autodesk"
]

version = "0.9.0"

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
    "gcc-6.3",
    "maya-2022.0",
    "PyOpenGL",
    "Jinja2",
    "PyYAML",
    "PySide2",
]

private_build_requires = [
    "cmake",
    "python-2.7",
    "maya_devkit-2022",
    "qtbase-5.15.2",
]

variants = [
    ["platform-linux", "arch-x86_64", "os-centos-7", "usd-20.08"],
]

build_command = "bash {root}/rez_build.sh {root}"

# If want to use Ninja, run the `rez-build -i --cmake-build-system "ninja"`
# or `rez-release --cmake-build-system "ninja"`

uuid = "repository.maya-usd"

def commands():
    # NOTE: REZ package versions can have "-" to separate the external
    # version from the internal modification version.
    # Example: 0.9.0-sse.1
    # 0.9.0 is the maya-usd version and sse.1 is the internal version
    split_versions = str(version).split('-')
    env.MAYA_USD_VERSION.set(split_versions[0])
    if len(split_versions) == 2:
        env.MAYA_USD_PACKAGE_VERSION.set(split_versions[1])

    env.MAYA_USD_ROOT.append("{root}")
    env.MAYA_USD_LOCATION.append("{root}")

    # For Maya to locate the .mod file to setup env variables for plugins and libraries
    env.MAYA_MODULE_PATH.append("{root}/module")
    env.MAYA_LOAD_USD.append("ON")

    env.PATH.append("{root}/module/mayausd/MayaUSD/lib")
    env.PATH.append("{root}/module/mayausd/usd/bin")
    env.PATH.append("{root}/module/mayausd/usd/lib")
