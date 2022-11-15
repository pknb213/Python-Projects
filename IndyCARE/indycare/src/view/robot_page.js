import React from 'react';
import TopMenu from "../components/Public/TopMenu";
import HeaderTitle from "../components/Public/HeaderTitle";
import SideNavigator from "../components/Public/SideNavigator";
import FirstTab from "../components/Robot/FirstTab";
import SecondTab from "../components/Robot/SecondTab";
import {Tabs} from "../components/Robot/Tabs";
import {Tab} from "../components/Robot/Tab";
// import {Tab,Tabs,TabList,TabPanel } from 'react-tabs'

const DetailView = ({match}) => {
    return (
        <div id="wrapper">
            {/*<h2>{match.params.sn}</h2>*/}
            <SideNavigator/>
            <div className="contents_wrap clear">
                <div className="header_wrap">
                    <div className="header_top">
                        <TopMenu/>
                        <HeaderTitle title="Robot Detail" breadcrumb="Robot Detail"/>
                    </div>

                    {/*<Tab/>*/}
                        {/*<FirstTab/>*/}
                        {/*<SecondTab/>*/}

                        <Tabs>
                            <Tab iconClassName={'icon-class-0'} linkClassName={'link-class-0'} text={'Robot Information'}>
                                <FirstTab sn={match.params.sn}/>
                            </Tab>
                            <Tab iconClassName={'icon-class-1'} linkClassName={'link-class-1'} text={'Chart Information'}>
                                <SecondTab/>
                            </Tab>
                        </Tabs>
                </div>
            </div>
        </div>
    );
};

export default DetailView;