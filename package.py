name = "maya_usd"

authors = [
    "Autodesk"
]

# NOTE: version = <mayausd_version>.sse.<sse_version>
version = "0.28.0.sse.2.0.0"

description = """Maya USD plugin"""

with scope("config") as c:
    import os
    c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

requires = [
]

private_build_requires = [
    "PyOpenGL",
    "Jinja2",
    "PyYAML",
    "PySide6",
    "maya_devkit",
]

variants = [
    ["maya-2024.2", "python-3.9", "usd-23.11"],
    ["maya-2025.1", "python-3.11", "usd-23.11"],
]

# If want to use Ninja, run:
# rez-build -i --cmake-build-system "ninja"
# rez-release --cmake-build-system "ninja"
#
# Pass cmake arguments:
# rez-build -i
# rez-release

uuid = "repository.maya-usd"

def pre_build_commands():

    info = {}
    with open("/etc/os-release", 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line_info = line.replace('\n', '').split('=')
            if len(line_info) != 2:
                continue
            info[line_info[0]] = line_info[1].replace('"', '')
    linux_distro = info.get("NAME", "centos")
    print("Using Linux distro: " + linux_distro)

    if linux_distro.lower().startswith("centos"):
        # command("source /opt/rh/devtoolset-6/enable")
        command("source /opt/rh/devtoolset-9/enable")
    elif linux_distro.lower().startswith("rocky"):
        pass

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