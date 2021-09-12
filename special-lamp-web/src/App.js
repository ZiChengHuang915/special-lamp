import './App.css';
import React, { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
	const [cards, setCard] = useState();
	const [gotCards, setGotCards] = useState(false);

	useEffect(() => {
		if (!gotCards) {
			getCards();
		}
	})

	const getCards = async () => {
		var url = "https://kijijifinder.herokuapp.com/getGPUs/";
		await axios.get(url)
			.then(res => {
				setCard(res.data.gpu_name)
				setGotCards(true);
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
