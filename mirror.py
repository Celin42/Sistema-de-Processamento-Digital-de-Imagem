import cv2, sys, json, os

def mirror_image(img):
    return cv2.flip(img, 1)

if __name__ == "__main__":
    in_path, out_path = sys.argv[1], sys.argv[2]
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    result = mirror_image(img)
    cv2.imwrite(out_path, result)
    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
