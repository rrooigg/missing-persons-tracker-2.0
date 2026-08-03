import { useState } from "react";

import {
  FaCheckCircle,
  FaTimesCircle
} from "react-icons/fa";

import { Link } from "react-router-dom";


function UploadForm() {

  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState(null);

  const [error, setError] = useState("");

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

      ...formData,

      [e.target.name]: e.target.value

    });

  };


  const handlePhotoChange = (e) => {

    setPhoto(
      e.target.files[0]
    );

  };


  const handleSubmit = async (e) => {

    e.preventDefault();

    setLoading(true);

    setResult(null);

    setError("");


    if (!photo) {

      setError(
        "Please upload a photo."
      );

      setLoading(false);

      return;

    }


    const data = new FormData();


    data.append(
      "fullName",
      formData.fullName
    );

    data.append(
      "age",
      formData.age
    );

    data.append(
      "gender",
      formData.gender
    );

    data.append(
      "description",
      formData.description
    );

    data.append(
      "lastSeenLocation",
      formData.lastSeenLocation
    );

    data.append(
      "file",
      photo
    );


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: data
        }
      );


      const responseData =
        await response.json();


      if (!response.ok) {

        throw new Error(
          responseData.detail
          || "Something went wrong."
        );

      }


      setResult(responseData);


    } catch (error) {

      console.error(error);

      setError(
        error.message
        || "Unable to search."
      );


    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="container mt-5">

      <Link
        to="/"
        className="btn btn-outline-danger mb-3"
      >
        🔙 Back
      </Link>


      <div className="card shadow p-4 w-50 mx-auto">

        <h2 className="mb-4 text-center">
          Missing Person Search
        </h2>


        {error && (

          <div className="alert alert-danger">

            <FaTimesCircle className="me-2" />

            {error}

          </div>

        )}


        {result && result.match_found && (

          <div className="alert alert-success">

            <div className="d-flex align-items-center">

              <FaCheckCircle
                size={30}
                className="me-2"
              />

              <strong>
                Match Found!
              </strong>

            </div>


            <hr />


            <p className="mb-1">

              <strong>
                Name:
              </strong>{" "}

              {result.matched_name}

            </p>


            <p className="mb-1">

              <strong>
                Similarity:
              </strong>{" "}

              {(
                100 -
                result.distance * 100
              ).toFixed(1)}
              %

            </p>


            <p className="mb-1">

              <strong>
                Institution:
              </strong>{" "}

              {result.institution.name}

            </p>


            <p className="mb-1">

              <strong>
                Type:
              </strong>{" "}

              {result.institution.type}

            </p>


            <p>

              <strong>
                Location:
              </strong>{" "}

              {result.institution.location}

            </p>


            <Link
              to={`/person/${result.matched_id}`}
              className="btn btn-success mt-2"
            >
              See More Information
            </Link>

          </div>

        )}


        {result && !result.match_found && (

          <div className="alert alert-danger">

            <FaTimesCircle
              size={30}
              className="me-2"
            />

            <strong>
              No Match Found
            </strong>

            <p className="mb-0 mt-2">
              No matching record was found
              across the registered institutions.
            </p>

          </div>

        )}


        <form onSubmit={handleSubmit}>


          <div className="mb-3">

            <label className="form-label">
              Full Name
            </label>

            <input
              type="text"
              className="form-control"
              name="fullName"
              value={formData.fullName}
              onChange={handleChange}
              required
            />

          </div>


          <div className="mb-3">

            <label className="form-label">
              Age
            </label>

            <input
              type="number"
              className="form-control"
              name="age"
              value={formData.age}
              onChange={handleChange}
              required
            />

          </div>


          <div className="mb-3">

            <label className="form-label">
              Gender
            </label>

            <select
              className="form-select"
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              required
            >

              <option value="">
                Select Gender
              </option>

              <option value="Male">
                Male
              </option>

              <option value="Female">
                Female
              </option>

            </select>

          </div>


          <div className="mb-3">

            <label className="form-label">
              Physical Description
            </label>

            <textarea
              className="form-control"
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows="4"
              placeholder="Scars, height, tattoos..."
              required
            />

          </div>


          <div className="mb-3">

            <label className="form-label">
              Last Seen Location
            </label>

            <input
              type="text"
              className="form-control"
              name="lastSeenLocation"
              value={formData.lastSeenLocation}
              onChange={handleChange}
              required
            />

          </div>


          <div className="mb-4">

            <label className="form-label">
              Upload Photo
            </label>

            <input
              type="file"
              className="form-control"
              accept="image/*"
              onChange={handlePhotoChange}
              required
            />

          </div>


          <button
            type="submit"
            className="btn btn-danger w-100"
            disabled={loading}
          >

            {loading
              ? "Searching All Institutions..."
              : "Search"}

          </button>


        </form>

      </div>

    </div>

  );

}


export default UploadForm;