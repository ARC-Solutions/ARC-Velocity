import {FaLongArrowAltDown, FaLongArrowAltLeft, FaLongArrowAltRight, FaLongArrowAltUp} from 'react-icons/fa';
import React, { useState, useEffect } from 'react'
export const ArrowKeys = React.memo(({value}) => {
    const keyDirections = {
    up: 'forward',
    down: 'backward',
    left: 'left',
    right: 'right'
}
    const wasdDirection = ['w','a','s','d'];
    const [keyDown, setKeyDown] = useState({
    up:false,
    down:false,
    left: false,
    right: false,
});
     const switchOn = (direction)=>{
    fetch(`http://localhost:5000/${direction}`)
    .then(res => res.text())
    .then(res => console.log(res))
    .catch(err => console.log(err));
    }
    const switchOff = (direction)=>{
    fetch(`http://localhost:5000/${direction}-off`)
        .then(res => res.text())
        .then(res => console.log(res))
        .catch(error => console.log(error));
    }

    const handleKeyDown = (e)=>{
        
        wasdDirection.map(key =>{
            let translateKey;
            if(e.key === key){
                translateKey = key === 'w'? 'up': key === 'a' ? 'left': key === 's' ? 'down': key === 'd' ? 'right':'';
                // switchOn(keyDirections[translateKey]);
                setKeyDown({...keyDown, [translateKey]: true}); 
            }
        });
    };

    const handleKeyUp =(e)=>{
         wasdDirection.map(key =>{
            let translateKey;
            if(e.key === key){
                translateKey = key === 'w'? 'up': key === 'a' ? 'left': key === 's' ? 'down': key === 'd' ? 'right':'';
                // switchOff(keyDirections[translateKey]);
                setKeyDown({...keyDown, [translateKey]: false});
            }
        });
    };

    useEffect(()=>{
        document.addEventListener('keydown', handleKeyDown);
        document.addEventListener('keyup', handleKeyUp);
        return ()=>{
           document.removeEventListener('keydown', handleKeyDown); 
           document.removeEventListener('keyup', handleKeyUp); 
        }
    },[handleKeyDown, handleKeyUp]);

  return (
        <div 
        className="bg"
        >
            {
                value === 'forward' ? 
        (
        <FaLongArrowAltUp 
        className={`controlls ${value} ${keyDown.up && "animate"}`}></FaLongArrowAltUp> 
        ):
        value === 'right' ? (
            <FaLongArrowAltRight 
            className={`controlls ${value} ${keyDown.right && "animateX"}`}></FaLongArrowAltRight> 
        ): 
        value === 'left' ? (
            <FaLongArrowAltLeft 
            className={`controlls ${value} ${keyDown.left && "animateX"}`}></FaLongArrowAltLeft> 
        ):
        <FaLongArrowAltDown 
        className={`controlls ${value} ${keyDown.down && "animate"}`}></FaLongArrowAltDown> 
            }
        </div>
        
  )
});
