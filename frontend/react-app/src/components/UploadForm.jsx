import { useState } from "react";

function UploadForm() {
  const [formData, setFormData] = useState({
    fullName: "",
    age: "",
    gender: "",
    description: "",
    lastSeenLocation: ""
  });

  const [photo, setPhoto] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData, //copies the existing data, w/o  it, updating input field erases the existing/previous data
      [e.target.name]: e.target.value, //updates whichever field is changed(input) i.e formData.fullName:"Ali.."
    });
  }

  const handPhotoChange = (e) => {
    setPhoto(e.target.files[0]); //e.target.files contains all files, [0]gets the first uploaded file
  }

  const handleSubmit = (e) => {
    e.preventDefault(); //avoids the page from refreshing

    console.log(formData);
    console.log(photo);
  }

return (
  <div className="container mt-5">
    <div className="card shadow p-4">
      <h2 className="mb-4 text-center">Prisoner Search Upload</h2>

      <form onSubmit={handleSubmit}>

        <div className="mb-3">
          <label className="form-label">Full Name</label>
          <input type="text" className="form-control" name="fullName" onChange={handleChange}/>
        </div>

        <div className="mb-3">
          <label className="form-label">Age</label>
          <input type="number" className="form-control" name="age" onChange={handleChange}/>
        </div>

        <div className="mb-3">
          <label className="form-label">Gender</label>
          <select className="form-select" name="gender" onChange={handleChange}>
            <option value="">Select Gender</option>
            <option>Male</option>
            <option>Female</option>
          </select>
        </div>

        <div className="mb-3">
          <label className="form-label">Physical Description</label>
          <textarea className="form-control" name="description" onChange={handleChange} rows="4" placeholder="Scars, height, tattoos..."></textarea>
        </div>

        <div className="mb-3">
          <label className="form-label">Last Seen Location</label>
          <input type="text" className="form-control" name="lastSeenLocation" onChange={handleChange}/>
        </div>

        <div className="mb-4">
          <label className="form-label">Upload Photo</label>
          <input type="file" className="form-control" accept="image/*" onChange={handPhotoChange}/>
        </div>

        <button type="submit" className="btn btn-primary w-100">Submit</button>

      </form>
    </div>
  </div>
)
}
export default UploadForm