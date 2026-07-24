import gc
from deepface import DeepFace
import tf_keras as keras

def verify_faces(img1_path: str, img2_path: str) -> bool:
    """
    Compares two face images directly using DeepFace.verify().
    Returns True if the faces match, False otherwise.
    """
    try:
        result = DeepFace.verify(
            img1_path=img1_path,
            img2_path=img2_path,
            model_name="Facenet",
            detector_backend="opencv",
            enforce_detection=False
        )
        
        # 'verified' is a boolean returned by DeepFace indicating a match
        return result.get("verified", False)

    except Exception as e:
        print(f"Error verifying faces between '{img1_path}' and '{img2_path}': {e}")
        return False
    finally:
        # Clean up session memory after each run
        keras.backend.clear_session()
        gc.collect()