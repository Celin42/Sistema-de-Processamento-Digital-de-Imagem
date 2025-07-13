import cv2, sys, json, os
import numpy as np

def equalize_histogram(img):
    """
    Se a imagem for colorida (3 canais RGB converte para YCrCb, equaliza o canal Y e reconverte para RGB
    Se for grayscale (1 canal), aplica cv2.equalizeHist diretamente.
    Retorna a imagem com histograma equalizado.
    """
    if img.ndim == 3 and img.shape[2] == 3:
        # Converte BGR → YCrCb
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        # Equaliza o canal Y (índice 0)
        ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
        # Converte de volta YCrCb → BGR
        equalized = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    else:
        # Imagem já é grayscale (1 canal)
        equalized = cv2.equalizeHist(img)
    return equalized

if __name__ == "__main__":
    # Espera receber exatamente dois argumentos: <in_path> e <out_path>
    if len(sys.argv) != 3:
        print(json.dumps({"status":"error","msg":"Uso: hist_equalization.py <in_path> <out_path>"}))
        sys.exit(1)

    in_path  = sys.argv[1]
    out_path = sys.argv[2]

    # Lê a imagem de entrada (pode ser colorida ou grayscale)
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    # Equaliza histograma
    result = equalize_histogram(img)

    # Grava o resultado
    cv2.imwrite(out_path, result)

    # Retorna JSON padrão para o pythonRunner
    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
