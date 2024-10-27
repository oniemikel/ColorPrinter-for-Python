import re
import builtins  # 元のprint関数を参照するために使用

class ColorPrinter:
    """
    色付きのテキストをコンソールに出力するクラス。
    """

    # 色名とRGBA値のマッピング
    COLOR_MAP: dict[str, tuple] = {
        "black"  : (  0,   0,   0, 255),
        "white"  : (255, 255, 255, 255),
        "red"    : (255,   0,   0, 255),
        "green"  : (  0, 255,   0, 255),
        "blue"   : (  0,   0, 255, 255),
        "yellow" : (255, 255,   0, 255),
        "cyan"   : (  0, 255, 255, 255),
        "magenta": (255,   0, 255, 255),
        "gray"   : (128, 128, 128, 255),
        "skyblue": (135, 206, 235, 255),
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
        r, g, b, _ = color
        return f"\033[38;2;{r};{g};{b}m"

    def set_rgba_background(self, color: tuple) -> str:
        """
        RGBA値に基づいて背景色のANSIエスケープシーケンスを生成する。

        Args:
            color (tuple): RGBA値を含むタプル。

        Returns:
            str: 背景色用のANSIエスケープシーケンス。
        """
        r, g, b, _ = color
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
        output: str = ""

        if tag == "{end}":
            # 全てのスタイルをリセットする
            output += self.reset_styles_to_output()
            return output

        # スタイルをリセットする
        reset_fore = False
        reset_back = False

        # 指定された色やスタイルを処理
        style_tags = re.findall(r'(\w+)\s*:\s*(\w+)', tag)
        for style, color_name in style_tags:
            if style == "fore":
                color_value = self.get_color_by_name(color_name)
                if color_value:
                    output += self.set_rgba_color(color_value)
                    self.active_styles["fore"] = color_value
                else:
                    reset_fore = True
            elif style == "back":
                color_value = self.get_color_by_name(color_name)
                if color_value:
                    output += self.set_rgba_background(color_value)
                    self.active_styles["back"] = color_value
                else:
                    reset_back = True

        # スタイルの適用
        if "bold" in tag:
            output += self.bold
            self.active_styles["bold"] = True
        if "italic" in tag:
            output += self.italic
            self.active_styles["italic"] = True
        if "underline" in tag:
            output += self.underline
            self.active_styles["underline"] = True
        
        # reset指定の処理
        if "end" in tag:
            if reset_fore:
                output += self.reset
                self.active_styles["fore"] = ""
            if reset_back:
                output += self.reset
                self.active_styles["back"] = ""

        return output

    def reset_styles_to_output(self) -> str:
        """
        現在のアクティブスタイルに基づいてリセット用のエスケープシーケンスを生成。

        Returns:
            str: リセット用のANSIエスケープシーケンス。
        """
        output = self.reset
        if self.active_styles["fore"]:
            output += self.reset
        if self.active_styles["back"]:
            output += self.reset
        return output

    def print_with_color(self, text: str, *args: tuple, **kwargs: any):
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

        # 最後にリセットコードを追加
        colored_text += self.reset
        
        # 元のprint関数を使用して出力
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
