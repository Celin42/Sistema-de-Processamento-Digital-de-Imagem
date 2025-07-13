import cv2, sys, json, os

def unsharp_mask(img, ksize=(5,5), sigma=1.0, amount=1.5):
    """
    Unsharp Mask:
    1) blur = GaussianBlur(img)
    2) mask  = img - blur
    3) result = img + amount * mask
    Clip result para [0,255] e converte para uint8.
    """
    # aplica Gaussian blur
    blur = cv2.GaussianBlur(img, ksize, sigma)
    # calcula máscara
    mask = cv2.subtract(img, blur)
    # adiciona máscara ponderada
    result = cv2.addWeighted(img, 1.0, mask, amount, 0)
    # garantir tipo correto
    return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(json.dumps({"status":"error","msg":"Uso: unsharp_mask.py <in> <out>"}))
        sys.exit(1)

    in_path, out_path = sys.argv[1], sys.argv[2]
    img = cv2.imread(in_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print(json.dumps({"status":"error","msg":"falha ao ler imagem"}), flush=True)
        sys.exit(1)

    out = unsharp_mask(img, ksize=(5,5), sigma=1.0, amount=1.5)
    cv2.imwrite(out_path, out)
    print(json.dumps({"status":"ok","out": os.path.abspath(out_path)}), flush=True)
    sys.exit(0)
