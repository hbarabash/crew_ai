// 'use client'; // Make sure it's a client-side component

// import React, { useState, useEffect } from 'react';

// import AICrewGame from '../../pycrew_game_train';
// import 

// interface Card {
//     color: string;
//     number: number;
// }

// const CrewGamePage: React.FC = () => {
//     const [deck, setDeck] = useState<Card[]>([]); // Current player's deck
//     const [currentPlayer, setCurrentPlayer] = useState<number>(0); // State to track whose turn it is
//     const [gameState, setGameState] = useState<any>(null); // The full game state
//     const [currentTable, setCurrentTable] = useState<any[]>([]); // Cards on the table (current play)

//     // Initialize the CrewGame object
//     const game = new AICrewGame(); // This creates a new instance of the CrewGame

//     // Function to update game state from CrewGame
//     const updateGameState = () => {
//         const state = game.get_game_state(); // Assuming you have a method to get the current game state
//         setDeck(game.get_current_player_deck()); // Update the deck of the current player
//         setCurrentPlayer(game.get_current_player_index()); // Update the current player
//         setCurrentTable(game.get_current_table()); // Update the table with played cards
//     };

//     // Handle card selection for the player
//     const handleCardSelect = (cardIndex: number) => {
//         // Play the selected card, pass action to game logic
//         const card = deck[cardIndex];
//         const action = game.get_current_player().deck.indexOf(card);
//         const [reward, done] = game.step(action); // Assuming `step` returns reward and done status
        
//         // Update the game state after making a move
//         updateGameState();
        
//         if (done) {
//             console.log("Game over, reward:", reward);
//         }
//     };

//     // Effect to initialize the game state
//     useEffect(() => {
//         updateGameState(); // Set initial game state
//     }, []);

//     return (
//         <div style={{ padding: '20px' }}>
//             <h1>Crew Game</h1>
//             <p>Player {currentPlayer + 1}'s turn</p>

//             <div>
//                 <h2>Current Table</h2>
//                 <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
//                     {currentTable.map((card, index) => (
//                         <button
//                             key={index}
//                             style={{
//                                 padding: '10px 20px',
//                                 borderRadius: '8px',
//                                 background: '#f1f1f1',
//                                 border: '1px solid #ddd',
//                             }}
//                         >
//                             {card.color} {card.number}
//                         </button>
//                     ))}
//                 </div>
//             </div>

//             <div>
//                 <h2>Your Deck</h2>
//                 <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
//                     {deck.map((card, index) => (
//                         <button
//                             key={index}
//                             onClick={() => handleCardSelect(index)}
//                             style={{
//                                 padding: '10px 20px',
//                                 borderRadius: '8px',
//                                 background: '#f1f1f1',
//                                 border: '1px solid #ddd',
//                             }}
//                         >
//                             {card.color} {card.number}
//                         </button>
//                     ))}
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default CrewGamePage;