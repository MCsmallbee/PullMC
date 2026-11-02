<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="img/logo_dark.svg">
    <img alt="PullMC Logo" src="img/logo.svg" width="100">
  </picture>
<h1>PullMC</h1>

**日本語** &nbsp;|&nbsp; [简体中文](../README.md) &nbsp;|&nbsp; [English](README_EN.md)

<p>軽量・クリーンな Minecraft Java版 バージョンダウンロードツール</p>

[![主要言語](https://img.shields.io/github/languages/top/MCsmallbee/PullMC)](https://github.com/MCsmallbee/PullMC)
[![スター数](https://img.shields.io/github/stars/MCsmallbee/PullMC?label=%E3%82%B9%E3%82%BF%E3%83%BC%E6%95%B0)](https://github.com/MCsmallbee/PullMC/stargazers)
[![ライセンス](https://img.shields.io/github/license/MCsmallbee/PullMC?label=%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3%E3%82%B9)](https://github.com/MCsmallbee/PullMC/blob/main/LICENSE)
[![最新リリース日](https://img.shields.io/github/release-date-pre/MCsmallbee/PullMC?label=%E6%9C%80%E6%96%B0%E3%83%AA%E3%83%AA%E3%83%BC%E3%82%B9%E6%97%A5)](https://github.com/MCsmallbee/PullMC/releases)
[![言語数](https://img.shields.io/github/languages/count/MCsmallbee/PullMC?label=%E8%A8%80%E8%AA%9E%E6%95%B0)](https://github.com/MCsmallbee/PullMC)
[![リポジトリサイズ](https://img.shields.io/github/repo-size/MCsmallbee/PullMC?label=%E3%83%AA%E3%83%9D%E3%82%B8%E3%83%88%E3%83%AA%E3%82%B5%E3%82%A4%E3%82%BA)](https://github.com/MCsmallbee/PullMC)


</div>

> [!IMPORTANT]
> **重要**：本プロジェクト内の大量のコードは **Vibe Coding（バイブコーディング）** 方式で書かれています。
>
> このようなプロジェクトを嫌う場合は、このプロジェクトを無視してください。ありがとうございます。

> [!NOTE]
> 本プロジェクトの主要機能は**開発中**です。現在は基本的な UI フレームワークのみ完成しています。
>
> **お楽しみに！**

## 📖 プロジェクト概要

PullMC は、ゲームのバージョンとファイルをより軽量で透明性の高い方法で管理したいプレイヤー向けの、オープンソースかつ非公式の Minecraft Java Edition ダウンロード・導入ツールです。

主に次の3つを担当します：

- バージョンメタデータの取得
- ゲームファイルのダウンロードと検証
- 指定したディレクトリへのファイル配置

PullMC はゲームアカウント、ランチャー、マルチプレイサービスを提供せず、ゲームリソースのホストやミラーリングも行いません。デスクトップアプリは Python、PySide6、QML、RinUI で構築されており、簡体字中国語・繁体字中国語・英語・日本語に対応し、Windows のテーマに追従します。

現在は `base` ステージです。デスクトップ UI、初回セットアップ、設定は完成していますが、バージョンライブラリ、ダウンロード、検証、配置は開発中です。

## 🗺️ やることリスト

- [x] 基本ウィンドウUIレイアウトの実装
- [x] 設定ページ、概要ページ、多言語対応とバージョン命名
- [ ] Minecraftバージョンマニフェストの取得とバージョンライブラリ
- [ ] ゲームファイルのダウンロード、検証と展開
- [ ] ダウンロードタスクキューと進捗管理
- [ ] ダウンロードソース、ミラーとプロキシ設定
- [ ] ModローダーとModのダウンロード
- [ ] Modパックインストールのサポート

## ⚠️ 免責事項

PullMC は、Minecraft Java Edition のダウンロードと導入を行うオープンソースツールです。バージョンメタデータの取得、ゲームファイルのダウンロード、ローカルファイルの検証のみを行い、ゲームアカウント、サーバー、マルチプレイサービスは提供しません。

- 本プロジェクトは、ゲームリソースの配信サイトを運営・ホストしておらず、ゲームファイルのミラーリングも行いません。すべてのダウンロード要求は、お使いの端末から選択した配信元（Mojang の公式ソース、BMCLAPI などの公開ミラー、またはローダーの公式ソース）へ直接送信され、指定したローカルディレクトリに保存されます。
- 本プロジェクトは、Microsoft、Mojang Studios、およびその関連会社・代理店と提携、協賛、承認、委託の関係にありません。
- Minecraft は Mojang Studios の商標です。本プロジェクトの名称は互換性の説明のみに使用しており、Mojang Studios による承認を意味するものではありません。
- 本プロジェクトを使用する前に、公式チャネルを通じて Minecraft: Java Edition のライセンスを合法的に取得し、適用されるエンドユーザーライセンス契約を遵守してください。
- 本プロジェクトは「現状のまま」提供され、第三者配信元の可用性、安定性、安全性について一切保証しません。使用に伴うリスクは利用者自身が負担するものとします。

## ⚖️ ライセンス

Copyright (c) 2026 MCsmallbee

本プロジェクトは MIT ライセンスを採用しています。詳細は [LICENSE](../LICENSE) ファイルをご覧ください。

一言で言えば：本プロジェクトのコードを自由に使用、複製、改変、配布できますが、著作権表示を保持する必要があり、作者は一切の責任を負いません。

## ⭐ スター履歴

<a href="https://www.star-history.com/?repos=mcsmallbee%2Fpullmc&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=mcsmallbee/pullmc&type=date&theme=dark&legend=bottom-right" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=mcsmallbee/pullmc&type=date&legend=bottom-right" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=mcsmallbee/pullmc&type=date&legend=bottom-right" />
 </picture>
</a>
