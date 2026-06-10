import cv2
import requests
from pathlib import Path

HEADSHOTS_DIR = Path("assets/images/headshots")
HEADSHOTS_DIR.mkdir(parents=True, exist_ok=True)

CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Best candidate-specific URLs: find the one with exactly 1 face (solo headshot)
BEST = {
    "wade_faulkner": {
        "url": "https://wadefaulkner.com/__static/production-domaincom-v1-0-2/422/1999422/cYNPspfn/0200014dc9f94df6aa7a1d928ac9f5df",
        "name": "Wade Faulkner",
    },
    "richard_sapp": {
        "url": "https://sapp4jp.com/wp-content/uploads/2025/08/RichardSapp_Vert_Opt.webp",
        "name": "Richard Sapp",
    },
    # Check the single-face option for Gauntt
    "john_gauntt_jr": {
        "urls": [
            ("https://storage.googleapis.com/cerberus-campaign-images/assets/images/Gauntt_About_Bio3.png", "bio3"),
            ("https://storage.googleapis.com/cerberus-campaign-images/assets/images/Gauntt_About_Hero.png", "hero"),
        ],
        "name": "John Gauntt Jr.",
    },
    # Best solo headshot for Jessica
    "jessica_a_gonzalez": {
        "urls": [
            ("https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/fcd97e9d-e800-4d72-9740-1fa03207126b/Slide5.JPG", "slide5"),
            ("https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/7a77df29-1b75-4e08-8e67-7ffee385b0fd/Slide6.JPG", "slide6"),
            ("https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/e806f2c8-d62b-41cf-a1b4-9cb6af9d5364/Slide9.JPG", "slide9"),
        ],
        "name": "Jessica Gonzalez",
    },
}


def download_image(url):
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            return resp.content
    except Exception as e:
        print(f"    DL error: {e}")
    return None


def check_face(data):
    """Check if image data contains exactly 1 face. Return (has_face, num_faces, img)"""
    tmp = HEADSHOTS_DIR / "_check_tmp.jpg"
    tmp.write_bytes(data)
    img = cv2.imread(str(tmp))
    if img is None:
        tmp.unlink(missing_ok=True)
        return False, 0, None
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    tmp.unlink(missing_ok=True)
    return len(faces) > 0, len(faces), img


def save_best(slug, img, name):
    """Resize to 400x500 maintaining aspect ratio with padding"""
    h, w = img.shape[:2]
    target_w, target_h = 400, 500
    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    canvas = cv2.copyMakeBorder(
        resized,
        0, target_h - new_h,
        (target_w - new_w) // 2, (target_w - new_w + 1) // 2,
        cv2.BORDER_CONSTANT, value=(255, 255, 255),
    )
    dest = HEADSHOTS_DIR / f"{slug}.jpg"
    cv2.imwrite(str(dest), canvas, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(f"    SAVED {dest.name} ({new_w}x{new_h} -> {target_w}x{target_h})")
    return dest


def main():
    print("=" * 60)
    print("Refining headshots - finding best solo photos")
    print("=" * 60)

    # 1. Debbie Garrett - try with verify=False
    print("\n--- Debbie Garrett ---")
    try:
        resp = requests.get(
            "https://debbiegarrettforjudge.com/wp-content/uploads/2023/08/Debbie-Garrett.jpg",
            timeout=30, verify=False,
        )
        if resp.status_code == 200:
            has, num, img = check_face(resp.content)
            if has:
                save_best("debbie_garrett", img, "Debbie Garrett")
                print(f"    Debbie Garrett: {num} face(s) - SAVED")
            else:
                print(f"    Debbie Garrett: no face detected in original image")
        else:
            print(f"    Debbie Garrett: HTTP {resp.status_code}")
    except Exception as e:
        print(f"    Debbie Garrett: {e}")

    # 2. Wade Faulkner - single URL already saved, but re-check with higher min size
    print("\n--- Wade Faulkner ---")
    data = download_image(BEST["wade_faulkner"]["url"])
    if data:
        has, num, img = check_face(data)
        if has:
            save_best("wade_faulkner", img, "Wade Faulkner")
            print(f"    Wade Faulkner: {num} face(s) - SAVED")
        else:
            print(f"    Wade Faulkner: 0 faces at higher threshold - keeping previous")
    else:
        print(f"    Wade Faulkner: download failed")

    # 3. Richard Sapp - already good
    print("\n--- Richard Sapp ---")
    data = download_image(BEST["richard_sapp"]["url"])
    if data:
        has, num, img = check_face(data)
        if has:
            save_best("richard_sapp", img, "Richard Sapp")
            print(f"    Richard Sapp: {num} face(s) - SAVED")
        else:
            print(f"    Richard Sapp: 0 faces at higher threshold")
    else:
        print(f"    Richard Sapp: download failed")

    # 4. John Gauntt Jr - try each URL, pick the best solo
    print("\n--- John Gauntt Jr. ---")
    best_gauntt = None
    best_gauntt_faces = 0
    for url, label in BEST["john_gauntt_jr"]["urls"]:
        data = download_image(url)
        if data:
            has, num, img = check_face(data)
            print(f"    {label}: {num} face(s)")
            if num == 1:
                best_gauntt = img
                best_gauntt_faces = 1
                print(f"      -> Best solo option")
                break
            elif num > best_gauntt_faces:
                best_gauntt = img
                best_gauntt_faces = num
        else:
            print(f"    {label}: download failed")
    if best_gauntt is not None:
        save_best("john_gauntt_jr", best_gauntt, "John Gauntt Jr.")

    # 5. Jessica Gonzalez - try each slide
    print("\n--- Jessica Gonzalez ---")
    best_jessica = None
    best_jessica_faces = 0
    for url, label in BEST["jessica_a_gonzalez"]["urls"]:
        data = download_image(url)
        if data:
            has, num, img = check_face(data)
            print(f"    {label}: {num} face(s)")
            if num == 1:
                best_jessica = img
                best_jessica_faces = 1
                print(f"      -> Best solo option")
                break
            elif num > best_jessica_faces and num < 3:
                best_jessica = img
                best_jessica_faces = num
        else:
            print(f"    {label}: download failed")
    if best_jessica is not None:
        save_best("jessica_a_gonzalez", best_jessica, "Jessica Gonzalez")

    print("\n" + "=" * 60)
    print("FINAL HEADSHOTS IN DIRECTORY:")
    for f in sorted(HEADSHOTS_DIR.glob("*.jpg")):
        img = cv2.imread(str(f))
        if img is not None:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
            print(f"  {f.name:30s} {img.shape[1]}x{img.shape[0]} - {len(faces)} face(s)")
        else:
            print(f"  {f.name:30s} FAILED TO LOAD")


if __name__ == "__main__":
    main()
