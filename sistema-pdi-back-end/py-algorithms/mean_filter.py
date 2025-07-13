import cv2, sys, json, os

def mean_filter(img, ksize=(5,5)):
    """
    Aplica filtro da média (box filter) de tamanho ksize.
    Funciona em imagens BGR ou grayscale.
    """
    return cv2.blur(img, ksize)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"status":"error","msg":"Uso: mean_filter.py <in_path> <out_path>"}))
        sys.exit(1)

    in_path, out_path = sys.argv[1], sys.argv[2]
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    result = mean_filter(img, ksize=(5,5))
    cv2.imwrite(out_path, result)
    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
