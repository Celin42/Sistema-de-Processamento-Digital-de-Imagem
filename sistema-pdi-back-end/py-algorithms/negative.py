import cv2, sys, json, os

def negative(img):
    return 255 - img

if __name__ == "__main__":
    in_path, out_path = sys.argv[1], sys.argv[2]
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}))
        sys.exit(1)
    cv2.imwrite(out_path, negative(img))
    print(json.dumps({"status":"ok","out":os.path.abspath(out_path)}))
