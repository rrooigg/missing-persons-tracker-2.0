import UploadForm from "./UploadForm";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PersonDetails from "./PersonDetails";
import LandingPage from "./LandingPage";
import Dashboard from "./Dashboard";
import RegisterInstitution from "./RegisterInstitution";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/search" element={<UploadForm />} />
        <Route path="/person/:id" element={<PersonDetails />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/register-institution" element={<RegisterInstitution />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App 