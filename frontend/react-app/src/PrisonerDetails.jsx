import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

export default function PrisonerDetails() {
  const { id } = useParams();
  const [ prisoner, setPrisoner ] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/prisoner/${id}`)
    .then(res => res.json())
    .then(data => setPrisoner(data));
  }, [id]);

  if (!prisoner) {
    return <p>Loading...</p>
  }

  return (
    <div className="container mt-5">
      <div className="card p-4">
        <img src={`http://127.0.0.1:8000/${prisoner.image_path}`} alt="" className="img-fluid mb-3"/>
        <h3>{prisoner.full_name}</h3>
        <p>Age: {prisoner.age}</p>
        <p>Gender: {prisoner.gender}</p>
        <p>Description: {prisoner.description}</p>
        <p>Last Seen: {" "} {prisoner.last_seen_location}</p>
      </div>
    </div>
  );
}