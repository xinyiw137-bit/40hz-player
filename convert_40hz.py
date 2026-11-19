#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
40Hz 伽马波音乐离线转换器
把一首音乐转成"音量每秒起伏 40 次"的版本（40Hz 振幅调制 / 伽马听觉夹带）。

用法：
    pip install numpy soundfile        # 首次使用需安装依赖
    python convert_40hz.py 输入.wav 输出.wav            # 默认 40Hz / 50% 强度
    python convert_40hz.py 输入.flac 输出.wav --depth 0.3 --freq 40

支持格式：WAV / FLAC / OGG（soundfile 支持的格式）。
MP3 请先转成 WAV（或用网页版 40hz_player.html，浏览器可直接播 MP3）。
"""

import argparse
import numpy as np
import soundfile as sf


def apply_40hz_modulation(data, sample_rate, freq=40.0, depth=0.5):
    """
    40Hz 振幅调制：y(t) = x(t) * (1 + depth * sin(2π * freq * t))
    depth=0.5 表示音量在 50% ~ 150% 之间起伏，平均仍是原音量。
    """
    t = np.arange(len(data)) / sample_rate
    envelope = 1.0 + depth * np.sin(2 * np.pi * freq * t)

    if data.ndim == 2:               # 立体声
        out = data * envelope[:, None]
    else:                            # 单声道
        out = data * envelope

    # 防止削波：若峰值超过 1.0，整体归一化
    peak = np.max(np.abs(out))
    if peak > 1.0:
        out = out / peak * 0.98
    return out


def main():
    parser = argparse.ArgumentParser(
        description="把音乐转为 40Hz 伽马调制版本（音量每秒起伏 40 次）"
    )
    parser.add_argument("input", help="输入音频文件")
    parser.add_argument("output", help="输出音频文件")
    parser.add_argument("--freq", type=float, default=40.0,
                        help="调制频率（赫兹），默认 40")
    parser.add_argument("--depth", type=float, default=0.5,
                        help="调制强度 0~1，默认 0.5（建议 0.3~0.5）")
    args = parser.parse_args()

    if not 0.0 <= args.depth <= 1.0:
        parser.error("--depth 必须在 0 到 1 之间")

    print(f"正在读取: {args.input}")
    data, sample_rate = sf.read(args.input, dtype="float32")

    print(f"正在处理: {args.freq} Hz 调制，强度 {args.depth} ...")
    out = apply_40hz_modulation(data, sample_rate, args.freq, args.depth)

    sf.write(args.output, out, sample_rate)
    print(f"完成！已保存到: {args.output}")


if __name__ == "__main__":
    main()
