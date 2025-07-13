import cv2, sys, json, os

def gaussian_blur(img, ksize=(5, 5), sigma=1.0):
    """
    Aplica suavização Gaussiana.
    - img: imagem de entrada (BGR ou grayscale).
    - ksize: tupla (largura, altura) do kernel (deve ser valores ímpares, ex: (5,5)).
    - sigma: desvio padrão do Gaussiano.
    Retorna a imagem suavizada (mesmo número de canais).
    """
    # Se for colorida (3 canais), aplica o filtro em cada canal igualmente
    # cv2.GaussianBlur funciona tanto em BGR quanto em grayscale diretamente:
    return cv2.GaussianBlur(img, ksize, sigma)

if __name__ == "__main__":
    # Espera receber: in_path, out_path
    if len(sys.argv) != 3:
        print(json.dumps({"status":"error","msg":"Uso: gaussian_blur.py <in_path> <out_path>"}))
        sys.exit(1)

    in_path  = sys.argv[1]
    out_path = sys.argv[2]

    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    # Aplica o Gaussian Blur (kernel 5×5 e sigma 1.0)
    result = gaussian_blur(img, ksize=(5, 5), sigma=1.0)

    # Grava o resultado
    cv2.imwrite(out_path, result)

    # Retorna JSON com status e caminho absoluto
    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
