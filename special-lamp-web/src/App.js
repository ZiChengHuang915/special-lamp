import './App.css';
import React, {useState, useEffect} from 'react'
import axios from 'axios'

const App = () => {
  const [cards, setCard] = useState();

  useEffect (() => {
    getCards()
  })

  const getCards = () => {
    var url = "https://kijijifinder.herokuapp.com/getGPUs/";
    console.log("hello")
    axios.get(url)
      .then(res => {
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