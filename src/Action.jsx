import React from 'react'
import { Link } from 'react-router-dom';

export const Action = () => {
  return (
    <aside id="action-section" className='action-autonomous'>
            <div className="video">
                <img id="liveVideo" src="http://192.168.43.112:8080/video" alt=""/>
            </div>
    </aside>
  ) 
};
