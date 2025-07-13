import cv2, sys, json, os

def canny_edge(img):
    # Converte para tons de cinza (se ainda não estiver)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Aplica Blur Gaussiano leve
    blurred = cv2.GaussianBlur(gray, (5, 5), 1.4)
    # Detecta bordas usando Canny
    edges = cv2.Canny(blurred, 100, 200)
    return edges

if __name__ == "__main__":
    in_path, out_path = sys.argv[1], sys.argv[2]
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    result = canny_edge(img)
    cv2.imwrite(out_path, result)

    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
