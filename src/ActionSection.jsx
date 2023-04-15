import React from 'react'
import { Link } from 'react-router-dom';

export const ActionSection = () => {
  return (
    <aside id="action-section">
            <div className="video">
                <img id="liveVideo" src="" alt=""/>
                <Link to="/landing-Page" className="home" onClick={()=>{
                                fetch(`http://localhost:5000/home`, { method: "POST" })
                                .then((res) => res.text())
                                .then((res) => console.log(res))
                                .catch((err) => console.log(err));
                            }}>HOME</Link>
                 {/* <a className="home" href="#landing-page">HOME</a> */}
            </div>
    </aside>
  )
};
