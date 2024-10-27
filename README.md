# ColorPrinter-for-Python  
  
**コマンドライン上でPythonプログラムを実行する際、文字の色や背景色をエスケープシーケンスにより色付けする機能を、print関数としてオーバーライドする、Pythonのライブラリです。**  

## 使用準備1 - 直接ファイルからライブラリをインストールする  
1. レポジトリ内にある、`ColorPrinter-x.x.x-py3-none-any.whl`ファイルをダウンロードする。(distディレクトリにある)    
2. 1でダウンロードしたファイルの絶対パスをコピーしておく。  
   例：
   `C:\Users\xxxxxx\Downloads\ColorPrinter-x.x.x-py3-none-any.whl`    
4. コマンドラインに、以下のコマンドを入力する。  
   例：コマンドプロンプト or Powershell
   ```bacth
   pip install C:\Users\xxxxxx\Downloads\ColorPrinter-x.x.x-py3-none-any.whl
   ```    
5. インストールが完了したら、使用できるようになる。  
  
## 使用準備2 - PyPlからインストールする    
1. コマンドラインに、以下のコマンドを入力する。  
   例：コマンドプロンプト or Powershell
   ```batch
   pip install ColorPrinter
   ```
     
   **注意**
   **pipコマンドでパッケージをインストールする際、同じパッケージ名が存在する等の理由により、以下のような警告が出ることがあります。**  
   **この場合、Authorが'OnieMikel'であるものを選択してください。**

2. インストールが完了したら、使用できるようになる。
  
  

## 使用方法  
1. 使用したいPythonスクリプトファイル内に、以下の文を記述する。  
   ```python
   from ColorPrinter import print
   ```
2. 使用したいPythonスクリプトファイルを実行すると、print関数がオーバーライドされ、色指定をしたprint出力が行えるようになる。  
  
  
### 色指定の仕方  
文字列内（クォーテーションで区切られた内部）において、色指定したい箇所を以下のように囲んで指定する。  
  
print関数で指定する文字列において（クォーテーションで区切った部分において）、フォーマット文字列を指定するときのように、波カッコ`{}`で`{fore:red}`や`{underline}`といったようなタグを、指定したい箇所に挿入するだけで、様々な文字の装飾を加えることができる。  
  
+ ### 文法  
   ```python
   print(" ... {fore:<color>/back:<color>/bold/italic/underline} ... {...} ... {end (fore/back/bold/italic/underline) ...} ... {...}")
   ```  
+ ### タグの種類  
  
   | タグ        | 名称                          | 
   | :---------: | :--------------------------: | 
   | `fore`      | フォアグラウンドカラー (前景色) | 
   | `back`      | バックグラウンドカラー (背景色) | 
   | `bold`      | ボールド体 (太字)              | 
   | `italic`    | イタリック体 (斜字)            | 
   | `underline` | アンダーライン (下線)          |
   |             |                              |
   | `end`       | 終了タグ                      |  

+ ### 指定できる色の種類  
   + **色名**で指定  

      | 色コード   | 色名         | 対応するRGBAコード (r, g, b, a) | 
      | :-------: | :----------: | :-----------------------------: | 
      | `black`   | 黒           | (  0,   0,   0,   1)            | 
      | `white`   | 白           | (255, 255, 255,   1)            | 
      | `red`     | 赤           | (255,   0,   0,   1)            | 
      | `green`   | 緑           | (  0, 255,   0,   1)            | 
      | `blue`    | 青           | (  0,   0, 255,   1)            | 
      | `yellow`  | 黄色         | (255, 255,   0,   1)            | 
      | `cyan`    | シアン       | (  0, 255, 255,   1)            | 
      | `magenta` | マゼンタ     | (255,   0, 255,   1)            | 
      | `gray`    | グレー       | (128, 128, 128,   1)            | 
      | `skyblue` | スカイブルー | (135, 206, 235,   1)            |  
     
   + **RGBAコード**で指定  
      `<red>`、`<green>`、`<blue>`値は、0~255の実数値で指定。  
      `<alpha>`値は0~1の実数値で指定。ただし、省略可能。  
        
      文法：  
      `rgba(<red>, <green>, <blue>(, <alpha>))`  
        
      例：
      `rgba(255, 0, 0, 255)`  
      (この場合、`red`と同じ)  
        
      >**注意**  
      **`<alpha>`値は対応している場合が少なく、基本的に指定しても機能しないことが多い。<br>そのため、基本的には指定しないことを推奨する。<br>それでも指定したい場合、`<alpha>`値を`1`と指定すること。そうでないと、色が適切に適用されない。**

