import React from 'react';

const Input = (props) => {
    return (
        <input type={props.type}
               className={props.name}
               placeholder={props.text}
               value={props.value} onChange={props.onChange}
        />
    );
};

export default Input;