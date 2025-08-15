#!/usr/bin/env python3
"""
商用利用制限チェッカー
MIT License

Copyright (c) 2024 Study2 Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import re
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Set

# 許可されるライセンス
ALLOWED_LICENSES = {
    'MIT', 'Apache-2.0', 'BSD-3-Clause', 'ISC', 'Unlicense',
    'MIT License', 'Apache License 2.0', 'BSD License', 'ISC License'
}

# 禁止されるライセンス
BLOCKED_LICENSES = {
    'GPL', 'AGPL', 'LGPL', 'MPL-2.0', 'CC-BY-SA',
    'GNU General Public License', 'GNU Affero General Public License',
    'GNU Lesser General Public License', 'Mozilla Public License'
}

# 商用利用制限を示すキーワード
COMMERCIAL_RESTRICTION_KEYWORDS = {
    'commercial use prohibited', 'non-commercial only', 'commercial license required',
    '商用利用禁止', '商用利用不可', '商用ライセンス必要'
}

# 除外するファイル・ディレクトリ
EXCLUDED_PATTERNS = {
    '.git/', 'node_modules/', '__pycache__/', '.pytest_cache/',
    'build/', 'dist/', '.cache/', 'coverage/', '.coverage',
    '*.pyc', '*.pyo', '*.log', '*.tmp', '*.swp', '*.swo'
}

class LicenseChecker:
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.issues = []
        self.file_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.cpp', '.c', '.h', '.hpp',
            '.java', '.kt', '.go', '.rs', '.php', '.rb', '.cs', '.swift',
            '.json', '.toml', '.xml', '.yaml', '.yml', '.md', '.txt'
        }
        
    def should_exclude_file(self, file_path: Path) -> bool:
        """ファイルを除外すべきかチェック"""
        file_str = str(file_path)
        
        # 除外パターンのチェック
        for pattern in EXCLUDED_PATTERNS:
            if pattern in file_str:
                return True
                
        # ライセンスチェッカー自体は除外
        if 'license_checker.py' in file_str:
            return True
            
        return False
        
    def check_file(self, file_path: Path) -> List[Dict]:
        """個別ファイルのライセンスをチェック"""
        issues = []
        
        # 除外ファイルのチェック
        if self.should_exclude_file(file_path):
            return issues
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # ライセンスヘッダーのチェック（ソースコードファイルのみ）
            if file_path.suffix in ['.py', '.js', '.jsx', '.ts', '.tsx', '.cpp', '.c', '.h', '.hpp']:
                if not self._has_license_header(content):
                    issues.append({
                        'type': 'warning',
                        'message': 'ライセンスヘッダーが見つかりません',
                        'file': str(file_path)
                    })
            
            # 禁止されたライセンスのチェック（READMEファイルの説明は除外）
            if file_path.name != 'README.md':
                for blocked_license in BLOCKED_LICENSES:
                    if blocked_license.lower() in content.lower():
                        issues.append({
                            'type': 'error',
                            'message': f'禁止されたライセンスが検出されました: {blocked_license}',
                            'file': str(file_path)
                        })
            
            # 商用利用制限キーワードのチェック
            for keyword in COMMERCIAL_RESTRICTION_KEYWORDS:
                if keyword.lower() in content.lower():
                    issues.append({
                        'type': 'error',
                        'message': f'商用利用制限が検出されました: {keyword}',
                        'file': str(file_path)
                    })
            
            # 依存関係のチェック（package.json, requirements.txt等）
            if file_path.name in ['package.json', 'requirements.txt', 'Cargo.toml', 'pom.xml']:
                deps_issues = self._check_dependencies(content, file_path)
                issues.extend(deps_issues)
                
        except Exception as e:
            issues.append({
                'type': 'error',
                'message': f'ファイル読み込みエラー: {e}',
                'file': str(file_path)
            })
            
        return issues
    
    def _has_license_header(self, content: str) -> bool:
        """ライセンスヘッダーの存在をチェック"""
        # 一般的なライセンスヘッダーパターン
        license_patterns = [
            r'MIT License',
            r'Apache License',
            r'BSD License',
            r'ISC License',
            r'Unlicense',
            r'Copyright.*MIT',
            r'Copyright.*Apache',
            r'Copyright.*BSD',
            r'Copyright.*ISC'
        ]
        
        for pattern in license_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _check_dependencies(self, content: str, file_path: Path) -> List[Dict]:
        """依存関係のライセンスをチェック"""
        issues = []
        
        if file_path.name == 'package.json':
            # npmパッケージのライセンスチェック
            issues.extend(self._check_npm_dependencies(content))
        elif file_path.name == 'requirements.txt':
            # Pythonパッケージのライセンスチェック
            issues.extend(self._check_python_dependencies(content))
            
        return issues
    
    def _check_npm_dependencies(self, content: str) -> List[Dict]:
        """npm依存関係のライセンスチェック"""
        issues = []
        # 一般的に商用利用可能なnpmパッケージのライセンスチェック
        # 実際の実装では、npm registryからライセンス情報を取得する必要があります
        return issues
    
    def _check_python_dependencies(self, content: str) -> List[Dict]:
        """Python依存関係のライセンスチェック"""
        issues = []
        # 一般的に商用利用可能なPythonパッケージのライセンスチェック
        # 実際の実装では、PyPIからライセンス情報を取得する必要があります
        return issues
    
    def get_staged_files(self) -> List[Path]:
        """Gitでステージングされたファイルを取得"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
                capture_output=True, text=True, cwd=self.workspace_path
            )
            
            if result.returncode == 0:
                staged_files = result.stdout.strip().split('\n')
                return [Path(f) for f in staged_files if f.strip()]
            else:
                print(f"⚠️  Gitコマンドエラー: {result.stderr}")
                return []
                
        except Exception as e:
            print(f"⚠️  Gitコマンド実行エラー: {e}")
            return []
    
    def scan_staged_files(self) -> Dict[str, List[Dict]]:
        """ステージングされたファイルのみをスキャン"""
        staged_files = self.get_staged_files()
        
        if not staged_files:
            return {
                'errors': [],
                'warnings': [],
                'total_files_checked': 0,
                'message': 'ステージングされたファイルがありません'
            }
        
        all_issues = []
        
        for file_path in staged_files:
            full_path = self.workspace_path / file_path
            if full_path.is_file():
                file_issues = self.check_file(full_path)
                all_issues.extend(file_issues)
        
        # 結果を整理
        results = {
            'errors': [issue for issue in all_issues if issue['type'] == 'error'],
            'warnings': [issue for issue in all_issues if issue['type'] == 'warning'],
            'total_files_checked': len(staged_files)
        }
        
        return results
    
    def scan_workspace(self) -> Dict[str, List[Dict]]:
        """ワークスペース全体をスキャン"""
        all_issues = []
        
        for file_path in self.workspace_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.file_extensions:
                file_issues = self.check_file(file_path)
                all_issues.extend(file_issues)
        
        # 結果を整理
        results = {
            'errors': [issue for issue in all_issues if issue['type'] == 'error'],
            'warnings': [issue for issue in all_issues if issue['type'] == 'warning'],
            'total_files_checked': len(set(issue['file'] for issue in all_issues))
        }
        
        return results
    
    def print_report(self, results: Dict[str, List[Dict]], staged_only: bool = False):
        """結果レポートを出力"""
        if staged_only:
            print("=" * 60)
            print("ステージングされたファイルのライセンスチェック")
            print("=" * 60)
        else:
            print("=" * 60)
            print("商用利用制限チェッカーレポート")
            print("=" * 60)
        
        if 'message' in results:
            print(f"\n{results['message']}")
            return
        
        print(f"\nチェックしたファイル数: {results['total_files_checked']}")
        
        if results['errors']:
            print(f"\n❌ エラー ({len(results['errors'])}件):")
            for error in results['errors']:
                print(f"  - {error['file']}: {error['message']}")
        else:
            print("\n✅ エラーは検出されませんでした")
            
        if results['warnings']:
            print(f"\n⚠️  警告 ({len(results['warnings'])}件):")
            for warning in results['warnings']:
                print(f"  - {warning['file']}: {warning['message']}")
        else:
            print("\n✅ 警告は検出されませんでした")
            
        print("\n" + "=" * 60)
        
        if results['errors']:
            print("❌ 商用利用に問題があるコードが検出されました")
            if staged_only:
                print("コミットを中止します。問題を修正してから再度コミットしてください。")
            sys.exit(1)
        else:
            print("✅ 商用利用可能なコードのみが検出されました")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='商用利用制限チェッカー')
    parser.add_argument('--staged-files', nargs='+', help='チェックするステージングされたファイル')
    parser.add_argument('--workspace', default='.', help='ワークスペースパス')
    parser.add_argument('--staged-only', action='store_true', help='ステージングされたファイルのみチェック')
    
    args = parser.parse_args()
    
    checker = LicenseChecker(args.workspace)
    
    if args.staged_only or args.staged_files:
        # ステージングされたファイルのみチェック
        results = checker.scan_staged_files()
        checker.print_report(results, staged_only=True)
    else:
        # ワークスペース全体をチェック
        results = checker.scan_workspace()
        checker.print_report(results)

if __name__ == "__main__":
    main()
