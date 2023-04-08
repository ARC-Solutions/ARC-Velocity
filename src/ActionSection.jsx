import React from 'react'
import { Link } from 'react-router-dom';

export const ActionSection = () => {
  return (
    <aside id="action-section">
            <div className="video">
                <img id="liveVideo" src="" alt=""/>
                <Link to="/landing-Page" className="home">HOME</Link>
                 {/* <a className="home" href="#landing-page">HOME</a> */}
            </div>
    </aside>
  )
};
