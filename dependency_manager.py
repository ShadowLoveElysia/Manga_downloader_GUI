import os
import importlib.metadata
import re
import sys # Added for sys.executable

class DependencyManager:
    def __init__(self):
        """Initializes the DependencyManager."""
        # No logger needed here, pure logic

    def get_requirements_path(self, project_root_dir):
        """Constructs and returns the full path to requirements.txt in the project root."""
        if not project_root_dir or not os.path.isdir(project_root_dir):
            # print(f"错误: 无效的项目根目录提供给 get_requirements_path: {project_root_dir}", file=sys.stderr)
            return None
        return os.path.join(project_root_dir, "requirements.txt") # Assuming requirements.txt is in the root

    def parse_requirement_line(self, line):
        """Parses a single line from requirements.txt.
        Returns a tuple (package_name, operator, version_spec) or None if invalid.
        Simplified for common cases like package==version, package>=version, package.
        """
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('-'): # Ignore comments, empty lines, and options
            return None

        # Regex to capture package name, operator, and version
        match = re.fullmatch(r'([a-zA-Z0-9_\-\.]+)\s*([><=!~]=?|==)?\s*([a-zA-Z0-9\._\-\+\*]*)?' , line)
        if match:
            name = match.group(1)
            op = match.group(2)
            version = match.group(3)

            if not op and version: # Handles cases like 'package1.0' which are invalid without operator
                 # Check for direct refs if needed, but for simplicity, basic format only
                return None # Invalid format

            return name, op, version if version else None
        return None

    def check_dependencies(self, requirements_file_path):
        """
        Checks installed packages against a requirements.txt file.
        Returns a dictionary summarizing the status and details.
        """
        if not requirements_file_path or not os.path.exists(requirements_file_path):
            # print(f"错误: requirements 文件路径无效或不存在: {requirements_file_path}", file=sys.stderr)
            return {
                "all_ok": False, "all_missing": False, "some_missing": False, "version_mismatch": False,
                "error": "Requirements file not found", "details": {},
                "missing_packages_info": [], "mismatch_packages_info": []
            }

        results_details = {}
        all_ok_flag = True
        any_missing_flag = False
        any_mismatch_flag = False
        missing_packages_list = []
        mismatch_packages_list = []

        try:
            with open(requirements_file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#') or line.startswith('-'):
                        continue

                    parsed_req = self.parse_requirement_line(line)
                    if not parsed_req:
                        # print(f"警告: 无法解析 requirements 文件中的行 {line_num}: '{line}'", file=sys.stderr)
                        all_ok_flag = False
                        results_details[f"unparsed_line_{line_num}"] = {
                            "original_line": line, "required": "N/A", "installed": "N/A", "status": "Parse Error"
                        }
                        continue

                    pkg_name, req_op, req_version_str = parsed_req

                    installed_version_str = "Not Found"
                    current_pkg_status = ''
                    try:
                        installed_version_str = importlib.metadata.version(pkg_name)
                        if req_version_str:
                            if req_op == "==":
                                if installed_version_str == req_version_str:
                                    current_pkg_status = 'OK'
                                else:
                                    current_pkg_status = 'Mismatch'
                                    any_mismatch_flag = True
                                    all_ok_flag = False # If any mismatch, overall not OK
                                    mismatch_packages_list.append({
                                        "name": pkg_name,
                                        "required": f"{req_op}{req_version_str}",
                                        "installed": installed_version_str,
                                        "original_line": line
                                    })
                            elif req_op and req_version_str:
                                # Simplified check for other operators: just check if installed
                                # print(f"提示: 依赖 '{pkg_name}' 使用了复杂比较符 ({req_op}{req_version_str})。已安装版本: {installed_version_str}. 暂标记为OK（未进行严格版本范围检查）。", file=sys.stderr)
                                current_pkg_status = 'OK' # Assume OK if installed for complex ops
                            else:
                                current_pkg_status = 'OK' # No version specified, just check if installed
                        else:
                             current_pkg_status = 'OK' # No version specified, just check if installed

                    except importlib.metadata.PackageNotFoundError:
                        current_pkg_status = 'Missing'
                        any_missing_flag = True
                        all_ok_flag = False # If any missing, overall not OK
                        missing_packages_list.append({"name": pkg_name, "original_line": line})
                    except Exception as e:
                        # print(f"错误: 检查包 '{pkg_name}' 时出错: {e}", file=sys.stderr)
                        current_pkg_status = 'Check Error'
                        all_ok_flag = False # If any error, overall not OK

                    results_details[pkg_name] = {
                        "original_line": line,
                        "required": f"{req_op or ''}{req_version_str or 'any'}",
                        "installed": installed_version_str,
                        "status": current_pkg_status
                    }

            final_status = {
                "all_ok": all_ok_flag,
                "all_missing": not all_ok_flag and any_missing_flag and not any_mismatch_flag and not any([p['status'] == 'Check Error' for p_name, p in results_details.items() if not p_name.startswith('unparsed_line')]),
                "some_missing": any_missing_flag,
                "version_mismatch": any_mismatch_flag,
                "error": None,
                "details": results_details,
                "missing_packages_info": missing_packages_list,
                "mismatch_packages_info": mismatch_packages_list
            }
            if not results_details: # Handle empty requirements.txt
                 final_status["all_missing"] = False
                 final_status["all_ok"] = True

            return final_status

        except IOError as e:
            # print(f"错误: 读取 requirements 文件失败: {e}", file=sys.stderr)
            return {"all_ok": False, "all_missing": False, "some_missing": False, "version_mismatch": False,
                    "error": f"Failed to read requirements file: {e}", "details": {},
                    "missing_packages_info": [], "mismatch_packages_info": []}
        except Exception as e:
            # print(f"错误: 检查依赖时发生意外错误: {e}", file=sys.stderr)
            return {"all_ok": False, "all_missing": False, "some_missing": False, "version_mismatch": False,
                    "error": f"Unexpected error during dependency check: {e}", "details": {},
                    "missing_packages_info": [], "mismatch_packages_info": []}

    # Note: Installation logic (running pip) will be handled in MainWindow using QProcess

# Example Usage (for testing purposes, will print to console)
if __name__ == '__main__':
    manager = DependencyManager()

    # Create a dummy requirements.txt for testing
    dummy_req_content = """
# This is a comment
selenium==4.8.2
Pillow>=9.0.0
undetected-chromedriver
requests==99.99.99 # Will likely be a mismatch
non_existent_package_xyz
    """
    test_req_path = "./temp_requirements_manga.txt"
    try:
        with open(test_req_path, "w") as f:
            f.write(dummy_req_content)

        print(f"--- 正在检查依赖: {test_req_path} ---")
        results = manager.check_dependencies(test_req_path)

        if results["error"]:
            print(f"检查时发生错误: {results['error']}")
        else:
            print("\n依赖检查结果:")
            for pkg, info in results["details"].items():
                 print(f"  包: {pkg:<25} 要求: {info['required']:<15} 已安装: {info['installed'] if info['installed'] != 'Not Found' else 'N/A':<15} 状态: {info['status']}")

            print("\n总结状态:")
            print(f"  所有OK: {results['all_ok']}")
            print(f"  全部缺失: {results['all_missing']}")
            print(f"  部分缺失: {results['some_missing']}")
            print(f"  版本不匹配: {results['version_mismatch']}")
            print(f"  缺失列表: {results['missing_packages_info']}")
            print(f"  不匹配列表: {results['mismatch_packages_info']}")

    finally:
        # Clean up dummy file
        if os.path.exists(test_req_path):
            os.remove(test_req_path)
