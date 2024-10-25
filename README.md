# ColorPrint-for-Python  

*コマンドライン上でPythonプログラムを実行する際、文字の色や背景色をエスケープシーケンスにより色付けする機能を、print関数としてオーバーライドする、Pythonのライブラリです。  

## 使用準備1 - 直接ファイルからライブラリをインストールする  
1. レポジトリ内にある、`ColorPrinter.whl`ファイルをダウンロードする。    
2. 1でダウンロードしたファイルの絶対パスをコピーしておく。  
   例：
   `C:\Users\xxxxxx\Downloads\ColorPrinter.whl`    
4. コマンドプロンプト、もしくはPowershell(Windows)やTerminal(Linux、MacOS)を立ち上げ、以下のコマンドを入力する。  
   例：
   `pip install C:\Users\xxxxxx\Downloads\ColorPrinter.whl`    
5. インストールが完了したら、使用できるようになる。  
  
## 使用準備2 - PyPlからインストールする    
1. コマンドプロンプト、もしくはPowershell(Windows)やTerminal(Linux、MacOS)を立ち上げ、以下のコマンドを入力する。    
   `pip install ColorPrint`
     
   **注意**
   **pipコマンドでパッケージをインストールする際、同じパッケージ名が存在する等の理由により、以下のような警告が出ることがあります。**  
   **この場合、Authorが'OnieMikel'であるものを選択してください。**

2. インストールが完了したら、使用できるようになる。
  
  

## 使用方法  
1. 使用したいPythonスクリプトファイル内に、以下の文を記述する。  
   `import ColorPrint`
2. 使用したいPythonスクリプトファイルを実行すると、print関数がオーバーライドされ、色指定をしたprint出力が行えるようになる。
---
