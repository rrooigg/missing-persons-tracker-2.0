from deepface import DeepFace
import numpy as np


def get_embedding(image_path):
  #Extract facial embedding from image.
  result = DeepFace.represent(
    img_path=image_path,
    model_name="ArcFace",
    enforce_detection=True
  )

  return result[0]["embedding"]


def cosine_similarity(embedding1, embedding2):
  #Returns similarity between 0 and 1. Higher means more similar.
  a = np.array(embedding1)
  b = np.array(embedding2)

  return np.dot(a, b) / (
    np.linalg.norm(a) * np.linalg.norm(b)
  )


def find_best_match(uploaded_embedding, prisoners):
  best_match = None
  best_score = 0

  for prisoner in prisoners:
    if prisoner.face_embedding is None:
      continue
    score = cosine_similarity(
      uploaded_embedding,
      prisoner.face_embedding
    )
    if score > best_score:
      best_score = score
      best_match = prisoner

  return best_match, best_score