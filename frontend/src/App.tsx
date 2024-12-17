import { useState } from 'react'
import ImageUpload from './components/ImageUpload'
import CardSelector from './components/CardSelector'
import PlayerCardSelector from './components/PlayerCardSelector'
import PositionSelector from './components/PositionSelector'
import ChatInterface from './components/ChatInterface'

interface Card {
  rank: string
  suit: string
}

const GAME_STAGES = ['Preflop', 'Flop', 'Turn', 'River']

// 添加卡牌格式转换函数
const convertCard = (card: { rank: string, suit: string }): Card => {
  // 转换花色
  const suitMap: { [key: string]: string } = {
    'spades': '♠',
    'hearts': '♥',
    'diamonds': '♦',
    'clubs': '♣',
    '♠': '♠',
    '♥': '♥',
    '♦': '♦',
    '♣': '♣'
  };

  // 转换点数
  const rankMap: { [key: string]: string } = {
    '10': 'T',
    'ten': 'T'
  };

  const suit = suitMap[card.suit.toLowerCase()] || card.suit;
  const rank = rankMap[card.rank.toLowerCase()] || card.rank.toUpperCase();

  return { rank, suit };
};

function App() {
  const [playerCards, setPlayerCards] = useState<Card[]>([])
  const [boardCards, setBoardCards] = useState<Card[]>([])
  const [gameStage, setGameStage] = useState(GAME_STAGES[0])
  const [position, setPosition] = useState('')
  const [stackSize, setStackSize] = useState(100)

  const handleAnalysisComplete = (data: any) => {
    if (data.success && data.data) {
      // Update player cards with converted format
      if (data.data.player_hand) {
        setPlayerCards(data.data.player_hand.map(convertCard))
      }
      // Update board cards with converted format
      if (data.data.board_cards) {
        setBoardCards(data.data.board_cards.map(convertCard))
      }
      // Update position if available
      if (data.data.current_user_position) {
        setPosition(data.data.current_user_position.toUpperCase())
      }
    }
  }

  const handlePlayerCardSelect = (card: Card) => {
    setPlayerCards(prev => {
      const newCards = [...prev];
      const existingIndex = newCards.findIndex(
        c => c.rank === card.rank && c.suit === card.suit
      );
      
      if (existingIndex !== -1) {
        newCards.splice(existingIndex, 1);
      } else {
        if (newCards.length < 2) {
          newCards.push(card);
        } else {
          newCards[1] = card;
        }
      }
      return newCards;
    });
  }

  const handleBoardCardSelect = (card: Card) => {
    setBoardCards(prev => {
      const exists = prev.some(c => c.rank === card.rank && c.suit === card.suit)
      if (exists) {
        return prev.filter(c => !(c.rank === card.rank && c.suit === card.suit))
      }
      return prev.length < 5 ? [...prev, card] : prev
    })
  }

  const gameState = {
    position,
    stage: gameStage,
    stack_size: stackSize,
    board_cards: boardCards,
    player_cards: playerCards
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center">
      <div className="container mx-auto px-4">
        <div className="bg-white shadow-lg rounded-3xl overflow-hidden">
          <div className="max-w-[1400px] mx-auto p-6 lg:p-10">
            <h1 className="text-3xl font-bold text-center mb-8">Poker Hand Analyzer</h1>
            
            {/* Game Stage and Position Selectors */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Game Stage
                  </label>
                  <select
                    value={gameStage}
                    onChange={(e) => setGameStage(e.target.value)}
                    className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                  >
                    {GAME_STAGES.map(stage => (
                      <option key={stage} value={stage}>{stage}</option>
                    ))}
                  </select>
                </div>
              </div>
              <PositionSelector
                position={position}
                stackSize={stackSize}
                onPositionChange={setPosition}
                onStackSizeChange={setStackSize}
              />
            </div>

            {/* Card Selectors */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <PlayerCardSelector
                selectedCards={playerCards}
                onCardSelect={handlePlayerCardSelect}
              />
              <CardSelector
                selectedCards={boardCards}
                maxCards={5}
                onCardSelect={handleBoardCardSelect}
                title="Board Cards"
              />
            </div>

            {/* Image Upload */}
            <div className="mb-8">
              <ImageUpload onAnalysisComplete={handleAnalysisComplete} />
            </div>

            {/* Chat Interface */}
            <div>
              <ChatInterface gameState={gameState} />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
