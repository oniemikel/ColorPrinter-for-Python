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

        # endタグの処理（特定の色やスタイルのみリセット）
        if tag.startswith("{end"):
            # まず、endタグでリセットする項目を特定
            end_options = re.findall(r'end\s*(\w+)?', tag)
            reset_options = set(end_options) if end_options[0] else {"fore", "back", "bold", "italic", "underline"}

            # 全体リセット
            output += self.reset

            # endタグ内で新しく指定されたスタイルを適用
            additional_styles = re.findall(r'(\w+)\s*:\s*(\w+)', tag)
            for style, color_name in additional_styles:
                if style == "fore" and "fore" in reset_options:
                    color_value = self.get_color_by_name(color_name)
                    if color_value:
                        output += self.set_rgba_color(color_value)
                        self.active_styles["fore"] = color_value
                elif style == "back" and "back" in reset_options:
                    color_value = self.get_color_by_name(color_name)
                    if color_value:
                        output += self.set_rgba_background(color_value)
                        self.active_styles["back"] = color_value
                elif style == "bold" and "bold" in reset_options:
                    output += self.bold
                    self.active_styles["bold"] = True
                elif style == "italic" and "italic" in reset_options:
                    output += self.italic
                    self.active_styles["italic"] = True
                elif style == "underline" and "underline" in reset_options:
                    output += self.underline
                    self.active_styles["underline"] = True

            # リセット対象外のスタイルを再適用
            output += self.reapply_styles(exclude=reset_options)
            return output

        # それ以外のスタイルタグの処理
        style_tags = re.findall(r'(\w+)\s*:\s*(\w+)', tag)
        for style, color_name in style_tags:
            if style == "fore":
                color_value = self.get_color_by_name(color_name)
                if color_value:
                    output += self.set_rgba_color(color_value)
                    self.active_styles["fore"] = color_value
            elif style == "back":
                color_value = self.get_color_by_name(color_name)
                if color_value:
                    output += self.set_rgba_background(color_value)
                    self.active_styles["back"] = color_value

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

        return output

    def reapply_styles(self, exclude: set) -> str:
        """
        リセット後に再適用するスタイルを生成する。

        Args:
            exclude (set): 再適用しないスタイルのセット。

        Returns:
            str: 再適用するANSIエスケープシーケンス。
        """
        output = ""
        if "fore" not in exclude and self.active_styles["fore"]:
            output += self.set_rgba_color(self.active_styles["fore"])
        if "back" not in exclude and self.active_styles["back"]:
            output += self.set_rgba_background(self.active_styles["back"])
        if "bold" not in exclude and self.active_styles["bold"]:
            output += self.bold
        if "italic" not in exclude and self.active_styles["italic"]:
            output += self.italic
        if "underline" not in exclude and self.active_styles["underline"]:
            output += self.underline
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
