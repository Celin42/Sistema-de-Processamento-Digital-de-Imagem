import cv2, sys, json, os
import numpy as np

def sobel_edge(img):
    """
    Calcula a magnitude do gradiente usando filtros de Sobel (3×3).
    Retorna uma imagem 8-bit (0..255) com as bordas realçadas.
    """
    # Se estiver colorida (3 canais), converta para tons de cinza
    if img.ndim == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    # Calcula gradientes em X e Y
    Gx = cv2.Sobel(gray, cv2.CV_64F, dx=1, dy=0, ksize=3)
    Gy = cv2.Sobel(gray, cv2.CV_64F, dx=0, dy=1, ksize=3)

    # Magnitude do gradiente: sqrt(Gx² + Gy²)
    mag = np.hypot(Gx, Gy)

    # Normaliza para [0, 255], convertendo para uint8
    mag = np.uint8((mag / np.max(mag)) * 255)

    return mag

if __name__ == "__main__":
    # Recebe dois argumentos de linha de comando: in_path e out_path
    in_path, out_path = sys.argv[1], sys.argv[2]

    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    # Executa Sobel
    result = sobel_edge(img)

    # Grava a imagem final (bordas realçadas)
    cv2.imwrite(out_path, result)

    # Retorna JSON padrão com "status" e "out" = caminho absoluto
    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
