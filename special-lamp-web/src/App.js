import './App.css';
import React, { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
	const [cards, setCard] = useState([]);
	const [gotCards, setGotCards] = useState(false);
	const [desc, setDesc] = useState([]);
	const [price, setPrice] = useState([]);
	const [name, setName] = useState([]);
	const [selectedCard, setSelectedCard] = useState("???");
	const [kjijiListings, setKijijiListings] = useState([]);
	const [gettingListings, setGettingListings] = useState(true);

	useEffect(() => {
		if (!gotCards) {
			getCards();
		}
	})

	useEffect(() => {
		var kjijiListingsTemp = []
		console.log(desc.length);
		for (let i = 0; i < desc.length; i++) {
			kjijiListingsTemp.push({ "name": name[i], "price": price[i], "desc": desc[i] })
			console.log("hi")
		}

		setKijijiListings(kjijiListingsTemp);
		setGettingListings(false);
	}, [desc, price, name]);

	const getCards = async () => {
		var url = "https://kijijifinder.herokuapp.com/getGPUs/";
		await axios.get(url)
			.then(res => {
				setCard(res.data.gpu_name)
				setGotCards(true);
			})
	}

	const getKijijiDeals = async (card_name) => {
		setSelectedCard(card_name);
		setGettingListings(true);
		var url = "https://kijijifinder.herokuapp.com/getKijijiEntries/" + card_name;
		const resposne = await axios.get(url)

		console.log(resposne.data);

		await setDesc(resposne.data.desc);
		await setPrice(resposne.data.price);
		await setName(resposne.data.gpu_name);
	}

	return (
		<div className="App">
			<div className="PickCard">
				<h1>Pick a Card, Any Card</h1>
				<div className="CardButtons">
					{gotCards ? (
						<div className="FoundCards">
							{cards.map(card_name => (
								<button onClick={() => getKijijiDeals(card_name)}>{card_name}</button>
							))}
						</div>
					) : (
						<>
							<div className="LoadingCards">
								<p>hold up</p>
							</div>
						</>
					)}
				</div>
			</div>
			<div className="KjijiListings">
				{gettingListings ? (
					<div className="FindingListings">
						<p>Finding Listings for {selectedCard}</p>
					</div>
				) : (
					<>
						<div className="FoundListings">
							{kjijiListings.map(kijijiListing => (
								<div className="kijijiListing">
									<p>{kijijiListing.name}</p>
									<p>${kijijiListing.price}</p>
									<p>{kijijiListing.desc}</p>
								</div>
							))}
						</div>
					</>
				)}
			</div>
		</div>
	);
}

export default App;
