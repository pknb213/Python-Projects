import React from 'react';
import './index.css';

// class Video extends React.Component{
//     render() {
//         return (
//             <h1>Hello Fucking World</h1>
//         );
//     }
// }

// Function형은 State를 갖지 않고 Render 함수만을 가짐.
function Video() {
    return (
        <div className={"event_view"}>
            <div className={'section_title'}>
                <h1>Hello Fucking World</h1>
            </div>
            <video id={"clip"} controls loop muted autoPlay/>
        </div>
    );
}
export default Video;