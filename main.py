import pyttsx3
import platform
import os

# WindowsのSAPI5ドライバを使用するために、ドライバ名を明示的に指定します
DRIVER_NAME = 'sapi5' # Windows環境向け
# ファイル名を WAV 形式に変更
OUTPUT_FILENAME = "output_speech.wav" 

def speach(text: str):
    # 1. TTSエンジンを初期化します
    try:
        engine = pyttsx3.init(DRIVER_NAME)
    except Exception as e:
        # comtypesが見つからないのはWSLでは正常
        print(f"⚠️ SAPI5ドライバの初期化に失敗しました。デフォルト/espeakドライバにフォールバックします: {e}")
        try:
            engine = pyttsx3.init()
        except Exception as e:
            print(f"❌ エラー: TTSエンジンの初期化中に失敗しました: {e}")
            return

    # 2. 日本語音声の設定
    voices = engine.getProperty('voices')
    japanese_voice_found = False
    
    is_windows = platform.system() == 'Windows'
    is_linux = platform.system() == 'Linux'

    if is_windows:
        for voice in voices:
            if 'haruka' in voice.name.lower() or 'japanese' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                japanese_voice_found = True
                print(f"✅ Windows (SAPI5) の高品質日本語音声 '{voice.name}' を設定しました。")
                break

    elif is_linux:
        try:
            engine.setProperty('voice', 'ja')
            japanese_voice_found = True
            print("✅ 環境がLinux/WSLであるため、明示的に言語を日本語('ja')に設定しました。")
        except Exception:
            pass

    if not japanese_voice_found:
        print(f"⚠️ 日本語音声が見つかりませんでした。デフォルト音声で読み上げます。")

    # 速度と音量調整
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0) 

    # 3. テキストをファイルとして保存
    
    # 【★ここから変更★】絶対パスを使用して保存先を明確にします
    current_dir = os.getcwd()
    full_output_path = os.path.join(current_dir, OUTPUT_FILENAME)
    
    print(f"💾 音声をファイル '{full_output_path}' として保存しています...")
    try:
        # save_to_file() に絶対パスを渡す
        engine.save_to_file(text, full_output_path)
        
        # runAndWait() を実行すると、ファイル保存処理が実行されます
        engine.runAndWait()
        
        # ファイルの存在確認も絶対パスで行う
        if os.path.exists(full_output_path):
            print(f"✅ ファイル '{full_output_path}' の保存が完了しました。")
        else:
             # runAndWait() が成功したにも関わらずファイルがない場合は、パスの問題の可能性
             print(f"❌ エラー: ファイル '{full_output_path}' の保存に失敗したか、ファイルが見つかりません。")

    except Exception as e:
        print(f"❌ ファイル保存中にエラーが発生しました: {e}")
    
    engine.stop()

# --- 実行例 ---

if __name__ == "__main__":
    message_to_speak = "WAV形式で音声ファイルを保存します。この形式はエンコードが不要なので、成功しやすいです。"
    
    # 変数を引数として関数に渡します
    speach(message_to_speak)