import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Link } from "react-router-dom";

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
      <Link to="/search" className="btn btn-outline-danger mb-3">🔙Back</Link>
      <div className="card p-4 w-50 mx-auto">
        <img src={`https://missing-persons-tracker.onrender.com/${prisoner.image_path}`} alt="" className="img-fluid mb-3 mx-auto rounded" style={{width:"300px"}}/>
        <h3>{prisoner.full_name}</h3>
        <p>Age: {prisoner.age}</p>
        <p>Gender: {prisoner.gender}</p>
        <p>Description: {prisoner.description}</p>
        <p>Last Seen: {" "} {prisoner.last_seen_location}</p>
      </div>
    </div>
  );
}