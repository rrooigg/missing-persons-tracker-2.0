import UploadForm from "./UploadForm";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PrisonerDetails from "./PrisonerDetails";
import LandingPage from "./LandingPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/search" element={<UploadForm />} />
        <Route path="/prisoner/:id" element={<PrisonerDetails />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App 