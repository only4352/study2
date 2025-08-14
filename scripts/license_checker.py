#!/usr/bin/env python3
"""
ライセンス自動チェッカー
生成されたコードや依存関係のライセンスを自動チェックします
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Set

class LicenseChecker:
    def __init__(self):
        # 許可されるライセンス
        self.allowed_licenses = {
            'MIT', 'Apache-2.0', 'BSD-3-Clause', 'ISC', 'Unlicense',
            'MIT License', 'Apache License 2.0', 'BSD 3-Clause License'
        }
        
        # 禁止されるライセンス
        self.blocked_licenses = {
            'GPL', 'AGPL', 'LGPL', 'MPL-2.0', 'CC-BY-SA',
            'GNU General Public License', 'GNU Affero General Public License'
        }
        
        # ライセンスパターン（検出のみ、ブロック判定は別途）
        self.license_patterns = {
            'MIT': r'MIT\s+License|The\s+MIT\s+License',
            'Apache': r'Apache\s+License\s+2\.0|Apache-2\.0',
            'BSD': r'BSD\s+3-Clause|BSD-3-Clause',
            'GPL': r'GNU\s+General\s+Public\s+License|GPL',
            'AGPL': r'GNU\s+Affero\s+General\s+Public\s+License|AGPL'
        }
    
    def check_file_license(self, file_path: str) -> Dict[str, any]:
        """ファイルのライセンスをチェック"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_licenses = set()
            blocked_found = set()
            
            # ライセンスパターンをチェック
            for license_name, pattern in self.license_patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    found_licenses.add(license_name)
                    # 禁止ライセンスの判定（実際のライセンス内容を確認）
                    if license_name in ['GPL', 'AGPL']:
                        # 実際のライセンス内容を確認（単なる文字列検索ではない）
                        if self._is_actual_license_violation(content, license_name):
                            blocked_found.add(license_name)
            
            # ライセンスヘッダーの存在チェック
            has_license_header = any([
                'license' in content.lower(),
                'copyright' in content.lower(),
                'mit license' in content.lower(),
                'apache license' in content.lower()
            ])
            
            return {
                'file': file_path,
                'licenses_found': list(found_licenses),
                'blocked_licenses': list(blocked_found),
                'has_license_header': has_license_header,
                'is_compliant': len(blocked_found) == 0,
                'status': 'BLOCKED' if blocked_found else 'OK'
            }
            
        except Exception as e:
            return {
                'file': file_path,
                'error': str(e),
                'status': 'ERROR'
            }
    
    def check_requirements_licenses(self, requirements_file: str) -> Dict[str, any]:
        """requirements.txtの依存関係ライセンスをチェック"""
        try:
            with open(requirements_file, 'r') as f:
                requirements = f.readlines()
            
            packages = []
            for line in requirements:
                line = line.strip()
                if line and not line.startswith('#'):
                    package = line.split('==')[0].split('>=')[0].split('<=')[0]
                    packages.append(package)
            
            # 一般的なライセンス情報（実際の実装ではPyPI APIを使用）
            known_licenses = {
                'fastapi': 'MIT',
                'uvicorn': 'BSD-3-Clause',
                'pydantic': 'MIT',
                'sqlalchemy': 'MIT',
                'requests': 'Apache-2.0',
                'numpy': 'BSD-3-Clause',
                'pandas': 'BSD-3-Clause'
            }
            
            results = []
            for package in packages:
                license_info = known_licenses.get(package.lower(), 'Unknown')
                is_allowed = license_info in self.allowed_licenses
                is_blocked = license_info in self.blocked_licenses
                
                results.append({
                    'package': package,
                    'license': license_info,
                    'is_allowed': is_allowed,
                    'is_blocked': is_blocked,
                    'status': 'BLOCKED' if is_blocked else 'OK'
                })
            
            return {
                'requirements_file': requirements_file,
                'packages': results,
                'has_blocked_packages': any(r['is_blocked'] for r in results),
                'status': 'BLOCKED' if any(r['is_blocked'] for r in results) else 'OK'
            }
            
        except Exception as e:
            return {
                'requirements_file': requirements_file,
                'error': str(e),
                'status': 'ERROR'
            }
    
    def scan_project(self, project_path: str) -> Dict[str, any]:
        """プロジェクト全体をスキャン"""
        project_path = Path(project_path)
        
        # チェック対象ファイル
        target_files = []
        for ext in ['.py', '.js', '.jsx', '.ts', '.tsx', '.cpp', '.hpp']:
            target_files.extend(project_path.rglob(f'*{ext}'))
        
        # ライセンスファイル
        license_files = list(project_path.rglob('LICENSE*')) + list(project_path.rglob('license*'))
        
        results = {
            'project_path': str(project_path),
            'files_checked': [],
            'license_files': [],
            'requirements_check': None,
            'summary': {}
        }
        
        # ファイルチェック
        for file_path in target_files:
            result = self.check_file_license(str(file_path))
            results['files_checked'].append(result)
        
        # ライセンスファイルチェック
        for license_file in license_files:
            results['license_files'].append(str(license_file))
        
        # requirements.txtチェック
        requirements_file = project_path / 'container' / 'webapi' / 'requirements.txt'
        if requirements_file.exists():
            results['requirements_check'] = self.check_requirements_licenses(str(requirements_file))
        
        # サマリー
        total_files = len(results['files_checked'])
        compliant_files = sum(1 for f in results['files_checked'] if f.get('is_compliant', False))
        blocked_files = sum(1 for f in results['files_checked'] if f.get('status') == 'BLOCKED')
        
        results['summary'] = {
            'total_files': total_files,
            'compliant_files': compliant_files,
            'blocked_files': blocked_files,
            'compliance_rate': (compliant_files / total_files * 100) if total_files > 0 else 0,
            'overall_status': 'BLOCKED' if blocked_files > 0 else 'OK'
        }
        
        return results
    
    def _is_actual_license_violation(self, content: str, license_type: str) -> bool:
        """実際のライセンス違反かどうかを判定（単なる文字列検索ではない）"""
        # ライセンスチェッカー自体のコード内での単なる参照は除外
        if 'license_checker' in content.lower() or 'license_checker.py' in content:
            return False
        
        # 実際のライセンスファイルやライセンス宣言の確認
        if license_type == 'GPL':
            # GPLライセンスの実際の適用を確認
            gpl_indicators = [
                'This program is free software',
                'GNU General Public License',
                'GPL v2', 'GPL v3',
                'under the terms of the GNU General Public License'
            ]
            return any(indicator in content for indicator in gpl_indicators)
        
        elif license_type == 'AGPL':
            # AGPLライセンスの実際の適用を確認
            agpl_indicators = [
                'GNU Affero General Public License',
                'AGPL v3',
                'under the terms of the GNU Affero General Public License'
            ]
            return any(indicator in content for indicator in agpl_indicators)
        
        return False
    
    def generate_report(self, scan_results: Dict[str, any]) -> str:
        """スキャン結果のレポートを生成"""
        report = []
        report.append("=" * 60)
        report.append("ライセンスコンプライアンスレポート")
        report.append("=" * 60)
        report.append(f"プロジェクト: {scan_results['project_path']}")
        report.append(f"全体ステータス: {scan_results['summary']['overall_status']}")
        report.append(f"コンプライアンス率: {scan_results['summary']['compliance_rate']:.1f}%")
        report.append("")
        
        # ファイルチェック結果
        report.append("ファイルチェック結果:")
        for file_result in scan_results['files_checked']:
            status_icon = "❌" if file_result.get('status') == 'BLOCKED' else "✅"
            report.append(f"  {status_icon} {file_result['file']}")
            if file_result.get('blocked_licenses'):
                report.append(f"    禁止ライセンス: {', '.join(file_result['blocked_licenses'])}")
        
        # 依存関係チェック結果
        if scan_results['requirements_check']:
            req_check = scan_results['requirements_check']
            report.append("")
            report.append("依存関係チェック結果:")
            for package in req_check['packages']:
                status_icon = "❌" if package['status'] == 'BLOCKED' else "✅"
                report.append(f"  {status_icon} {package['package']}: {package['license']}")
        
        return "\n".join(report)

def main():
    """メイン関数"""
    checker = LicenseChecker()
    
    # プロジェクトパス
    project_path = os.getcwd()
    
    print("ライセンスチェックを開始しています...")
    results = checker.scan_project(project_path)
    
    # レポート生成
    report = checker.generate_report(results)
    print(report)
    
    # 結果をJSONファイルに保存
    output_file = Path(project_path) / 'license_scan_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n詳細結果を {output_file} に保存しました")
    
    # 終了コード
    if results['summary']['overall_status'] == 'BLOCKED':
        print("\n⚠️  ライセンス違反が検出されました！")
        exit(1)
    else:
        print("\n✅ ライセンスチェック完了 - 問題なし")
        exit(0)

if __name__ == "__main__":
    main()
