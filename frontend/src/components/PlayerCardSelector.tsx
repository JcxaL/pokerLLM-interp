import React, { useState } from 'react';

const RANKS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'];
const SUITS = ['♠', '♥', '♦', '♣'];
const SUIT_COLORS = {
  '♠': 'text-black',
  '♥': 'text-red-500',
  '♦': 'text-red-500',
  '♣': 'text-black'
} as const;

interface Card {
  rank: string;
  suit: string;
}

interface PlayerCardSelectorProps {
  selectedCards: Card[];
  onCardSelect: (card: Card) => void;
}

const PlayerCardSelector: React.FC<PlayerCardSelectorProps> = ({
  selectedCards,
  onCardSelect,
}) => {
  const [selectedRank, setSelectedRank] = useState<string | null>(null);
  const [activeCardIndex, setActiveCardIndex] = useState<number | null>(null);

  const handleRankClick = (rank: string) => {
    setSelectedRank(rank);
  };

  const handleSuitClick = (suit: string) => {
    if (selectedRank && activeCardIndex !== null) {
      const newCard = { rank: selectedRank, suit };
      const updatedCards = [...selectedCards];
      updatedCards[activeCardIndex] = newCard;
      onCardSelect(newCard);
      setSelectedRank(null);
      setActiveCardIndex(null);
    }
  };

  const handleCardSlotClick = (index: number) => {
    setActiveCardIndex(index);
    setSelectedRank(null);
  };

  return (
    <div className="mb-6">
      <h3 className="text-lg font-semibold mb-2">Player Cards</h3>
      
      {/* Card Selection Slots */}
      <div className="flex space-x-4 mb-4">
        {[0, 1].map((index) => (
          <button
            key={index}
            onClick={() => handleCardSlotClick(index)}
            className={`w-16 h-24 rounded border-2 ${
              activeCardIndex === index
                ? 'border-blue-500'
                : 'border-gray-300'
            } flex items-center justify-center text-lg`}
          >
            {selectedCards[index] ? (
              <span className={SUIT_COLORS[selectedCards[index].suit as keyof typeof SUIT_COLORS]}>
                {selectedCards[index].rank}
                {selectedCards[index].suit}
              </span>
            ) : (
              `Card ${index + 1}`
            )}
          </button>
        ))}
      </div>

      {/* Ranks */}
      <div className="grid grid-cols-13 gap-1 mb-4">
        {RANKS.map(rank => (
          <button
            key={rank}
            onClick={() => handleRankClick(rank)}
            className={`w-8 h-8 rounded ${
              selectedRank === rank
                ? 'bg-blue-500 text-white'
                : 'bg-white border border-gray-300 hover:bg-gray-100'
            }`}
          >
            {rank}
          </button>
        ))}
      </div>

      {/* Suits */}
      <div className="flex space-x-4 justify-center">
        {SUITS.map(suit => (
          <button
            key={suit}
            onClick={() => handleSuitClick(suit)}
            className={`w-12 h-12 rounded ${
              selectedRank && activeCardIndex !== null
                ? 'hover:bg-gray-100 cursor-pointer'
                : 'opacity-50 cursor-not-allowed'
            } border border-gray-300 flex items-center justify-center text-2xl ${SUIT_COLORS[suit as keyof typeof SUIT_COLORS]}`}
          >
            {suit}
          </button>
        ))}
      </div>
    </div>
  );
};

export default PlayerCardSelector; 