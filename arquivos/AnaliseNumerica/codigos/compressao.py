from pathlib import Path

import ffmpeg

pasta = Path(__file__).resolve().parent
entrada = pasta / "2026-11-17.mp4"
saida = pasta / "2026-11-17_comprimido.mp4"

if not entrada.is_file():
    raise FileNotFoundError(f"Vídeo não encontrado: {entrada}")

try:
    (
        ffmpeg
        .input(str(entrada))
        .output(
            str(saida),
            vcodec="libx264",
            crf=28,
            preset="medium",
            acodec="aac",
            movflags="+faststart",
        )
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )
    print(f"Vídeo comprimido com sucesso: {saida}")
except ffmpeg.Error as erro:
    mensagem = erro.stderr.decode("utf-8", errors="replace") if erro.stderr else str(erro)
    raise RuntimeError(f"Falha ao comprimir o vídeo:\n{mensagem}") from erro