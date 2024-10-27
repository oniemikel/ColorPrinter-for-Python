import re
import builtins  # 元のprint関数を参照するために使用

class ColorPrinter:
    """
    色付きのテキストをコンソールに出力するクラス。
    """

    # 色名とRGBA値のマッピング（アルファ値は1）
    COLOR_MAP: dict[str, tuple] = {
        "black"   : (  0,   0,   0,  1),
        "white"   : (255, 255, 255,  1),
        "red"     : (255,   0,   0,  1),
        "green"   : (  0, 255,   0,  1),
        "blue"    : (  0,   0, 255,  1),
        "yellow"  : (255, 255,   0,  1),
        "cyan"    : (  0, 255, 255,  1),
        "magenta" : (255,   0, 255,  1),
        "gray"    : (128, 128, 128,  1),
        "skyblue" : (135, 206, 235,  1),
    }

    def __init__(self):
        """
        ColorPrinterクラスの初期化メソッド。
        """
        self.reset: str = "\033[0m"
        self.bold: str = "\033[1m"
        self.italic: str = "\033[3m"
        self.underline: str = "\033[4m"
        self.active_styles: dict[str, any] = {
            "fore": "",
            "back": "",
            "bold": False,
            "italic": False,
            "underline": False,
        }

    def set_rgba_color(self, color: tuple) -> str:
        """
        RGBA値に基づいて前景色のANSIエスケープシーケンスを生成する。

        Args:
            color (tuple): RGBA値を含むタプル。

        Returns:
            str: 前景色用のANSIエスケープシーケンス。
        """
        r, g, b, a = color
        return f"\033[38;2;{r};{g};{b}m"

    def set_rgba_background(self, color: tuple) -> str:
        """
        RGBA値に基づいて背景色のANSIエスケープシーケンスを生成する。

        Args:
            color (tuple): RGBA値を含むタプル。

        Returns:
            str: 背景色用のANSIエスケープシーケンス。
        """
        r, g, b, a = color
        return f"\033[48;2;{r};{g};{b}m"

    def get_color_by_name(self, name: str) -> tuple:
        """
        色名からRGBA値を取得する。

        Args:
            name (str): 色の名前。

        Returns:
            tuple: RGBA値を含むタプル。色名が無効な場合はNoneを返す。
        """
        return self.COLOR_MAP.get(name.lower(), None)

    def parse_rgba(self, value: str) -> tuple:
        """
        RGBA形式の文字列を解析し、RGBA値をタプルとして返す。

        Args:
            value (str): RGBA形式の文字列。

        Returns:
            tuple: RGBA値を含むタプル。無効な場合はNoneを返す。
        """
        # カンマの前後に空白があっても正しくマッチする正規表現
        rgba_match = re.match(r'rgba\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,?\s*([\d.]*)\s*\)', value)
        if rgba_match:
            r, g, b = map(int, rgba_match.groups()[:3])  # r, g, bを整数に変換
            a = float(rgba_match.group(4)) if rgba_match.group(4) else 1  # アルファ値が指定されていない場合は1
            return (r, g, b, a)  # aを指定された値または1にする
        return None

    def reset_styles(self):
        """
        現在のスタイルをリセットする。
        """
        self.active_styles = {
            "fore": "",
            "back": "",
            "bold": False,
            "italic": False,
            "underline": False,
        }

    def parse_color_tag(self, tag: str) -> str:
        """
        タグを解析して対応するエスケープシーケンスに変換。

        Args:
            tag (str): 解析する色指定のタグ。

        Returns:
            str: 対応するANSIエスケープシーケンス。
        """
        output = ""

        # endタグの処理
        if "end" in tag:
            # 現在のスタイルをリセット
            output += self.reset
            self.reset_styles()

            # タグに指定されたスタイルを適用
            style_tags = re.findall(r'(\w+)\s*:\s*([\w(),\s]+)', tag)
            for style, color_value in style_tags:
                if style == "fore":
                    color_value = self.parse_rgba(color_value) or self.get_color_by_name(color_value)
                    if color_value:
                        output += self.set_rgba_color(color_value)
                elif style == "back":
                    color_value = self.parse_rgba(color_value) or self.get_color_by_name(color_value)
                    if color_value:
                        output += self.set_rgba_background(color_value)
            return output

        # 色とスタイルの指定
        style_tags = re.findall(r'(\w+)\s*:\s*([\w(),\s]+)', tag)
        for style, color_value in style_tags:
            if style == "fore":
                color_value = self.parse_rgba(color_value) or self.get_color_by_name(color_value)
                if color_value:
                    output += self.set_rgba_color(color_value)
                    self.active_styles["fore"] = color_value
            elif style == "back":
                color_value = self.parse_rgba(color_value) or self.get_color_by_name(color_value)
                if color_value:
                    output += self.set_rgba_background(color_value)
                    self.active_styles["back"] = color_value
            elif style == "bold":
                output += self.bold
                self.active_styles["bold"] = True
            elif style == "italic":
                output += self.italic
                self.active_styles["italic"] = True
            elif style == "underline":
                output += self.underline
                self.active_styles["underline"] = True

        return output

    def print_with_color(self, text: str, *args, **kwargs):
        """
        テキスト内のタグを解析して色付きで表示。

        Args:
            text (str): 色付きで表示するテキスト。
            *args: print関数に渡す追加の引数。
            **kwargs: print関数に渡す追加のキーワード引数。
        """
        parts = re.split(r'(\{.*?\})', text)
        colored_text = ""
        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                colored_text += self.parse_color_tag(part)
            else:
                colored_text += part
        colored_text += self.reset
        builtins.print(colored_text, *args, **kwargs)



def print(text, *args, **kwargs):
    """
    色付きでテキストを表示するために、print関数をオーバーラップするための関数。

    Args:
        text (str): 色付きで表示するテキスト。
        *args: print関数に渡す追加の引数。
        **kwargs: print関数に渡す追加のキーワード引数。
    """
    ColorPrinter().print_with_color(text, *args, **kwargs)
