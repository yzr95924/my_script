'''
setup my ssh key from encrypted file
'''

import os
import getopt
import sys
import errno

sys.path.append("../common_include")
_g_proc_name = "setup_ssh_key"

from my_py import logger
from my_py import crypto_tool
from my_py import os_util
from my_py import setup

_g_is_dry_run = False
_g_is_debug = False
_g_logger = logger.get_logger(name=_g_proc_name)

_g_cipher_key_dir = "./cipher_key"
_g_plaintext_key_dir = os.path.join(os.path.expanduser("~"), ".ssh")


def usage():
    print("Usage: python3 {} -r -d -e -i <input key> -p <password>")
    print("-r (optional): dry run")
    print("-d (optional): debug mode")
    print("-e (optional): encryption mode")
    print("-i: path of input private key")
    print("-p: password")


def enc_key_to_cipher_dir(private_key_path: str, pwd: str):
    _g_logger.info("enable enc mode")
    out_private_path = os.path.basename(private_key_path) + ".enc"
    out_private_path = os.path.join(_g_cipher_key_dir, out_private_path)
    _g_logger.info("out enc private key path: {}".format(out_private_path))

    key_bytes = crypto_tool.Hasher.cal_sha256_hash(pwd)
    ret = crypto_tool.AESCipher.encrypt_with_key(private_key_path,
                                                 key_bytes,
                                                 out_private_path)
    if (ret != 0):
        _g_logger.error("enc private key failed: {}".format(
            os_util.translate_linux_err_code(ret)))
        return ret
    _g_logger.info("enc private key successful: {}".format(out_private_path))

    public_key_path = private_key_path + ".pub"
    out_public_path = os.path.basename(public_key_path) + ".enc"
    out_public_path = os.path.join(_g_cipher_key_dir, out_public_path)
    _g_logger.info("out enc public key path: {}".format(out_public_path))

    ret = crypto_tool.AESCipher.encrypt_with_key(public_key_path,
                                                 key_bytes,
                                                 out_public_path)
    if (ret != 0):
        _g_logger.error("enc public key failed: {}".format(
            os_util.translate_linux_err_code(ret)))
        return ret
    _g_logger.info("enc public key successful: {}".format(out_public_path))

    return 0


def dec_key_to_plaintext_dir(enc_private_key_path: str, pwd: str):
    ret = 0
    _g_logger.info("disable enc mode")
    out_private_path = os.path.basename(enc_private_key_path)
    if (not out_private_path.endswith(".enc")):
        _g_logger.error("input enc private key path invalid")
        return errno.EINVAL
    out_private_path = out_private_path[:-4]
    out_private_path = os.path.join(_g_plaintext_key_dir, out_private_path)
    _g_logger.info("out private key path: {}".format(out_private_path))

    if (os_util.FS.check_if_file_exist(out_private_path)):
        ret = os_util.FS.change_file_mode(out_private_path, "600")
        if (ret != 0):
            _g_logger.error("change private key mode with write failed: {}".format(
                os_util.translate_linux_err_code(ret)
            ))
            return ret

    if (not os_util.FS.check_if_file_exist(_g_plaintext_key_dir)):
        ret = os_util.FS.mkdir_p(_g_plaintext_key_dir)
        if (ret != 0):
            _g_logger.error("create dir {} failed: {}".format(
                _g_plaintext_key_dir, os_util.translate_linux_err_code(ret)
            ))
            return ret

    key_bytes = crypto_tool.Hasher.cal_sha256_hash(pwd)
    ret = crypto_tool.AESCipher.decrypt_with_key(enc_private_key_path,
                                                 key_bytes,
                                                 out_private_path)
    if (ret != 0):
        _g_logger.error("dec private key failed: {}".format(
            os_util.translate_linux_err_code(ret)))
        return ret
    _g_logger.info("dec private key successful: {}".format(out_private_path))

    public_key_path = enc_private_key_path[:-4] + ".pub" + ".enc"
    out_public_path = os.path.basename(enc_private_key_path[:-4] + ".pub")
    out_public_path = os.path.join(_g_plaintext_key_dir, out_public_path)
    _g_logger.info("out public key path: {}".format(out_public_path))

    if (os_util.FS.check_if_file_exist(out_public_path)):
        ret = os_util.FS.change_file_mode(out_public_path, "600")
        if (ret != 0):
            _g_logger.error("change public key mode with write failed: {}".format(
                os_util.translate_linux_err_code(ret)
            ))
            return ret

    ret = crypto_tool.AESCipher.decrypt_with_key(public_key_path,
                                                 key_bytes,
                                                 out_public_path)
    if (ret != 0):
        _g_logger.error("dec public key failed: {}".format(
            os_util.translate_linux_err_code(ret)))
        return ret
    _g_logger.info("dec public key successful: {}".format(out_public_path))

    return 0


def change_key_file_mode(enc_private_key_path: str):
    private_key_name = os.path.basename(enc_private_key_path[:-4])
    private_key_file = os.path.join(_g_plaintext_key_dir, private_key_name)
    public_key_name = private_key_name + ".pub"
    public_key_file = os.path.join(_g_plaintext_key_dir, public_key_name)
    mode = "400"

    ret = 0
    ret = os_util.FS.change_file_mode(private_key_file, mode)
    if (ret != 0):
        _g_logger.error("change private key mode failed: {}".format(
            os_util.translate_linux_err_code(ret)))
        return ret

    ret = os_util.FS.change_file_mode(public_key_file, mode)
    if (ret != 0):
        _g_logger.error("change public key mode failed: {}".format(
            os_util.translate_linux_err_code(ret)))
        return ret
    return 0


if __name__ == "__main__":
    short_options = "erdhi:p:"
    required_list = ["-i", "-p"]
    ret = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], shortopts=short_options)
    except getopt.GetoptError as err:
        _g_logger.error(str(err))
        usage()
        sys.exit(errno.EINVAL)

    is_enc_mode = False
    password = ""
    in_file_path = ""
    out_file_path = ""
    for opt, arg in opts:
        if (opt == "-h"):
            usage()
            sys.exit(0)
        elif (opt == "-r"):
            _g_is_dry_run = True
        elif (opt == "-d"):
            _g_is_debug = True
        elif (opt == "-e"):
            is_enc_mode = True
        elif (opt == "-i"):
            in_file_path = os.path.abspath(arg)
            required_list.remove(opt)
        elif (opt == "-p"):
            password = arg
            required_list.remove(opt)
        else:
            _g_logger.error("wrong opt")
            usage()
            sys.exit(errno.EINVAL)
    setup.init_dry_run_debug_flag(is_dry_run=_g_is_dry_run,
                                  is_debug=_g_is_debug)

    if (len(required_list) > 0):
        _g_logger.error("missing required parameter {}".format(required_list))
        sys.exit(errno.EINVAL)

    if (is_enc_mode):
        ret = enc_key_to_cipher_dir(in_file_path, pwd=password)
        if (ret != 0):
            _g_logger.error("enc key failed: {}".format(
                os_util.translate_linux_err_code(ret)))
            sys.exit(ret)
        sys.exit(0)
    else:
        ret = dec_key_to_plaintext_dir(in_file_path, pwd=password)
        if (ret != 0):
            _g_logger.error("dec key failed: {}".format(
                os_util.translate_linux_err_code(ret)))
            sys.exit(ret)
        ret = change_key_file_mode(in_file_path)
        if (ret != 0):
            _g_logger.error("change key file mod failed: {}".format(
                os_util.translate_linux_err_code(ret)))
            sys.exit(ret)
    sys.exit(0)
