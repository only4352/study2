#!/usr/bin/env python3
"""
ライセンスチェッカーのテストスクリプト
MIT License

Copyright (c) 2024 Study2 Project
"""

import sys
import os
from pathlib import Path

# ライセンスチェッカーをインポート
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from license_checker import LicenseChecker

def test_license_checker():
    """ライセンスチェッカーのテスト"""
    print("🧪 ライセンスチェッカーのテストを開始...")
    
    # ワークスペースパスを取得
    workspace_path = Path(__file__).parent.parent
    
    # ライセンスチェッカーを作成
    checker = LicenseChecker(str(workspace_path))
    
    print(f"📁 ワークスペース: {workspace_path}")
    
    # ステージングされたファイルのチェックテスト
    print("\n📋 ステージングされたファイルのチェックテスト:")
    staged_results = checker.scan_staged_files()
    checker.print_report(staged_results, staged_only=True)
    
    # ワークスペース全体のチェックテスト
    print("\n🌐 ワークスペース全体のチェックテスト:")
    workspace_results = checker.scan_workspace()
    checker.print_report(workspace_results)
    
    print("\n✅ テスト完了")

if __name__ == "__main__":
    test_license_checker()
