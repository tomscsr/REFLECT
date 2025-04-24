import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk # type: ignore
from PIL import Image, ImageTk # type: ignore
import cv2 # type: ignore
import mediapipe as mp # type: ignore
import numpy as np # type: ignore
from sklearn.cluster import KMeans # type: ignore

# Initialisation
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
cap = cv2.VideoCapture(0)
running = False
show_recommendations = False
current_reco = []

product_links = {
    "Hydratant SPF 50": "https://www.sephora.fr/p/creme-solaire-spf-50",
    "Fond de teint rosé": "https://www.nocibe.fr/fond-de-teint-rose",
    "Sérum vitamine C": "https://www.theordinary.com/fr/serum-vitamin-c",
    "BB crème ton neutre": "https://www.lorealparis.fr/bb-creme",
    "Contour stick caramel": "https://www.sephora.fr/contour-stick",
    "Crème hydratante équilibrante": "https://www.yves-rocher.fr/creme-equilibrante",
    "Fond de teint chocolat": "https://www.fentybeauty.com/fond-de-teint",
    "Illuminateur or": "https://www.kiko-milano.fr/illuminateur",
    "Crème riche au beurre de karité": "https://www.loccitane.com/fr-fr/beurre-karite",
    "Contour fin": "https://www.nyxcosmetics.fr/contour",
    "Highlighter pommettes": "https://www.sephora.fr/highlighter",
    "Blush vertical": "https://www.sephora.fr/blush",
    "Produits universels": "https://www.nocibe.fr/maquillage-universel",
    "Liner en V": "https://www.kiko-milano.fr/liner",
    "Rouge à lèvres tous styles": "https://www.lorealparis.fr/rouge-a-levres",
    "Blush horizontal": "https://www.sephora.fr/blush",
    "Bronzer tempes": "https://www.kiko-milano.fr/bronzer",
    "Highlight bas du visage": "https://www.fentybeauty.com/highlighter"
}

def detect_face_shape(landmarks):
    jaw = [landmarks[i] for i in range(0, 17)]
    jaw_width = np.linalg.norm(np.array(jaw[0]) - np.array(jaw[-1]))
    forehead_to_chin = np.linalg.norm(np.array(landmarks[10]) - np.array(landmarks[152]))
    ratio = jaw_width / forehead_to_chin
    if ratio > 1.05:
        return "Visage rond"
    elif 0.9 < ratio <= 1.05:
        return "Visage ovale"
    else:
        return "Visage long / rectangulaire"

def extract_skin_tone(image):
    h, w, _ = image.shape
    center = image[h//2-30:h//2+30, w//2-30:w//2+30]
    pixels = center.reshape(-1, 3)
    kmeans = KMeans(n_clusters=1, n_init=10)
    kmeans.fit(pixels)
    dominant_color = kmeans.cluster_centers_[0].astype(int)
    r, g, b = dominant_color
    if r > 110:
        return "Peau claire"
    elif 60 < r <= 110:
        return "Peau médium"
    else:
        return "Peau foncée"

def recommend_products(shape, tone):
    base = {
        "Peau claire": ["Hydratant SPF 50", "Fond de teint rosé", "Sérum vitamine C"],
        "Peau médium": ["BB crème ton neutre", "Contour stick caramel", "Crème hydratante équilibrante"],
        "Peau foncée": ["Fond de teint chocolat", "Illuminateur or", "Crème riche au beurre de karité"]
    }
    shape_products = {
        "Visage rond": ["Contour fin", "Highlighter pommettes", "Blush vertical"],
        "Visage ovale": ["Produits universels", "Liner en V", "Rouge à lèvres tous styles"],
        "Visage long / rectangulaire": ["Blush horizontal", "Bronzer tempes", "Highlight bas du visage"]
    }
    return base.get(tone, []) + shape_products.get(shape, [])

def analyse_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    shape, tone, reco = "Non détecté", "Non détecté", []
    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]
        h, w, _ = frame.shape
        landmarks = [(int(pt.x * w), int(pt.y * h)) for pt in face_landmarks.landmark]
        shape = detect_face_shape(landmarks)
        tone = extract_skin_tone(frame)
        reco = recommend_products(shape, tone)
    return shape, tone, reco

