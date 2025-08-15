#!/usr/bin/env python3
"""
商用利用制限チェッカー
MIT License

Copyright (c) 2024 Study2 Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
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

class LicenseChecker:
    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.issues = []
        self.file_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.cpp', '.c', '.h', '.hpp',
            '.java', '.kt', '.go', '.rs', '.php', '.rb', '.cs', '.swift'
        }
        
    def check_file(self, file_path: Path) -> List[Dict]:
        """個別ファイルのライセンスをチェック"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # ライセンスチェッカー自体は除外
            if 'license_checker.py' in str(file_path):
                return issues
                
            # ライセンスヘッダーのチェック
            if not self._has_license_header(content):
                issues.append({
                    'type': 'warning',
                    'message': 'ライセンスヘッダーが見つかりません',
                    'file': str(file_path)
                })
            
            # 禁止されたライセンスのチェック
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
    
    def print_report(self, results: Dict[str, List[Dict]]):
        """結果レポートを出力"""
        print("=" * 60)
        print("商用利用制限チェッカーレポート")
        print("=" * 60)
        
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
            sys.exit(1)
        else:
            print("✅ 商用利用可能なコードのみが検出されました")

def main():
    """メイン関数"""
    workspace_path = sys.argv[1] if len(sys.argv) > 1 else "."
    
    checker = LicenseChecker(workspace_path)
    results = checker.scan_workspace()
    checker.print_report(results)

if __name__ == "__main__":
    main()
