import cv2, sys, json, os
import numpy as np

def sharpen(img):
    """
    Aplica kernel de realce (sharpen).
    Usa kernel 3×3: [[0,-1,0],[-1,5,-1],[0,-1,0]]
    Funciona em BGR ou grayscale.
    """
    kernel = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)
    return cv2.filter2D(img, -1, kernel)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"status":"error","msg":"Uso: sharpen.py <in_path> <out_path>"}))
        sys.exit(1)

    in_path, out_path = sys.argv[1], sys.argv[2]
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    result = sharpen(img)
    cv2.imwrite(out_path, result)

    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
