from .common import Common
from .xplat_utils import Utils


# --------------------
## return the root directory.
# Either "." locally or the cwd if in a module
#
# @return the root directory
def root_dir():
    return Utils.root_dir()


# --------------------
## return the module name for this given arg
#
# @return the module name or an error message
def get(var):
    # if var is invalid, AttributeError is thrown
    return getattr(Common, var)


# --------------------
## get the version string from the module's version.json file
# get the long desc i.e. the README.md content
#
# @return the version string and the long version of it
def init():
    gen_version_json(True)

    Common.long_version = Common.version.replace('.', '_')
    Common.long_desc = (Utils.root_dir() / 'README.md').read_text()
    Common.long_desc_type = 'text/markdown'


# --------------------
def gen_version_json(verbose):
    Utils.set_params(verbose, Common)
    Utils.gen_version_json()


# --------------------
def gen_build_info_file(verbose):
    Utils.set_params(verbose, Common)
    Utils.gen_build_info_file()


# --------------------
def do_clean(verbose):
    Utils.set_params(verbose, Common)
    Utils.do_clean()


# --------------------
def do_lint(verbose):
    Utils.set_params(verbose, Common)
    Utils.do_lint()


# --------------------
def do_doc(verbose):
    Utils.set_params(verbose, Common)
    Utils.do_doc()


# --------------------
def do_check(verbose):
    Utils.set_params(verbose, Common)
    Utils.do_check()


# --------------------
def do_publish(verbose):
    Utils.set_params(verbose, Common)
    Utils.do_publish()
