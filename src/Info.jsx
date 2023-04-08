import React, { useState, useEffect, useRef  } from 'react'
import { Link } from 'react-router-dom';
export const Info = () => {  
    const [hotLap, setHotLap] = useState(false);
    const [lapTime, setLapTime] = useState({ms: 0, sec: 0, min: 0});
    const interval = useRef();
    const resetTimer = ()=>{
        setLapTime({ms: 0, sec: 0, min: 0});
    }
    const startTimer = ()=>{
        setLapTime((lapTime)=>{
            if(lapTime.ms > 99){
            return {...lapTime, sec: lapTime.sec +1, ms:0}
            }
            else if(lapTime.sec == 60){
                
            return {...lapTime, min: lapTime.min +1, sec: 0}
            }
            else {
                return {...lapTime, ms: lapTime.ms +1}
            }
        });
    }
    
    const startHotLap = ()=>{
            setHotLap(true);
        	resetTimer();
            interval.current = setInterval(startTimer, 10);

    }
    const stopHotLap = ()=>{
        setHotLap(false);
        clearInterval(interval.current);
    }
    const handlePressSpace = (e)=>{
        if(e.code === 'Space'){
            if(hotLap){
                stopHotLap();
            }
            else if(!hotLap){
                startHotLap();
            }
        }
    }
    useEffect(()=>{
        document.addEventListener('keydown', handlePressSpace);

        return ()=>{
            document.removeEventListener('keydown', handlePressSpace);
        }
    },[handlePressSpace]);
  return (
     <aside id="info-section">
        <div className="lap-time">
                <h1>ARC AI</h1>
                <h2>
                    <span className="minutes">{`${lapTime.min.toString().length > 1 ?lapTime.min : `0${lapTime.min}`}`}
                    </span>:<span className="seconds">{`${lapTime.sec.toString().length > 1 ? lapTime.sec : `0${lapTime.sec}`}`}
                    </span>:<span className="milliseconds">{`${lapTime.ms.toString().length > 1 ?lapTime.ms : `0${lapTime.ms}`}`}
                    </span>
                </h2>
            </div>
            <Link to="/landing-Page" className='home'>HOME</Link>
     </aside>
  )
}
