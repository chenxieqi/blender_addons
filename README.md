# blender_addons

自作の Blender アドオンをまとめたリポジトリです。すべて Python で書いています。

A collection of Blender add-ons I've made, all written in Python.

## アドオン一覧 / Add-ons

| アドオン / Add-on | 説明 / Description |
| --- | --- |
| [Random Duplicate](random_duplicate/) | 選択したオブジェクトを、ランダムな大きさと回転で複製します。<br>Duplicates selected objects with random scale and rotation. |

---

## Random Duplicate

### 概要

選択したオブジェクトを指定した数だけ複製し、それぞれの大きさと回転をランダムに変えます。岩や草、木などをばらつきを持たせて配置したいときに便利です。

### 機能

- **複製する数**：オブジェクトごとに 1〜1000 個まで複製できます。
- **リンク複製**：メッシュデータを共有して複製します（Alt+D と同じ）。
- **大きさのランダム化**
  - 最小・最大の倍率を指定できます。
  - 「縦横比を保つ」：XYZ に同じ倍率をかけます。オフにすると軸ごとに別の倍率になります。
  - 「元の大きさに掛ける」：オフにすると、元の大きさに関係なく値をそのまま設定します。
- **回転のランダム化**
  - X・Y・Z 軸ごとにオン／オフと角度の範囲（度）を指定できます。
  - 「元の回転に足す」：オフにすると、角度をそのまま設定します。
  - オイラー角・クォータニオン・軸角度のどの回転モードにも対応しています。
- **シードを固定**：オンにすると毎回同じ結果になります。

### 動作環境

Blender 3.0 以降

### インストール

1. [`random_duplicate/random_duplicate.py`](random_duplicate/random_duplicate.py) をダウンロードします。
2. Blender で「編集 > プリファレンス > アドオン > インストール」を開き、ダウンロードしたファイルを選びます。
3. 一覧に表示された「Random Duplicate」にチェックを入れて有効にします。

### 使い方

1. オブジェクトモードで、複製したいオブジェクトを選択します。
2. 3D ビューポートで `N` キーを押してサイドバーを開き、「ランダム複製」タブを開きます。
3. 数・大きさ・回転などを設定し、「ランダム複製」ボタンを押します。
4. 複製されたオブジェクトが選択された状態になります。`Ctrl+Z` で元に戻せます。

---

### Overview

Duplicates the selected objects as many times as you specify and gives each copy a random scale and rotation. Handy for scattering rocks, grass, trees and similar objects with natural variation.

### Features

- **Count**: make 1–1000 copies of each selected object.
- **Linked duplicate**: copies share mesh data (same as Alt+D).
- **Random scale**
  - Set a minimum and maximum scale factor.
  - *Keep proportions*: use the same factor on X, Y and Z. Turn it off to randomize each axis separately.
  - *Multiply original scale*: turn it off to set the value directly, ignoring the original scale.
- **Random rotation**
  - Turn each of the X, Y and Z axes on or off and set its angle range in degrees.
  - *Add to original rotation*: turn it off to set the angle directly.
  - Works with Euler, quaternion and axis-angle rotation modes.
- **Fixed seed**: gives the same result every time.

### Requirements

Blender 3.0 or later

### Installation

1. Download [`random_duplicate/random_duplicate.py`](random_duplicate/random_duplicate.py).
2. In Blender, open *Edit > Preferences > Add-ons > Install* and select the downloaded file.
3. Tick **Random Duplicate** in the list to enable it.

### Usage

1. In Object Mode, select the objects you want to duplicate.
2. In the 3D Viewport, press `N` to open the sidebar and go to the **ランダム複製** (Random Duplicate) tab.
3. Set the count, scale, rotation and other options, then press the **ランダム複製** button.
4. The new copies are left selected. Press `Ctrl+Z` to undo.

> 注意 / Note: UI は日本語表記です。 / The add-on's UI is in Japanese.
