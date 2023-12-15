import os
from detect_llm_api_keys.key_detector import APIKeyDetector


this_file_abs_path = os.path.abspath(__file__)
this_dir_abs_path = os.path.dirname(this_file_abs_path)

parent_dir = os.path.dirname(this_dir_abs_path)
package_dir = os.path.join(parent_dir, "detect_llm_api_keys")

main_script = os.path.join(package_dir, "__main__.py")
test_file_dir = os.path.join(this_dir_abs_path, "test_files")


def test_APIKeyDetector_positive():
    pos_results = APIKeyDetector.check_file(os.path.join(test_file_dir, "foobar.py"))
    assert pos_results


def test_APIKeyDetector_negative():
    neg_results = APIKeyDetector.check_file(os.path.join(test_file_dir, "foobar3.py"))
    assert not neg_results


# def test_APIKeyDetector_subprocess():
#     pos_cmd = [
#         "python",
#         main_script,
#         os.path.join(test_file_dir, "foobar.py"),
#         os.path.join(test_file_dir, "foobar2.py"),
#     ]
#     with pytest.raises(subprocess.CalledProcessError):
#         subprocess.run(
#             pos_cmd,
#             shell=True,
#             check=True,
#             text=True,
#             stderr=subprocess.STDOUT,
#             universal_newlines=True,
#         )
#
#     neg_cmd = [
#         "python",
#         main_script,
#         os.path.join(test_file_dir, "foobar3.py"),
#     ]
#     subprocess.run(
#         neg_cmd,
#         shell=True,
#         check=True,
#         text=True,
#         stderr=subprocess.STDOUT,
#         universal_newlines=True,
#     )
