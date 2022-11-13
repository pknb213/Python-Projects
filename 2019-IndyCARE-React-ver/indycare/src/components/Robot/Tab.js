import React from 'react';
import './Tab.css';

export class Tab extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.handleTabClick = this.handleTabClick.bind(this);
    }

    handleTabClick(event) {
        event.preventDefault();
        this.props.onClick(this.props.tabIndex);
    }

    render() {
        return (
            <button className="tablinks" onClick={this.handleTabClick}
                    id="defaultOpen">
                {this.props.text}
            </button>
        )
    }
}



