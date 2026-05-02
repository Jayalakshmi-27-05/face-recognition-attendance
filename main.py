from attendance import mark_attendance
import cv2
import pickle
import numpy as np
from deepface import DeepFace

# Load dataset
with open("face_db.pkl", "rb") as f:
    data = pickle.load(f)

db_embeddings = np.array(data["embeddings"])
db_names = np.array(data["names"])

# Normalize database
db_embeddings = db_embeddings / np.linalg.norm(db_embeddings, axis=1, keepdims=True)

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

print("System Running ✔ Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    name = "Unknown"

    try:
        faces = DeepFace.extract_faces(
            frame,
            detector_backend="opencv",
            enforce_detection=False
        )

        if len(faces) > 0:
            face_img = faces[0]["face"]

            emb = DeepFace.represent(
                face_img,
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"]

            emb = np.array(emb)
            emb = emb / np.linalg.norm(emb)

            # 🔥 KNN STYLE MATCHING (NO FIXED THRESHOLD)
            distances = np.linalg.norm(db_embeddings - emb, axis=1)

            idx = np.argsort(distances)[0]   # best match
            best_distance = distances[idx]

            second_best = np.argsort(distances)[1]  # second best

            # 🔥 CONFIDENCE RULE (IMPORTANT FIX)
            if best_distance < 0.9 and (second_best - best_distance) > 0.05:
                name = db_names[idx]
                mark_attendance(name)   # ✅ AUTO SAVE

    except:
        pass

    cv2.putText(frame, name, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
