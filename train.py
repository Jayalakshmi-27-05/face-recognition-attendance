import os
import numpy as np
import pickle
from deepface import DeepFace

dataset_path = "dataset"

embeddings = []
names = []

print("STRICT TRAINING STARTED 🧠")

for person in os.listdir(dataset_path):

    person_path = os.path.join(dataset_path, person)

    if not os.path.isdir(person_path):
        continue

    print("Processing:", person)

    for img in os.listdir(person_path):

        img_path = os.path.join(person_path, img)

        try:
            # 🔥 FORCE FACE DETECTION (CRITICAL FIX)
            face_objs = DeepFace.extract_faces(
                img_path,
                detector_backend="opencv",
                enforce_detection=True
            )

            if len(face_objs) == 0:
                continue

            face_img = face_objs[0]["face"]

            emb = DeepFace.represent(
                face_img,
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"]

            emb = np.array(emb)
            emb = emb / np.linalg.norm(emb)

            embeddings.append(emb)
            names.append(person)

        except:
            print("Skipped:", img_path)

print("Total embeddings:", len(embeddings))

data = {
    "embeddings": np.array(embeddings),
    "names": names
}

with open("face_db.pkl", "wb") as f:
    pickle.dump(data, f)

print("TRAINING COMPLETE ✔")    
