import re
import builtins  # 元のprint関数を参照するために使用

class ColorPrinter:
    # 色名とRGBA値のマッピング
    COLOR_MAP = {
        "black": (0, 0, 0, 255),
        "white": (255, 255, 255, 255),
        "red": (255, 0, 0, 255),
        "green": (0, 255, 0, 255),
        "blue": (0, 0, 255, 255),
        "yellow": (255, 255, 0, 255),
        "cyan": (0, 255, 255, 255),
        "magenta": (255, 0, 255, 255),
        "gray": (128, 128, 128, 255),
        "skyblue": (135, 206, 235, 255),
    }

    def __init__(self):
        """
        終了コードを指定
        """
        self.reset = "\033[0m"

    def set_rgba_color(self, color):
        """
        RGBAタプル (r, g, b, a) から前景色のエスケープシーケンスを生成
        
        Args:
            color (tuple): RGBAタプル (r, g, b, a)
        """
        r, g, b, a = color
        return f"\033[38;2;{r};{g};{b}m"

    def set_rgba_background(self, color):
        """
        RGBAタプル (r, g, b, a) から背景色のエスケープシーケンスを生成
        
        Args:
            color (tuple): RGBAタプル (r, g, b, a)
        """
        r, g, b, a = color
        return f"\033[48;2;{r};{g};{b}m"

    def get_color_by_name(self, name):
        """
        色名からRGBAタプルを取得
        
        Args:
            name (str): 色名
        """
        return self.COLOR_MAP.get(name.lower(), None)  # 色名を小文字に変換

    def parse_color_tag(self, tag):
        """
        {fore:<r,g,b,a>} または {back:<r,g,b,a>} の形式のタグを解析して、
        それぞれのエスケープシーケンスに変換。
        {end} タグがあれば、リセットシーケンスを返す。
        
        Args:
            tag (str): 色指定タグ
        """
        fore_match = re.match(r'{fore:(\d+),(\d+),(\d+),(\d+)}', tag)
        back_match = re.match(r'{back:(\d+),(\d+),(\d+),(\d+)}', tag)
        color_name_match = re.match(r'{(fore|back):(\w+)}', tag)

        if fore_match:
            r, g, b, a = map(int, fore_match.groups())
            return self.set_rgba_color((r, g, b, a))
        elif back_match:
            r, g, b, a = map(int, back_match.groups())
            return self.set_rgba_background((r, g, b, a))
        elif color_name_match:
            color_type, color_name = color_name_match.groups()
            color_value = self.get_color_by_name(color_name)
            if color_value:
                if color_type == "fore":
                    return self.set_rgba_color(color_value)
                elif color_type == "back":
                    return self.set_rgba_background(color_value)

        elif tag == '{end}':
            return self.reset  # リセットコードを返す
        
        return ""  # タグにマッチしなければ空文字を返す

    def print_with_color(self, text: str, *args: tuple, **kwargs: any):
        """
        テキスト内の{fore:<r,g,b,a>}や{back:<r,g,b,a>}タグ、{end}を解析して色付きで表示
        また、色名を使った指定もサポート。
        
        Args:
            text (str): any
            *args (tuple): any
            **kwargs (any): any
        """
        
        # 正規表現で{fore:...}や{back:...}、{end}を抽出
        parts = re.split(r'(\{.*?\})', text)
        colored_text = ""

        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                # 色指定タグの場合、対応するエスケープシーケンスに変換
                colored_text += self.parse_color_tag(re.sub(r'\s+', '', part))
            else:
                # 通常のテキストはそのまま追加
                colored_text += part

        # textの最後に終了コードを追加
        colored_text += self.reset  # リセットコードを追加する
        
        # 元のprint関数を使用して出力
        builtins.print(colored_text, *args, **kwargs)

def print(text, *args, **kwargs):
    """
    色付きでテキストを表示するために、print関数をオーバーラップするための関数
    
    Args:
        text (str): any
    """
    ColorPrinter().print_with_color(text, *args, **kwargs)
    
# # 使用例
# print("This is {fore:red}red{end} and {back:blue}blue{end} text.")
