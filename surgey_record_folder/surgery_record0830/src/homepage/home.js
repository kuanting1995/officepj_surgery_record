import React from "react";
import LoginComponent from "../components/login-component";
import { COLORS } from "../utils/color";
import 'bootstrap/dist/css/bootstrap.min.css';
import SurgeryCalendar from "./surgery-calendar.";
import '../styles/main.css';
import Sidebar from "./sidebar";
import NavComponent from "../components/nav-component";




const HomePage = () => {
  
  return (
 <>
 <div style={{ display: "flex", justifyContent: "space-between", height: 'auto'}}>
  {/* <div className="sidebar">
  <Sidebar/>
  </div> */}
  <div style={{ width: '100%',height: 'auto', maxHeight: '100vh' }}>
  <SurgeryCalendar/>
  </div>
  </div>
 </>
  );
};

export default HomePage;