import cv2, sys, json, os

def otsu(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return thresh

if __name__ == "__main__":
    in_path, out_path = sys.argv[1], sys.argv[2]
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}))
        sys.exit(1)
    cv2.imwrite(out_path, otsu(img))
    print(json.dumps({"status":"ok","out":os.path.abspath(out_path)}))