import React from 'react';

const Home = ({match}) => {
    return (
        <div>
            <h2>{match.params.name}홈</h2>
        </div>
    );
};

export default Home;