"""ディレクトリ配下のファイルサイズを計算する"""

from argparse import ArgumentParser
from pathlib import Path


def conv_readable_byte_size(byte_size: int):
    """バイト表記のサイズを分かりやすい単位に変換する

    TBまで対応

    Args:
        byte_size (int): バイトサイズ

    Returns:
        str: 変換後の単位表示 例: 1.0 KB
    """
    multipe = 1000
    for unit in ["KB", "MB", "GB", "TB"]:
        byte_size /= multipe
        if byte_size < multipe:
            return "{0:.1f} {1}".format(byte_size, unit)


def _cal_size(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    elif path.is_dir():
        return sum((_cal_size(p) for p in path.iterdir()))


def cal_directories_size(root_path: Path):
    for path in root_path.glob("**"):
        if path.is_dir():
            yield path, _cal_size(path)


if __name__ == "__main__":
    parser = ArgumentParser(description="show each directory size")
    parser.add_argument("root", help="root path")
    parser.add_argument("-o", type=str, default="result.txt", help="output file name")

    args = parser.parse_args()

    root_path = Path(args.root)
    result_file = Path(args.o)

    with open(result_file, "w", encoding="utf-8") as f:
        for name, size in sorted(cal_directories_size(root_path), key=lambda x: x[1]):
            f.write(f"{name}: {conv_readable_byte_size(size)}\n")
