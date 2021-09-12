import './App.css';
import React, {useState, useEffect} from 'react'
import axios from 'axios'

function App() {
  const [cards, setCard] = useState();

  useEffect (() => {
    getCards()
  })

  const getCards = () => {
    var url = "https://kijijifinder.herokuapp.com/getGPUs/";
    axios.get(url)
      .then(res => {
        console.log("hello")
        console.log(res.data.data)
      })
  }

  return (
    <div className="App">
      <div className="PickCard">
        <h1>Pick a Card, Any Card</h1>
      </div>
      <div className="KjijiListings">
      </div>
    </div>
  );
}

export default App;
