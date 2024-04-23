import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useEffect } from "react";

import Main from './components/Main';
import Login from "./views/Login";
import Courses from "./views/Courses";
import './App.css';

function App() {
  useEffect(() => {
    document.title = 'VPL IDE';
  }, []);

  return (
    <Router>
      <div className="mainWrapper">
        <Routes>
          <Route exact path="/login" element={<Login />} />
          <Route exact path="/courses" element={<Courses />} />
          <Route exact path="/" element={<Main />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
