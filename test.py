import yt_dlp
import os

def download_audio_as_wav(url: str, output_dir: str):
    # Убедитесь, что директория существует
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Путь и имя файла
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',  # Конвертация в WAV
            'preferredquality': '192',
        }],
        'quiet': False,  # True если не хотите видеть вывод
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Пример использования
if __name__ == "__main__":
    video_url = "https://on.api-core.soundcloud-stage.com/ZXUm9shL8MX2ZXhKNh"  # замени на нужную ссылку
    download_folder = "./music_wav"  # куда сохранять
    download_audio_as_wav(video_url, download_folder)
