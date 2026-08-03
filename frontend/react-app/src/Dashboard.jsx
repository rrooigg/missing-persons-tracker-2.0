import { useEffect, useState } from "react";

import { Link } from "react-router-dom";


export default function Dashboard() {

  const [institutions, setInstitutions] =
    useState([]);

  const [stats, setStats] =
    useState(null);

  const [loading, setLoading] =
    useState(true);


  useEffect(() => {

    Promise.all([

      fetch(
        "http://127.0.0.1:8000/institutions"
      ).then(res => res.json()),

      fetch(
        "http://127.0.0.1:8000/dashboard/stats"
      ).then(res => res.json())

    ])

      .then(([institutionData, statsData]) => {

        setInstitutions(
          institutionData
        );

        setStats(
          statsData
        );

      })

      .catch(error => {

        console.error(
          "Dashboard error:",
          error
        );

      })

      .finally(() => {

        setLoading(false);

      });

  }, []);


  if (loading) {

    return (

      <div className="container mt-5">

        <h3>
          Loading Dashboard...
        </h3>

      </div>

    );

  }


  return (

    <div className="container mt-5">


      <div className="d-flex justify-content-between align-items-center mb-4">

        <div>

          <h1>
            Admin Dashboard
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

          <div className="card shadow-sm p-4">

            <h6 className="text-muted">
              Registered Institutions
            </h6>

            <h1>
              {stats?.institutions_count || 0}
            </h1>

          </div>

        </div>


        <div className="col-md-4 mb-3">

          <div className="card shadow-sm p-4">

            <h6 className="text-muted">
              Total Records
            </h6>

            <h1>
              {stats?.people_count || 0}
            </h1>

          </div>

        </div>


        <div className="col-md-4 mb-3">

          <div className="card shadow-sm p-4">

            <h6 className="text-muted">
              Institution Types
            </h6>

            <h1>
              {
                Object.keys(
                  stats?.by_type || {}
                ).length
              }
            </h1>

          </div>

        </div>


      </div>


      {/* INSTITUTION TABLE */}

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
                    Registered Records
                  </th>

                </tr>

              </thead>


              <tbody>

                {institutions.map(
                  institution => (

                    <tr
                      key={institution.id}
                    >

                      <td>

                        <strong>
                          {institution.name}
                        </strong>

                      </td>


                      <td>

                        <span className="badge bg-secondary">

                          {
                            institution.institution_type
                          }

                        </span>

                      </td>


                      <td>
                        {institution.location}
                      </td>


                      <td>

                        <strong>
                          {
                            institution.people_count
                          }
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

                      No institutions
                      registered yet.

                    </td>

                  </tr>

                )}

              </tbody>

            </table>

          </div>

        </div>

      </div>


      {/* TYPE SUMMARY */}

      <div className="card shadow-sm mt-4">

        <div className="card-body">

          <h4>
            Records by Institution Type
          </h4>

          <div className="row mt-3">

            {Object.entries(
              stats?.by_type || {}
            ).map(
              ([type, count]) => (

                <div
                  className="col-md-3 mb-3"
                  key={type}
                >

                  <div className="border rounded p-3">

                    <h6>
                      {type}
                    </h6>

                    <h3>
                      {count}
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