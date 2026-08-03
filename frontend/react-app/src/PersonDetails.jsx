import { useEffect, useState } from "react";

import {
  Link,
  useParams
} from "react-router-dom";


export default function PersonDetails() {

  const { id } = useParams();

  const [person, setPerson] =
    useState(null);

  const [error, setError] =
    useState("");


  useEffect(() => {

    fetch(
      `http://127.0.0.1:8000/person/${id}`
    )

      .then(async (res) => {

        const data =
          await res.json();

        if (!res.ok) {

          throw new Error(
            data.detail
            || "Person not found"
          );

        }

        return data;

      })

      .then(data => {

        setPerson(data);

      })

      .catch(error => {

        setError(
          error.message
        );

      });

  }, [id]);


  if (error) {

    return (

      <div className="container mt-5">

        <Link
          to="/search"
          className="btn btn-outline-danger mb-3"
        >
          🔙 Back
        </Link>

        <div className="alert alert-danger">

          {error}

        </div>

      </div>

    );

  }


  if (!person) {

    return (

      <div className="container mt-5">

        <p>
          Loading...
        </p>

      </div>

    );

  }


  return (

    <div className="container mt-5">

      <Link
        to="/search"
        className="btn btn-outline-danger mb-3"
      >
        🔙 Back
      </Link>


      <div className="card shadow p-4 mx-auto"
        style={{ maxWidth: "600px" }}
      >


        <img
          src={
            `http://127.0.0.1:8000/${person.image_path}`
          }
          alt={person.full_name}
          className="img-fluid mb-4 mx-auto rounded"
          style={{
            width: "300px",
            height: "300px",
            objectFit: "cover"
          }}
        />


        <h3>
          {person.full_name}
        </h3>


        <hr />


        <p>

          <strong>
            Age:
          </strong>{" "}

          {person.age}

        </p>


        <p>

          <strong>
            Gender:
          </strong>{" "}

          {person.gender}

        </p>


        <p>

          <strong>
            Description:
          </strong>{" "}

          {person.description}

        </p>


        <p>

          <strong>
            Last Seen:
          </strong>{" "}

          {person.last_seen_location}

        </p>


        <div className="alert alert-info mt-3">

          <h5>
            Institution
          </h5>


          <p className="mb-1">

            <strong>
              Name:
            </strong>{" "}

            {person.institution.name}

          </p>


          <p className="mb-1">

            <strong>
              Type:
            </strong>{" "}

            {person.institution.type}

          </p>


          <p className="mb-1">

            <strong>
              Location:
            </strong>{" "}

            {person.institution.location}

          </p>


          {person.institution.contact && (

            <p className="mb-0">

              <strong>
                Contact:
              </strong>{" "}

              {person.institution.contact}

            </p>

          )}

        </div>


      </div>

    </div>

  );

}