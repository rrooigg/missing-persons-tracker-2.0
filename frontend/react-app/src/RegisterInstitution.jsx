import { useState } from "react";

import { Link, useNavigate } from "react-router-dom";


export default function RegisterInstitution() {

  const navigate = useNavigate();


  const [formData, setFormData] = useState({

    name: "",
    institution_type: "",
    location: "",
    contact: ""

  });


  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);


  const handleChange = (e) => {

    setFormData({

      ...formData,

      [e.target.name]:
        e.target.value

    });

  };


  const handleSubmit = async (e) => {

    e.preventDefault();

    setLoading(true);

    setMessage("");

    setError("");


    const data = new FormData();


    data.append(
      "name",
      formData.name
    );

    data.append(
      "institution_type",
      formData.institution_type
    );

    data.append(
      "location",
      formData.location
    );

    data.append(
      "contact",
      formData.contact
    );


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/institutions",
        {
          method: "POST",
          body: data
        }
      );


      const result =
        await response.json();


      if (!response.ok) {

        throw new Error(
          result.detail
          || "Registration failed."
        );

      }


      setMessage(
        "Institution registered successfully!"
      );


      setFormData({

        name: "",
        institution_type: "",
        location: "",
        contact: ""

      });


      setTimeout(() => {

        navigate("/dashboard");

      }, 1000);


    } catch (error) {

      setError(
        error.message
      );

    } finally {

      setLoading(false);

    }

  };


  return (

    <div className="container mt-5">

      <Link
        to="/dashboard"
        className="btn btn-outline-danger mb-3"
      >
        🔙 Back to Dashboard
      </Link>


      <div
        className="card shadow p-4 mx-auto"
        style={{ maxWidth: "600px" }}
      >

        <h2 className="mb-4">
          Register Institution
        </h2>


        {message && (

          <div className="alert alert-success">

            {message}

          </div>

        )}


        {error && (

          <div className="alert alert-danger">

            {error}

          </div>

        )}


        <form onSubmit={handleSubmit}>


          <div className="mb-3">

            <label className="form-label">

              Institution Name

            </label>

            <input
              type="text"
              className="form-control"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. Jela Baridi Prison"
              required
            />

          </div>


          <div className="mb-3">

            <label className="form-label">

              Institution Type

            </label>


            <select
              className="form-select"
              name="institution_type"
              value={formData.institution_type}
              onChange={handleChange}
              required
            >

              <option value="">
                Select institution type
              </option>

              <option value="Prison">
                Prison
              </option>

              <option value="Police">
                Police
              </option>

              <option value="Hospital">
                Hospital
              </option>

              <option value="School">
                School
              </option>

              <option value="Shelter">
                Shelter
              </option>

              <option value="Morgue">
                Morgue
              </option>

              <option value="Other">
                Other
              </option>

            </select>

          </div>


          <div className="mb-3">

            <label className="form-label">

              Location

            </label>

            <input
              type="text"
              className="form-control"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g. Mombasa"
              required
            />

          </div>


          <div className="mb-4">

            <label className="form-label">

              Contact

            </label>

            <input
              type="text"
              className="form-control"
              name="contact"
              value={formData.contact}
              onChange={handleChange}
              placeholder="Phone or official contact"
            />

          </div>


          <button
            type="submit"
            className="btn btn-danger w-100"
            disabled={loading}
          >

            {loading
              ? "Registering..."
              : "Register Institution"}

          </button>


        </form>

      </div>

    </div>

  );

}