import { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import LoginComponent from "./components/login-component";
import HomeComponent from "./homepage/home";
import AuthService from "./service/auth.service";
import SurgeyCalendar from "./homepage/surgery-calendar.";
import SurgeyForm from "./homepage/surgery-form";
import HomePage from "./homepage/home";


function App() {
  const [currentUser, setCurrentUser] = useState(AuthService.getCurrentUser());

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <Layout currentUser={currentUser} setCurrentUser={setCurrentUser} />
          }
        >
          <Route index element={<HomeComponent />}></Route>
          <Route
            path="login"
            element={
              <LoginComponent
                currentUser={currentUser}
                setCurrentUser={setCurrentUser}
              />
            }
          ></Route>
          <Route
                  path="/home"
                  element={<HomePage />}
                />
          {/* <Route
                  path="/surgey-calendar"
                  element={<SurgeyCalendar />}
                /> */}
          <Route
                  path="/surgey-form"
                  element={<SurgeyForm />}
                />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;