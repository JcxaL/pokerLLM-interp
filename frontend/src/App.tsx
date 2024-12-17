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

const MODEL_OPTIONS = {
  "ft:gpt-4o-mini-2024-07-18:personal::Af1GA1or": "Fine-tuned Poker Model",
  "gpt-4o-mini": "Standard GPT-4o Mini"
} as const;

function App() {
  const [playerCards, setPlayerCards] = useState<Card[]>([])
  const [boardCards, setBoardCards] = useState<Card[]>([])
  const [gameStage, setGameStage] = useState(GAME_STAGES[0])
  const [position, setPosition] = useState('')
  const [stackSize, setStackSize] = useState(100)
  const [modelParams, setModelParams] = useState({
    model_id: "ft:gpt-4o-mini-2024-07-18:personal::Af1GA1or" as keyof typeof MODEL_OPTIONS,
    temperature: 0.7,
    max_tokens: 512,
    top_p: 1.0,
    frequency_penalty: 0,
    presence_penalty: 0
  });

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
            
            {/* Model Parameters Sidebar */}
            <div className="fixed right-0 top-0 h-full w-64 bg-white shadow-lg p-4 overflow-y-auto">
              <h3 className="text-lg font-semibold mb-4">Model Parameters</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Model
                  </label>
                  <select
                    value={modelParams.model_id}
                    onChange={(e) => setModelParams(prev => ({
                      ...prev,
                      model_id: e.target.value as keyof typeof MODEL_OPTIONS
                    }))}
                    className="w-full px-3 py-2 border rounded-md bg-white"
                  >
                    {Object.entries(MODEL_OPTIONS).map(([id, name]) => (
                      <option key={id} value={id}>{name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Temperature
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={modelParams.temperature}
                    onChange={(e) => setModelParams(prev => ({...prev, temperature: parseFloat(e.target.value)}))}
                    className="w-full"
                  />
                  <span className="text-sm text-gray-500">{modelParams.temperature}</span>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Max Tokens
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="2048"
                    value={modelParams.max_tokens}
                    onChange={(e) => setModelParams(prev => ({...prev, max_tokens: parseInt(e.target.value)}))}
                    className="w-full px-3 py-2 border rounded-md"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Top P
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={modelParams.top_p}
                    onChange={(e) => setModelParams(prev => ({...prev, top_p: parseFloat(e.target.value)}))}
                    className="w-full"
                  />
                  <span className="text-sm text-gray-500">{modelParams.top_p}</span>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Frequency Penalty
                  </label>
                  <input
                    type="range"
                    min="-2"
                    max="2"
                    step="0.1"
                    value={modelParams.frequency_penalty}
                    onChange={(e) => setModelParams(prev => ({...prev, frequency_penalty: parseFloat(e.target.value)}))}
                    className="w-full"
                  />
                  <span className="text-sm text-gray-500">{modelParams.frequency_penalty}</span>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Presence Penalty
                  </label>
                  <input
                    type="range"
                    min="-2"
                    max="2"
                    step="0.1"
                    value={modelParams.presence_penalty}
                    onChange={(e) => setModelParams(prev => ({...prev, presence_penalty: parseFloat(e.target.value)}))}
                    className="w-full"
                  />
                  <span className="text-sm text-gray-500">{modelParams.presence_penalty}</span>
                </div>
              </div>
            </div>

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

            {/* Chat Interface with model params */}
            <div>
              <ChatInterface 
                gameState={gameState}
                modelParams={modelParams}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
