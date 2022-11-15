import React from 'react';
import {Route, Switch} from 'react-router-dom';
import {LoginView, Home, test, RobotListForUser, DetailView} from '../view';

const App = () => {
      return (
          <div>
              <Route exact path="/" component={LoginView}/>
              <Switch>
              <Route path="/test/:name" component={Home}/>
              <Route path="/test" component={test}/>
              </Switch>
              <Route path="/list/robots/user" component={RobotListForUser}/>
              <Route path="/display/:sn" component={DetailView}/>
          </div>
      );
};

export default App;
