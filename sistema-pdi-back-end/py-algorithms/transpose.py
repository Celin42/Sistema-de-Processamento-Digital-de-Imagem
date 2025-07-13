import cv2, sys, json, os
import numpy as np

def transpose_image(img):
    # Se for colorida (3 canais), convém transpor o array inteiro
    # cv2.transpose funciona tanto para grayscale quanto color
    return cv2.transpose(img)

if __name__ == "__main__":
    in_path, out_path = sys.argv[1], sys.argv[2]
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    result = transpose_image(img)
    cv2.imwrite(out_path, result)
    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
