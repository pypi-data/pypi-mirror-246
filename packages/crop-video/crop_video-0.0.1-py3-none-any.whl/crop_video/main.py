# -*- encoding: utf-8 -*-
# @Author: SWHL
# @Contact: liekkaskono@163.com
import argparse
from pathlib import Path
from typing import Optional

from moviepy import editor


class CropVideo:
    def __init__(self) -> None:
        pass

    def __call__(
        self,
        video_path: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        save_path: Optional[str] = None,
    ):
        if not any([video_path, start_time, end_time, save_path]):
            raise ValueError(
                "The video_path, start_time, end_time, save_path four parameters must not be empty."
            )

        save_dir = Path(save_path).resolve().parent
        self.mkdir(save_dir)

        with editor.VideoFileClip(video_path) as cliper:
            video_clip = cliper.subclip(start_time, end_time)

            with editor.CompositeVideoClip([video_clip]) as f:
                f.write_videofile(str(save_path))

        print(f"Saved under {save_dir}")

    @staticmethod
    def mkdir(path):
        Path(path).mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "video_path",
        type=str,
        default=None,
        help="Video path",
    )
    parser.add_argument(
        "start_time",
        type=str,
        default=None,
        help="Start time",
    )
    parser.add_argument(
        "end_time",
        type=str,
        default=None,
        help="End time",
    )
    parser.add_argument("save_path", type=str, default=None)
    args = parser.parse_args()

    cutter = CropVideo()
    cutter(args.video_path, args.start_time, args.end_time, args.save_path)


if __name__ == "__main__":
    main()
