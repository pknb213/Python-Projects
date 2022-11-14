import React from 'react';
import ReactDOM from 'react-dom';
import App_bk from './App_bk';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<App_bk />, div);
  ReactDOM.unmountComponentAtNode(div);
});
