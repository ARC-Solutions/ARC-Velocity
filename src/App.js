import React, {createContext} from "react";
import {BrowserRouter, Link, Route, Routes, useNavigate} from "react-router-dom"
import {FiPlay} from "react-icons/fi"
import {TbMinusVertical} from "react-icons/tb"
import {BsBoxArrowInRight} from "react-icons/bs"
import {HiMinus} from "react-icons/hi"
import { Content } from "./Content";
import {InfoSection} from "./InfoSection"
import { ActionSection } from "./ActionSection";
import {Info} from "./Info"
import {Action} from "./Action"
import video from "./videos/Hopium.mp4"
import logo from "./pictures/logo.png"
export const AppContext = createContext();
function App() {
  return (
   <AppContext.Provider value = {AppContext}>
    <BrowserRouter>
    <Routes>
    <Route path="/" element={
     <>    
        <div className="video-container">
            <video autoPlay muted loop className="video">
          <source  src={video} type="video/mp4"/>
        </video> 
      <div className="textContent">
        <div className="logo-container">
                <img src={logo} id="logo" alt="" />
        </div>
        <h1>Autonomous RC-Car</h1>
        <div className="navigation">
          <div className="watch-video">
            <FiPlay/>
            <h6>watch video</h6>
          </div>
          <TbMinusVertical style={{transform: "scale(2)"}}/>
          <Link to={"/landing-Page"} className="navigate-home">
          <BsBoxArrowInRight/>
            <h6>explore</h6>
          </Link>
          <div id="line"></div>
        </div>
      </div>

        </div>
    </>
        
      }/>
      <Route path="/landing-Page" element={
        <main id="landing-page">
    <div className="container content">
      <Content/>
    </div>
    </main>
      }/>
      <Route path="/manPage" element={
        <section id="project-page">
        <InfoSection/>
        <ActionSection/>
      </section>
      }/>
      <Route path="/autoPage" element={
        <section id="project-page">
        <Info/>
        <Action/>
      </section>
      }/>
      <Route path="*" element={
        <h1>Mark ist poop
        </h1>
      }/>

    </Routes>
    </BrowserRouter>
   </AppContext.Provider>
  );
}

export default App;
