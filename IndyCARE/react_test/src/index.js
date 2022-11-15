import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Video from './video';
import Timer from "./tick";
import ToggleBtn from './toggle';
import {Form, TextAreaForm, SelectForm, ReservationForm} from './form';
import BoilingForm from './parent_state';
import {WelcomeDialog, WelcomeSplit} from "./composition";
import * as serviceWorker from './serviceWorker';


ReactDOM.render(
    <div>
        <ToggleBtn/>
        <Timer/>
        <Form/>
        <TextAreaForm/>
        <SelectForm/>
        <ReservationForm/>
        <BoilingForm/>
        <WelcomeDialog/>
        <WelcomeSplit/>
        <Video/>
    </div>
    , document.getElementById('root')
);


// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