def update_video():
    ret, frame = cap.read()
    if not ret:
        return
    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    height = webcam_label.winfo_height()
    width = webcam_label.winfo_width()
    if height > 0 and width > 0:
        pass
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    webcam_label.imgtk = imgtk
    webcam_label.configure(image=imgtk)
    root.after(30, update_video)

def update_analysis():
    global current_reco
    if not show_recommendations:
        overlay_text.set("Cliquez sur 'Démarrer l'analyse' pour obtenir vos recommandations beauté ✨")
    else:
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            shape, tone, reco = analyse_frame(frame)
            if reco:
                current_reco = reco
                msg = f"\n💁‍♀️ Forme : {shape}\n🎨 Carnation : {tone}\n\n"
                msg += "\n".join([f"💄 {r}" for r in reco])
            else:
                dots = [".", "..", "..."]
                update_analysis.anim_state = (update_analysis.anim_state + 1) % 3
                msg = f"🔍 Analyse en cours{dots[update_analysis.anim_state]}\nMerci de regarder la caméra."
            overlay_text.set(msg)
    root.after(1000, update_analysis)
update_analysis.anim_state = 0

def start_analysis():
    global show_recommendations
    show_recommendations = True
    overlay_text.set("🔍 Analyse en cours...")

def reset_analysis():
    global show_recommendations, current_reco
    show_recommendations = False
    current_reco = []
    overlay_text.set("Cliquez sur 'Démarrer l'analyse' pour obtenir vos recommandations beauté ✨")

def show_shopping_list():
    if current_reco:
        items = "\n".join([f"- {item} ({product_links.get(item, 'lien indisponible')})" for item in current_reco])
        messagebox.showinfo("🛒 Liste de courses beauté", f"Voici votre liste :\n\n{items}")
    else:
        messagebox.showwarning("Aucune recommandation", "Veuillez lancer l'analyse avant de générer la liste de courses.")

def save_txt_file():
    if not current_reco:
        messagebox.showwarning("Aucune recommandation", "Veuillez d'abord lancer l'analyse.")
        return
    with open("recommandations.txt", "w", encoding="utf-8") as f:
        f.write("Liste de produits beauté recommandés :\n\n")
        for item in current_reco:
            f.write(f"- {item} : {product_links.get(item, 'lien indisponible')}\n")
    messagebox.showinfo("✅ Fichier enregistré", "La liste a été enregistrée sous 'recommandations.txt'.")

# Interface
root = ThemedTk(theme="arc")
root.title("REFLECT Project")
root.configure(bg="black")
root.geometry("1200x700")

main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True)

webcam_frame = tk.Frame(main_frame, bg="black")
webcam_frame.pack(side="left", fill="both", expand=True)
webcam_label = tk.Label(webcam_frame, bg="black")
webcam_label.pack(fill="both", expand=True)

right_panel = tk.Frame(main_frame, bg="black")
right_panel.pack(side="right", fill="y", padx=20, pady=40)

overlay_text = tk.StringVar()
overlay_label = tk.Label(right_panel, textvariable=overlay_text, font=("Helvetica", 16), bg="black", fg="white", justify="left", wraplength=400)
overlay_label.config(padx=20, pady=10, borderwidth=2, relief="ridge")
overlay_label.pack(pady=20, fill="both", expand=True)

ttk.Button(right_panel, text="Démarrer l'analyse", command=start_analysis).pack(pady=10, fill="x")
ttk.Button(right_panel, text="Réinitialiser", command=reset_analysis).pack(pady=10, fill="x")
ttk.Button(right_panel, text="🛍 Voir la liste de courses", command=show_shopping_list).pack(pady=10, fill="x")
ttk.Button(right_panel, text="💾 Enregistrer en .txt", command=save_txt_file).pack(pady=10, fill="x")

update_video()
update_analysis()
root.mainloop()

if cap:
    cap.release()
cv2.destroyAllWindows()
