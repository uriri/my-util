import argparse
import zipfile
from logging import DEBUG, Formatter, Logger, NullHandler, StreamHandler, getLogger
from pathlib import Path


def create_argparser():
    parser = argparse.ArgumentParser()

    parser.add_argument("src_dir", type=Path, help="directory with zip files")
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="unzip recursive"
    )

    return parser


class UnzipService:
    def __init__(self, *, logger: Logger = None) -> None:
        if logger is None:
            logger = getLogger(__name__)
            handler = NullHandler()
            logger.addHandler(handler)

        self.logger = logger

    def _is_need_directory(self, unzip_dir: str, sample_file: str) -> bool:
        """ディレクトリを作成する必要があるか判定

        directory/file.* の形式になっているか確認

        Args:
            unzip_dir (str): 解凍先ディレクトリ（zipファイル名）
            sample_file (str): zipファイル内のファイルパス

        Returns:
            bool: ディレクトリ作成が必要
        """
        return sample_file.startswith(unzip_dir + "/") is False

    def unzip(self, root_dir: Path, is_recursive: bool) -> None:
        """zip解凍

        Args:
            root_dir (Path): 対象ディレクトリ
            is_recursive (bool): サブディレクトリまで再帰処理
        """
        ptn = "**/*.zip" if is_recursive else "*.zip"

        for zip_file in root_dir.glob(ptn):
            with zipfile.ZipFile(zip_file) as zf:
                self.logger.info(f"unzip: {zf.filename}")

                unzip_dir, _ = zf.filename.split(".")
                sample_file = zf.namelist()[0]
                is_need_dir = self._is_need_directory(unzip_dir, sample_file)

                if is_need_dir:
                    self.logger.info(f"create dir {unzip_dir}")
                    zf.extractall(unzip_dir)
                else:
                    zf.extractall()


if __name__ == "__main__":
    logger = getLogger(__name__)

    handler = StreamHandler()
    handler.setFormatter(Formatter("%(asctime)s [%(levelname)s] %(message)s"))

    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    logger.propagate = False

    parser = create_argparser()
    args = parser.parse_args()

    root_dir = args.src_dir
    is_recursive = args.recursive

    service = UnzipService(logger=logger)
    service.unzip(root_dir, is_recursive)
