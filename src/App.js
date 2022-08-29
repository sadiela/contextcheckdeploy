import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

// Solid test articles
/**
 * CNN: https://www.cnn.com/2021/02/05/media/lou-dobbs-fox-show-canceled/index.html
 * FOX: https://www.foxnews.com/politics/biden-terrorist-designation-yemens-houthi-militia
 * HUFFPOST: https://www.huffpost.com/entry/covid-19-eviction-crisis-women_n_5fca8af3c5b626e08a29de11
 */

//Components:
import Homepage from './Homepage/Homepage';
import Deets from './Deets/Deets';
import AboutUs from './AboutUs/AboutUs';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Homepage />}/>
        <Route path="/about-us" element={<AboutUs />}/>
        <Route path="/deets" element={<Deets />}/>
      </Routes>
    </Router>
  );
}

export default App;


/*

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/">
          <div className="App">
            <Homepage />
          </div>
        </Route>
        <Route exact path="/about-us">
          <div className="App">
            <AboutUs />
          </div>
        </Route>
        <Route exact path="/deets">
          <div className="App">
            <Deets />
          </div>
        </Route>
      </Routes>
    </Router>
  );
}

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
      </div>
    );
  }
}

export default App;*/
