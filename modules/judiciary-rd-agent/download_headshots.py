import cv2
import requests
import sys
import os
from pathlib import Path

HEADSHOTS_DIR = Path("assets/images/headshots")
HEADSHOTS_DIR.mkdir(parents=True, exist_ok=True)

CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

TARGET_SIZE = (400, 500)

CANDIDATES = {
    "debbie_garrett": {
        "urls": ["https://debbiegarrettforjudge.com/wp-content/uploads/2023/08/Debbie-Garrett.jpg"],
        "name": "Debbie Garrett",
    },
    "wade_faulkner": {
        "urls": [
            "https://wadefaulkner.com/__static/production-domaincom-v1-0-2/422/1999422/cYNPspfn/0200014dc9f94df6aa7a1d928ac9f5df",
        ],
        "name": "Wade Faulkner",
    },
    "john_gauntt_jr": {
        "urls": [
            "https://storage.googleapis.com/cerberus-campaign-images/assets/images/Gauntt_About_Bio1.png",
            "https://storage.googleapis.com/cerberus-campaign-images/assets/images/Gauntt_About_Bio2.png",
            "https://storage.googleapis.com/cerberus-campaign-images/assets/images/Gauntt_About_Bio3.png",
            "https://storage.googleapis.com/cerberus-campaign-images/assets/images/Gauntt_About_Hero.png",
        ],
        "name": "John Gauntt Jr.",
    },
    "richard_sapp": {
        "urls": [
            "https://sapp4jp.com/wp-content/uploads/2025/08/RichardSapp_Vert_Opt.webp",
        ],
        "name": "Richard Sapp",
    },
    "jessica_a_gonzalez": {
        "urls": [
            "https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/fcd97e9d-e800-4d72-9740-1fa03207126b/Slide5.JPG",
            "https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/7a77df29-1b75-4e08-8e67-7ffee385b0fd/Slide6.JPG",
            "https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/6c6725b4-8344-45a7-95fe-ee544ee71168/V%20MVM.jpeg",
            "https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/94d19ac0-b8b6-4999-a853-cb251fe85e00/ORANGE.JPG",
            "https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/2d8d70b4-7487-440c-b936-ee36e16e7ea0/Slide23.JPG",
            "https://img1.wsimg.com/isteam/ip/82eeae29-7a77-42c2-8e91-a4d1be4989e0/downloads/2f5fc2d5-9d9d-45ff-8ff6-850ae2f53433/Slide24.JPG",
            "https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/98053a48-1d6c-49a2-983c-024f8cac6898/Slide4.JPG",
            "https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/3c508dfe-c4e5-46d9-bf84-e2392144064b/Slide10.JPG",
            "https://img1.wsimg.com/isteam/ip/82eeae29-7a77-42c2-8e91-a4d1be4989e0/downloads/90a86491-bc91-4e7f-81da-872317cfaffb/Slide1.JPG",
            "https://img1.wsimg.com/isteam/ip/82eeae29-7a77-42c2-8e91-a4d1be4989e0/downloads/9b3795d7-fc12-45f0-b852-125a43356ff2/Slide2.JPG",
            "https://img1.wsimg.com/isteam/ip/82eeae29-7a77-42c2-8e91-a4d1be4989e0/downloads/fbe88dbf-58f6-493b-99f2-70432df7c71e/Slide3.JPG",
            "https://img1.wsimg.com/isteam/ip/82eeae29-7a77-42c2-8e91-a4d1be4989e0/downloads/88e0ffc3-7dcc-4d24-8ab9-b993b8c7e65b/Slide4.JPG",
            "https://img1.wsimg.com/isteam/ip/82eeae29-7a77-42c2-8e91-a4d1be4989e0/downloads/379a2382-4a7e-4c8b-8823-7aab2513770e/Slide5.JPG",
            "https://img1.wsimg.com/isteam/ip/82eeae29-7a77-42c2-8e91-a4d1be4989e0/downloads/22267c3d-213c-4040-81fa-f7291c28210c/Slide6.JPG",
            "https://img1.wsimg.com/isteam/ip/3e9cd44a-7cda-418d-bcd8-05e3e637795f/downloads/e806f2c8-d62b-41cf-a1b4-9cb6af9d5364/Slide9.JPG",
        ],
        "name": "Jessica Gonzalez",
    },
}


def has_face(image_path):
    img = cv2.imread(str(image_path))
    if img is None:
        return False
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    return len(faces) > 0


def download_and_verify(slug, info):
    best_image = None
    best_faces = 0

    for url in info["urls"]:
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code != 200:
                print(f"  FAIL {url[:80]} - HTTP {resp.status_code}")
                continue

            ext = url.split("?")[0].rsplit(".", 1)[-1] if "." in url else "jpg"
            ext = ext[:4]
            tmp_path = HEADSHOTS_DIR / f"_{slug}_tmp.{ext}"
            tmp_path.write_bytes(resp.content)

            faces_found = 0
            if has_face(tmp_path):
                faces_found = 1
                img = cv2.imread(str(tmp_path))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
                faces_found = len(faces)

            if faces_found > best_faces:
                best_faces = faces_found
                dest = HEADSHOTS_DIR / f"{slug}.jpg"
                # resize to target
                img = cv2.imread(str(tmp_path))
                h, w = img.shape[:2]
                target_w, target_h = TARGET_SIZE
                scale = min(target_w / w, target_h / h)
                new_w, new_h = int(w * scale), int(h * scale)
                resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
                canvas = cv2.copyMakeBorder(resized, 0, target_h - new_h, 0, target_w - new_w, cv2.BORDER_CONSTANT, value=(255, 255, 255))
                cv2.imwrite(str(dest), canvas, [cv2.IMWRITE_JPEG_QUALITY, 90])
                best_image = dest
                print(f"  FOUND {best_faces} face(s) in {url[:80]} -> saved to {dest.name}")
            else:
                print(f"  NO face in {url[:80]}")
            tmp_path.unlink(missing_ok=True)

        except Exception as e:
            print(f"  ERROR {url[:80]}: {e}")

    return best_image, best_faces


def main():
    print("=" * 60)
    print("Downloading and verifying judicial officer headshots")
    print("=" * 60)

    results = []
    for slug, info in CANDIDATES.items():
        print(f"\n--- {info['name']} ({slug}) ---")
        path, faces = download_and_verify(slug, info)
        results.append((slug, info["name"], path, faces))

    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    for slug, name, path, faces in results:
        status = f"SAVED ({path.name})" if path else "NO HEADSHOT FOUND"
        faces_str = f"{faces} face(s)" if faces else ""
        print(f"  {name:25s} -> {status} {faces_str}")

    print(f"\nHeadshots saved to: {HEADSHOTS_DIR.resolve()}")


if __name__ == "__main__":
    main()
