# Check system

Small cli tool that check system environment markers according to PEP 508 and
exits with an error if it is not.

It is meant to be used to abort scripts that are run on the "wrong" system,
e.g., a compilation of requirements (with pip-compile) run on a different
architecture than the intended use of the requirement file.

The whole library is just one file
[check_system.py](src/check_system/check_system.py).

## Usage

```shell
$ check-system --help
usage: check-system [-h] [--os-name OS_NAME] [--sys-platform SYS_PLATFORM] [--platform-machine PLATFORM_MACHINE] [--platform-python-implementation PLATFORM_PYTHON_IMPLEMENTATION] [--platform-release PLATFORM_RELEASE] [--platform-system PLATFORM_SYSTEM] [--platform-version PLATFORM_VERSION]
                    [--python-version PYTHON_VERSION] [--python-full-version PYTHON_FULL_VERSION] [--implementation-name IMPLEMENTATION_NAME] [--implementation-version IMPLEMENTATION_VERSION]

options:
  -h, --help            show this help message and exit
  --os-name OS_NAME
  --sys-platform SYS_PLATFORM
  --platform-machine PLATFORM_MACHINE
  --platform-python-implementation PLATFORM_PYTHON_IMPLEMENTATION
  --platform-release PLATFORM_RELEASE
  --platform-system PLATFORM_SYSTEM
  --platform-version PLATFORM_VERSION
  --python-version PYTHON_VERSION
  --python-full-version PYTHON_FULL_VERSION
  --implementation-name IMPLEMENTATION_NAME
  --implementation-version IMPLEMENTATION_VERSION
```

## Example

Run on a Linux laptop

```shell
$ check-system --sys-platform linux
$ echo $?  # prints last exit code
0
$ check-system --sys-platform windows
Check failed: sys_platform was linux. Checked against: windows
$ echo $?
1
```
