import { Link } from "react-router-dom";
import hero from "./assets/hero.jpg";
import why_matters from "./assets/why_matters.jpg";
import search from "./assets/search.jpg";

export default function LandingPage() {
  return (
    <>
      {/* NAVBAR */}
      <nav
        className="navbar navbar-expand-lg navbar-dark fixed-top"
        style={{
          backgroundColor: "#8B0000",
        }}
      >
        <div className="container">
          <span className="navbar-brand fw-bold">
            Missing Persons Tracker
          </span>

          <Link
            to="/search"
            className="btn btn-light text-danger fw-bold"
          >
            Search Now
          </Link>
        </div>
      </nav>

      {/* HERO */}
      <section
        style={{
          minHeight: "100vh",
          backgroundImage:
            `linear-gradient(rgba(0,0,0,.65), rgba(0,0,0,.65)), url(${hero})`,
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
          backgroundPosition: "center",
          display: "flex",
          alignItems: "center",
        }}
      >
        <div className="container text-center text-white">
          <h1
            className="fw-bold mb-4"
            style={{
              fontSize: "4rem",
            }}
          >
            Reconnecting Families Through
            Intelligent Facial Recognition
          </h1>

          <p
            className="lead mb-5 mx-auto"
            style={{
              maxWidth: "800px",
            }}
          >
            Our platform uses facial recognition technology to help
            identify missing persons by comparing uploaded photos
            against registered records.
          </p>
          <Link
            to="/search"
            className="btn btn-lg px-5 py-3 fw-bold text-white"
            style={{backgroundColor: "#8B0000"}}>
            Start Search
          </Link>
          <Link
          to="/dashboard"
          className="btn btn-lg px-5 py-3 fw-bold text-white ms-4"
          style={{backgroundColor: "#8B0000"}}
        >
          Dashboard
        </Link>
        </div>
      </section>

      {/* WHAT WE DO */}
      <section className="py-5">
        <div className="container py-5">

          <h2 className="text-center fw-bold mb-5">
            What We Do
          </h2>

          <div className="row g-4">

            <div className="col-md-4">
              <div
                className="card h-100 border-0 shadow"
                style={{
                  backgroundColor: "#fff",
                  minHeight: "250px",
                }}
              >
                <div className="card-body p-4">
                  <h4 className="text-danger mb-3">
                    Upload Images
                  </h4>

                  <p>
                    Submit a photograph of a person you wish
                    to identify through our secure search system.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-md-4">
              <div
                className="card h-100 border-0 shadow text-white"
                style={{
                  backgroundColor: "#B22222",
                  minHeight: "250px",
                }}
              >
                <div className="card-body p-4">
                  <h4>
                    AI Recognition
                  </h4>

                  <p>
                    Advanced facial recognition extracts unique
                    facial features from uploaded photographs.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-md-4">
              <div
                className="card h-100 border-0 shadow"
                style={{
                  minHeight: "250px",
                }}
              >
                <div className="card-body p-4">
                  <h4 className="text-danger">
                    Match Results
                  </h4>

                  <p>
                    Potential matches are presented instantly,
                    helping families and investigators obtain
                    critical information faster.
                  </p>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* WHY IT MATTERS */}
      <section
        style={{
          minHeight: "80vh",
          backgroundImage:
            `linear-gradient(rgba(0,0,0,.70), rgba(0,0,0,.70)), url(${why_matters})`,
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <div className="container py-5 text-white">

          <div
            className="d-flex flex-column justify-content-center"
            style={{
              minHeight: "80vh",
            }}
          >
            <h2 className="fw-bold mb-4">
              Why This Matters
            </h2>

            <p
              className="lead"
              style={{
                maxWidth: "800px",
              }}
            >
              Every missing person represents a family searching
              for answers. Traditional methods can be slow and
              resource-intensive. Our platform leverages modern
              facial recognition technology to accelerate the
              identification process and support reunification
              efforts.
            </p>
          </div>

        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="py-5">
        <div className="container py-5">

          <h2 className="text-center fw-bold mb-5">
            How It Works
          </h2>

          <div className="row g-4">

            <div className="col-md-3">
              <div
                className="card text-center border-0 shadow"
                style={{
                  minHeight: "280px",
                }}
              >
                <div className="card-body d-flex flex-column justify-content-center">
                  <h1 className="text-danger">1</h1>
                  <h5>Upload</h5>
                  <p>Upload a facial image.</p>
                </div>
              </div>
            </div>

            <div className="col-md-3">
              <div
                className="card text-center border-0 shadow text-white"
                style={{
                  backgroundColor: "#B22222",
                  minHeight: "280px",
                }}
              >
                <div className="card-body d-flex flex-column justify-content-center">
                  <h1>2</h1>
                  <h5>Detect</h5>
                  <p>Locate and extract facial features.</p>
                </div>
              </div>
            </div>

            <div className="col-md-3">
              <div
                className="card text-center border-0 shadow"
                style={{
                  minHeight: "280px",
                }}
              >
                <div className="card-body d-flex flex-column justify-content-center">
                  <h1 className="text-danger">3</h1>
                  <h5>Compare</h5>
                  <p>Search the database for matches.</p>
                </div>
              </div>
            </div>

            <div className="col-md-3">
              <div
                className="card text-center border-0 shadow text-white"
                style={{
                  backgroundColor: "#B22222",
                  minHeight: "280px",
                }}
              >
                <div className="card-body d-flex flex-column justify-content-center">
                  <h1>4</h1>
                  <h5>Identify</h5>
                  <p>Review matching records instantly.</p>
                </div>
              </div>
            </div>

          </div>

        </div>
      </section>

      {/* BENEFITS */}
      <section
        style={{
          minHeight: "80vh",
          backgroundImage:
            `linear-gradient(rgba(255,255,255,.90), rgba(255,255,255,.90)), url(${search})`,
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover", 
          backgroundPosition: "center",
        }}
      >
        <div className="container py-5">

          <h2 className="text-center fw-bold mb-5">
            Key Benefits
          </h2>

          <div className="row g-4">

            <div className="col-md-4">
              <div className="card border-0 shadow h-100">
                <div className="card-body p-4">
                  <h4 className="text-danger">
                    Faster Searches
                  </h4>

                  <p>
                    Automated matching significantly reduces
                    identification time.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-md-4">
              <div
                className="card border-0 shadow text-white h-100"
                style={{
                  backgroundColor: "#B22222",
                }}
              >
                <div className="card-body p-4">
                  <h4>
                    Improved Accuracy
                  </h4>

                  <p>
                    AI-powered recognition reduces human error
                    during identification.
                  </p>
                </div>
              </div>
            </div>

            <div className="col-md-4">
              <div className="card border-0 shadow h-100">
                <div className="card-body p-4">
                  <h4 className="text-danger">
                    Accessible
                  </h4>

                  <p>
                    Available through a simple web interface
                    accessible from anywhere.
                  </p>
                </div>
              </div>
            </div>

          </div>

        </div>
      </section>

      {/* CTA */}
      <section
        style={{
          backgroundColor: "#8B0000",
        }}
        className="py-5 text-white"
      >
        <div className="container text-center py-5">

          <h2 className="fw-bold mb-4">
            Ready to Begin Your Search?
          </h2>

          <p className="lead mb-4">
            Upload a photograph and let our system help identify
            potential matches.
          </p>

          <Link
            to="/search"
            className="btn btn-light text-danger btn-lg px-5 fw-bold"
          >
            Start Search
          </Link>

        </div>
      </section>

      {/* FOOTER */}
      <footer
        className="text-center fw-bold py-4"
      >
        <p className="mb-0">
          © 2026 Missing Persons Tracker
        </p>
      </footer>
    </>
  );
}