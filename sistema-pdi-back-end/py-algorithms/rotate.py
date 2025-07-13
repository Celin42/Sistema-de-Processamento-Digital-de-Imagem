import cv2, sys, json, os

def rotate90_image(img):
    # Rotaciona 90° no sentido horário:
    # primeiro, obtém centro, em seguida, matriz de rotação 90°
    # mas podemos usar cv2.rotate (mais simples)
    # cv2.ROTATE_90_CLOCKWISE
    return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

if __name__ == "__main__":
    in_path, out_path = sys.argv[1], sys.argv[2]
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    result = rotate90_image(img)
    cv2.imwrite(out_path, result)
    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
