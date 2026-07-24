from deepface import DeepFace
import tensorflow as tf
import gc

def get_face_embedding(image_path: str):
  try:
    results = DeepFace.represent(
      img_path=image_path,
      model_name="Facenet",  # Generates 128 floats
      detector_backend="opencv",
      enforce_detection=False
    )
    if results and len(results) > 0:
      return results[0]["embedding"]
    return None
  except Exception as e:
    print(f"Error extracting embedding: {e}")
    return None
  finally:
    tf.keras.backend.clear_session()
    gc.collect()