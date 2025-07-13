import cv2, sys, json, os

def alpha_combine(img1, img2, alpha=0.5):
    # img1, img2: RGB ou grayscale; retorna tipo uint8
    beta = 1.0 - alpha
    result = cv2.addWeighted(img1, alpha, img2, beta, 0)
    return result

if __name__ == "__main__":
    if not (4 <= len(sys.argv) <= 5):
        print(json.dumps({"status":"error","msg":"Uso: alpha.py <in1> <in2> <out> [alpha]"}), flush=True)
        sys.exit(1)

    in1, in2, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    alpha = float(sys.argv[4]) if len(sys.argv) == 5 else 0.5

    img1 = cv2.imread(in1, cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(in2, cv2.IMREAD_UNCHANGED)
    if img1 is None or img2 is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagens"}), flush=True)
        sys.exit(1)

    # redimensiona img2 se necessário
    if img1.shape[:2] != img2.shape[:2]:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    out = alpha_combine(img1, img2, alpha)
    cv2.imwrite(out_path, out)
    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
