import React, { useState, useEffect } from 'react';
import { ColorfulMessage } from './components/ColorfulMessage';

export const App = () => {
  const [num, setNum] = useState(0);
  const [isShowFace, setIsShowFace] = useState(true);
  const onClickCountUp = () => {
    setNum(num + 1);
  };
  const onClickSwitchShowFace = () => {
    setIsShowFace(!isShowFace);
  };

  useEffect(() => {
    if (num > 0) {
      if (num % 3 === 0) {
        isShowFace || setIsShowFace(true);
      } else {
        isShowFace && setIsShowFace(false);
      }
    }
  }, [num]);

  return (
    <>
      <h1>こんにちは</h1>
      <ColorfulMessage color='blue'>お元気ですか？</ColorfulMessage>
      <ColorfulMessage color='green'>元気です！</ColorfulMessage>
      <button onClick={onClickCountUp}>カウントアップ</button>
      <p>{num}</p>
      <button onClick={onClickSwitchShowFace}>on/off</button>
      {isShowFace && <p>(T_T)</p>}
    </>
  );
};
