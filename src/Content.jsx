import React from 'react';
import "./index.css"
import { SiPython,SiJavascript, SiCplusplus, SiBlender, SiApachecordova, SiGithub } from "react-icons/si";
import { useRef, useState } from 'react';
import { useEffect } from 'react';
export const Content = () => {
    const navBar = useRef();
    const lineOne = useRef();
    const [navBarHeight, setNavBarHeight] = useState();
    const [lineOneOffset, setLineOneOffset] = useState();

    useEffect(()=>{
        setNavBarHeight(navBar.current.getBoundingClientRect().top);
        setLineOneOffset(lineOne.current.getBoundingClientRect().bottom);
    }, []);
   
    const calcTextContentMargin = ()=>{
        return lineOneOffset - navBarHeight;
    }
  return (
    <>
    <nav id="nav-bar" ref={navBar}>
    <img src="./pictures/mercedes.png" id="logo" alt=""></img>
    </nav>
    <header id="section-page">
        <aside>
            <div id="lineOne" ref={lineOne}></div>
            <div className="icons">
                <SiPython className='icon'/>
                <SiGithub className='icon'/>
                <SiJavascript className='icon'/>
                <SiCplusplus className='icon'/>
                <SiBlender className='icon'/>
                <SiApachecordova className='icon'/>
            </div>
            <div id="lineTwo"></div>
        </aside>
        <main id="text-content" style={{margin: `${calcTextContentMargin() -20}px 0 0 0`}}>
            <h1>Autonomous RC-Car</h1>
                    <p>The place where an idea meets three enthusiastic programmers,
                        with a passion for Formula 1 and a simple philosophy 
                        “We’ll succeed when everyone delivers their tenth of a second”.
                        Formula 1 is usually associated with massive machinery and
                        engineered insanity, we thought of fueling our passion 
                        for adrenaline by sharing our love to everyone who is
                        curious about our journey.</p>
                    <a href="#project-page" className="racing">GO RACING</a>
        </main>
    </header>
    </>
  )
}
