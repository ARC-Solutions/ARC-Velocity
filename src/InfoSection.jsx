import React, { useState, useEffect, useRef  } from 'react'
import { ArrowKeys } from './ArrowKeys';
export const InfoSection = () => {

    const arrows = ['forward', 'right', 'backward', 'left'];
    const [hotLap, setHotLap] = useState(false);
    const [btnStyle, setBtnStyle] = useState({bgColour: 'var(--primary-color)', color: '#fff', value: 'Press Space To Start'});
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
            setBtnStyle({bgColour: '#fff', color: '#333', value: 'Press Space To Stop'});
    }
    const stopHotLap = ()=>{
        setHotLap(false);
        clearInterval(interval.current);
        setBtnStyle({bgColour: 'var(--primary-color)', color: '#fff', value: 'Press Space To Start'});
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
                <h1>Lap Time</h1>
                <h2>
                    <span className="minutes">{`${lapTime.min.toString().length > 1 ?lapTime.min : `0${lapTime.min}`}`}
                    </span>:<span className="seconds">{`${lapTime.sec.toString().length > 1 ? lapTime.sec : `0${lapTime.sec}`}`}
                    </span>:<span className="milliseconds">{`${lapTime.ms.toString().length > 1 ?lapTime.ms : `0${lapTime.ms}`}`}
                    </span>
                </h2>
            </div>
            <div className="challangeTime">
                <h4>Time To Beat</h4>
                <h4 id="time">00:00:00</h4>
            </div>
            <div 
            className="controller"
            >
                {
                    arrows.map((arrowVal, index) =>{
                        return (
                            <ArrowKeys key={index} value={arrowVal}/>
                        )
                    })
                }
            </div>
            <button 

            className="racing space" 
            style={{backgroundColor: `${btnStyle.bgColour}`, color: `${btnStyle.color}`}}
            >{btnStyle.value}</button>
     </aside>
  )
}
