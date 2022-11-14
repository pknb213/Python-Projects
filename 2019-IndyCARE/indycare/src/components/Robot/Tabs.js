import React from 'react';
import PropTypes from 'prop-types';
import './Tabs.css'

export class Tabs extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeTabIndex: 0
        };
        this.handleTabClick = this.handleTabClick.bind(this);
    }

    // Toggle currently active tab
    handleTabClick(tabIndex) {
        this.setState({
            activeTabIndex: tabIndex === this.state.activeTabIndex ? this.props.defaultActiveTabIndex : tabIndex
        });
    }

    // Encapsulate <Tabs/> component API as props for <Tab/> children
    renderChildrenWithTabsApiAsProps() {
        return React.Children.map(this.props.children, (child, index) => {
            return React.cloneElement(child, {
                onClick: this.handleTabClick,
                tabIndex: index,
                isActive: index === this.state.activeTabIndex
            });
        });
    }

    // Render current active tab content
    renderActiveTabContent() {
        const {children} = this.props;
        const {activeTabIndex} = this.state;
        if (children[activeTabIndex]) {
            return children[activeTabIndex].props.children;
        }
    }

    render() {
        return (
            <div>
                <div className="tab_menu">
                    {this.renderChildrenWithTabsApiAsProps()}
                </div>
                <div className="tab_contents_wrap">
                    {this.renderActiveTabContent()}
                </div>
            </div>
        );
    }
}

Tabs.propTypes = {
    defaultActiveTabIndex: PropTypes.number
};

Tabs.defaultProps = {
    defaultActiveTabIndex: null
};

