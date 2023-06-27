whisper.cppのPybind11バインディング(https://github.com/aarnphm/whispercpp)をテストした。

## インストール方法
pip install whispercppを実行したが、https://github.com/aarnphm/whispercpp/issues/84と同様のエラーが発生した。
そのため、pip install git+https://github.com/aarnphm/whispercpp.git -vvで最新版をインストールしたところ、正常に動作した。

## 音声ファイルについて
whisper.cppでは、16kHzのwavファイルのみサポートされている。
mp3ファイルなどのサポート外のファイルを扱う場合には、変換サイトやffmpegを使うと良い。
今回はネット上にあったサンプルのwavファイルを、変換サイト(https://online-audio-converter.com/ja/)を利用して16kHzに変換した。

## テスト環境
Raspberry Pi 4 Model B(RAM: 4GB)
テスト音声：https://www.hke.jp/products/voice/wav/audition/01.femal.wav　5秒ほどの音声。変換サイトで16kHzに変換後、音声認識を実行した。
使用したモデル：small

## テスト結果
約90秒

## whisper.cppのPybind11について
https://github.com/aarnphm/whispercpp/blob/main/src/whispercpp/utils.pyによると、ggmlのモデルを読み込んでいるようである。
