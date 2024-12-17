import React from 'react';

const RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];
const SUITS = ['♠', '♥', '♦', '♣'];
const SUIT_COLORS = {
  '♠': 'text-black',
  '♥': 'text-red-500',
  '♦': 'text-red-500',
  '♣': 'text-black'
};

interface Card {
  rank: string;
  suit: string;
}

interface CardSelectorProps {
  selectedCards: Card[];
  maxCards: number;
  onCardSelect: (card: Card) => void;
  title: string;
}

const CardSelector: React.FC<CardSelectorProps> = ({
  selectedCards,
  maxCards,
  onCardSelect,
  title
}) => {
  const isCardSelected = (rank: string, suit: string) => {
    return selectedCards.some(card => card.rank === rank && card.suit === suit);
  };

  const handleCardClick = (rank: string, suit: string) => {
    if (isCardSelected(rank, suit)) {
      // Remove card if already selected
      onCardSelect({ rank, suit });
    } else if (selectedCards.length < maxCards) {
      // Add card if under max limit
      onCardSelect({ rank, suit });
    }
  };

  const getSuitSymbol = (suit: string) => {
    switch (suit) {
      case 'spades': return '♠';
      case 'hearts': return '♥';
      case 'diamonds': return '♦';
      case 'clubs': return '♣';
      default: return suit;
    }
  };

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <div className="grid grid-cols-13 gap-1">
        {RANKS.map(rank => (
          <div key={rank} className="flex flex-col items-center">
            {SUITS.map(suit => (
              <button
                key={`${rank}${suit}`}
                onClick={() => handleCardClick(rank, suit)}
                className={`w-8 h-8 m-1 rounded ${
                  isCardSelected(rank, suit)
                    ? 'bg-blue-500 text-white'
                    : 'bg-white border border-gray-300 hover:bg-gray-100'
                } ${SUIT_COLORS[suit]} transition-colors`}
              >
                {rank}
                <span className="text-xs">{suit}</span>
              </button>
            ))}
          </div>
        ))}
      </div>
      <div className="mt-2">
        Selected: {selectedCards.map(card => 
          <span key={`${card.rank}${card.suit}`} className={`mx-1 ${SUIT_COLORS[getSuitSymbol(card.suit)]}`}>
            {card.rank}{getSuitSymbol(card.suit)}
          </span>
        )}
      </div>
    </div>
  );
};

export default CardSelector; 