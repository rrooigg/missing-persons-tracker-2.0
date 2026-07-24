from deepface import DeepFace


def verify_faces(uploaded_image_path, stored_image_path):
  result = DeepFace.verify(
    img1_path=uploaded_image_path,
    img2_path=stored_image_path,
    model_name="Facenet",
    detector_backend="opencv",
    enforce_detection=False
  )
  return (
    result["verified"],
    result["distance"],
    result["threshold"]
  )