+ 各タグの説明  
   + ### `fore`  
      フォアグラウンドカラー (前景色) の色を指定する。
      `fore`の後にコロン`:`をつけ、そのあとに色コードまたはrgbaを記述する。
      `:`の前後にはスペースがどれだけあっても構わない。
      記述例：`fore:red`、`fore:rbga(255, 0, 0)`  
         
      実行例：  
      ```python
      print("This is a {fore:green}green text." # green text. の前景色が緑色になる
      ```  
      ![image](https://github.com/user-attachments/assets/6dd05ff3-e84e-4089-a5f0-00fb6a8200d2)


   + ### `back`
      バックグラウンドカラー (背景色) の色を指定する。
      `back`の後にコロン`:`をつけ、そのあとに色コードまたはrgbaを記述する。
      `:`の前後にはスペースがどれだけあっても構わない。
      記述例：`back:red`、`back:rbga(125, 255, 0)`  
         
      実行例：
     ```python
     print("The background color is {back:red}red.") # red. 部分の背景色が赤色になる
     ```  
     ![image](https://github.com/user-attachments/assets/61fd6cf6-34f2-4d4b-8652-a04ef01e7c9f)


   + ### `bold`  
      ボールド体 (太字) の指定をする。  
      記述例：`bold`  
         
      実行例：
     ```python
     print("This is a {bold}text.") # text. が太字になる
     ```
     ![image](https://github.com/user-attachments/assets/d311d27c-e3a0-4fe3-81f4-0a55709b54dc)


   + ### `itaric`  
      イタリック体 (斜字) の指定をする。
      記述例：`italic` 
         
      実行例：
     ```python  
     print("This is a {italic}text.") # text. が斜字になる
     ```
     ![image](https://github.com/user-attachments/assets/e63efae9-1646-40ca-b496-d7130e6969f1)

      
   + ### `underline`  
      アンダーライン (下線) の指定をする。  
      記述例：`underline`  
         
      実行例：
     ```python
     print("This is a {underline}text.") # text. に下線がつく
     ```  
     ![image](https://github.com/user-attachments/assets/e74604f6-0fab-4651-8df9-e7d545101b66)

     

   + ### `end`
      タグの終了箇所を指定する。  
      記述例：`end`、`end fore`  
         
      `end`のみを指定すると、すべてのスタイルがリセットされ、デフォルト表示に戻る。  
      実行例：
     ```python
     print("{fore:red}red{end} text and {fore:black, back:white}black{end} text.") # redが赤色、blackについては、前景色が黒色、背景色が白色で表示される。
     ```  
     ![image](https://github.com/user-attachments/assets/6d3e4ff3-a9eb-4dbd-85ce-28a6a12c5f87)



      `end`にタグの引数を持たせた場合、そのタグのスタイルのみをリセットすることができる。なお、この引数は複数指定できる。  
      実行例：
     ```python
     print("{fore:red back:white}red{end fore}, {fore:blue}blue{end fore}{fore:black, italic}... but the WHITE background.") # 文字列全体の背景が白色で、redが赤色、blueが青色、そしてそれ以降の文字がイタリック体で表示される。
     ```  
     ![image](https://github.com/user-attachments/assets/5a1565ac-6058-4aa7-ab95-c8bb2793c49e)

     ただし、同じタグ内で`end`と併用して新たなスタイルを適用すると、`end`が無視される。
     実行例：
     ```python
     print("{fore:red, back:white}red{end fore}, {fore:blue}blue{italic, end fore}... but the WHITE background.") # 上記と同じ結果を出力すると思われるはずだが、endが無視され、前景色が青色のまま、italicのみがitalicに適用されている。
     ```
     ![image](https://github.com/user-attachments/assets/6e13532b-acec-4fff-ad4d-62fb27dd3aeb)


   >**注意<br>タグ指定するとき、タグやその値同士にスペースがいくつ入っていても、動作に全く問題はない。<br>しかしながら、<ins>タグ自体や色コード自体にスペースが入っていると、適切に動作しない。</ins>**
   >**実行例：**
   >```python
   >print("{ fore  :    red  }Hello, { italic  fore       :  rgba    (125,  211, 32)  }world!") # スペースがどれだけあっても、Hello, は赤色、world! は青色で表示される。
   >```  
   >![image](https://github.com/user-attachments/assets/4c5c91c0-a9b9-4a10-a3a1-99c82b68c39f)
   >
   >```python
   >print("{for e:re d}Hello, {ita lic f ore:rgb a(125,211,32)}world!") # この場合、foreやitalicといったコマンドが認識できないため、スタイルが適用されない
   >```
   >![image](https://github.com/user-attachments/assets/0ccaa6c5-0c61-404b-ac77-cde67996bac8)

