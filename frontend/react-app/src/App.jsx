import UploadForm from "./UploadForm";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrisonerDetails from "./PrisonerDetails";
import LandingPage from "./LandingPage";
import Dashboard from "./Dashboard";
import RegisterInstitution from "./RegisterInstitution";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/search" element={<UploadForm />} />
        <Route path="/prisoner/:id" element={<PrisonerDetails />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/register-institution" element={<RegisterInstitution />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App 