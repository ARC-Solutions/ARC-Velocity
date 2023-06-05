import React from 'react'
import { Link } from 'react-router-dom';

export const Action = () => {
  return (
    <aside id="action-section" className='action-autonomous'>
      <div className="dot-container">
      <span class="dot"></span>
<span class="dot"></span>
      </div>
            <div className="video">
                <img id="liveVideo" src="http://192.168.0.164:8080/video" alt=""/>
            </div>
            <div className="dot-container">
            <span class="dot"></span>
        <span class="dot"></span>
            </div>
            
    </aside>
  ) 
};
