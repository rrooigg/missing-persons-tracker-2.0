import { useEffect, useState } from "react";
import { Link } from "react-router-dom";


export default function Dashboard() {

  const [institutions, setInstitutions] = useState([]);
  const [stats, setStats] = useState({
    institutions_count: 0,
    people_count: 0,
    by_type: {}
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");


  useEffect(() => {

    const loadDashboard = async () => {

      try {

        const institutionsResponse = await fetch(
          "http://127.0.0.1:8000/institutions"
        );

        const statsResponse = await fetch(
          "http://127.0.0.1:8000/dashboard/stats"
        );


        if (!institutionsResponse.ok) {
          throw new Error(
            `Institutions request failed: ${institutionsResponse.status}`
          );
        }

        if (!statsResponse.ok) {
          throw new Error(
            `Stats request failed: ${statsResponse.status}`
          );
        }


        const institutionsData =
          await institutionsResponse.json();

        const statsData =
          await statsResponse.json();


        console.log(
          "INSTITUTIONS API:",
          institutionsData
        );

        console.log(
          "STATS API:",
          statsData
        );


        setInstitutions(
          Array.isArray(institutionsData)
            ? institutionsData
            : []
        );


        setStats({
          institutions_count:
            Number(statsData.institutions_count) || 0,

          people_count:
            Number(statsData.people_count) || 0,

          by_type:
            statsData.by_type &&
            typeof statsData.by_type === "object"
              ? statsData.by_type
              : {}
        });


      } catch (error) {

        console.error(
          "Dashboard error:",
          error
        );

        setError(
          error.message ||
          "Failed to load dashboard."
        );

      } finally {

        setLoading(false);

      }

    };


    loadDashboard();

  }, []);


  if (loading) {

    return (

      <div className="container mt-5">

        <div className="text-center">

          <div
            className="spinner-border text-danger"
            role="status"
          />

          <p className="mt-3">
            Loading dashboard...
          </p>

        </div>

      </div>

    );

  }


  if (error) {

    return (

      <div className="container mt-5">

        <Link
          to="/"
          className="btn btn-outline-danger mb-3"
        >
          🔙 Back
        </Link>


        <div className="alert alert-danger">

          <h4>
            Dashboard Error
          </h4>

          <p className="mb-0">
            {error}
          </p>

          <hr />

          <p className="mb-0">

            Make sure your FastAPI backend
            is running on port 8000.

          </p>

        </div>

      </div>

    );

  }


  return (

    <div className="container mt-5">


      {/* HEADER */}

      <div className="d-flex justify-content-between align-items-center mb-4">

        <div>

          <h1>
            Dashboard
          </h1>

          <p className="text-muted">
            Missing Persons Tracker
          </p>

        </div>


        <div>

          <Link
            to="/"
            className="btn btn-outline-danger me-2"
          >
            Home
          </Link>


          <Link
            to="/register-institution"
            className="btn btn-danger"
          >
            Register Institution
          </Link>

        </div>

      </div>


      {/* STATISTICS */}

      <div className="row mb-5">


        <div className="col-md-4 mb-3">

          <div className="card shadow-sm h-100">

            <div className="card-body">

              <h6 className="text-muted">
                Registered Institutions
              </h6>

              <h1>
                {stats.institutions_count}
              </h1>

            </div>

          </div>

        </div>


        <div className="col-md-4 mb-3">

          <div className="card shadow-sm h-100">

            <div className="card-body">

              <h6 className="text-muted">
                Total Records
              </h6>

              <h1>
                {stats.people_count}
              </h1>

            </div>

          </div>

        </div>


        <div className="col-md-4 mb-3">

          <div className="card shadow-sm h-100">

            <div className="card-body">

              <h6 className="text-muted">
                Institution Types
              </h6>

              <h1>
                {
                  Object.keys(
                    stats.by_type
                  ).length
                }
              </h1>

            </div>

          </div>

        </div>

      </div>


      {/* INSTITUTIONS */}

      <div className="card shadow-sm">

        <div className="card-header">

          <h4 className="mb-0">
            Registered Institutions
          </h4>

        </div>


        <div className="card-body p-0">

          <div className="table-responsive">

            <table className="table table-hover mb-0">

              <thead>

                <tr>

                  <th>
                    Institution
                  </th>

                  <th>
                    Type
                  </th>

                  <th>
                    Location
                  </th>

                  <th>
                    Records
                  </th>

                </tr>

              </thead>


              <tbody>

                {institutions.map(
                  (institution) => (

                    <tr
                      key={institution.id}
                    >

                      <td>

                        <strong>

                          {String(
                            institution.name ?? ""
                          )}

                        </strong>

                      </td>


                      <td>

                        <span className="badge bg-secondary">

                          {String(
                            institution.institution_type ?? ""
                          )}

                        </span>

                      </td>


                      <td>

                        {String(
                          institution.location ?? ""
                        )}

                      </td>


                      <td>

                        <strong>

                          {Number(
                            institution.people_count
                          ) || 0}

                        </strong>

                      </td>

                    </tr>

                  )
                )}


                {institutions.length === 0 && (

                  <tr>

                    <td
                      colSpan="4"
                      className="text-center p-4"
                    >

                      No institutions registered yet.

                    </td>

                  </tr>

                )}

              </tbody>

            </table>

          </div>

        </div>

      </div>


      {/* RECORDS BY TYPE */}

      <div className="card shadow-sm mt-4 mb-5">

        <div className="card-body">

          <h4>
            Records by Institution Type
          </h4>


          <div className="row mt-3">

            {Object.entries(
              stats.by_type
            ).map(
              ([type, count]) => (

                <div
                  className="col-md-3 mb-3"
                  key={type}
                >

                  <div className="border rounded p-3">

                    <h6>
                      {String(type)}
                    </h6>

                    <h3>
                      {Number(count) || 0}
                    </h3>

                    <small className="text-muted">
                      records
                    </small>

                  </div>

                </div>

              )
            )}

          </div>

        </div>

      </div>


    </div>

  );

}