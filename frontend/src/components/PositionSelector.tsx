import React from 'react';

const POSITIONS = ['BTN', 'SB', 'BB', 'UTG', 'MP', 'CO'] as const;

interface PositionSelectorProps {
  position: string;
  stackSize: number;
  onPositionChange: (position: string) => void;
  onStackSizeChange: (stackSize: number) => void;
}

const PositionSelector: React.FC<PositionSelectorProps> = ({
  position,
  stackSize,
  onPositionChange,
  onStackSizeChange,
}) => {
  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Position & Stack Size</h3>
      
      {/* Position Selector */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Position
        </label>
        <select
          value={position}
          onChange={(e) => onPositionChange(e.target.value)}
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
        >
          <option value="">Select Position</option>
          {POSITIONS.map(pos => (
            <option key={pos} value={pos}>{pos}</option>
          ))}
        </select>
      </div>

      {/* Stack Size Slider */}
      <div className="space-y-3">
        <label className="block text-sm font-medium text-gray-700">
          Stack Size: {stackSize} BB
        </label>
        <div className="flex items-center space-x-4">
          <span className="text-sm font-medium text-gray-500">10</span>
          <div className="flex-1">
            <input
              type="range"
              min="10"
              max="200"
              value={stackSize}
              onChange={(e) => onStackSizeChange(Number(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
            />
          </div>
          <span className="text-sm font-medium text-gray-500">200</span>
        </div>
        <div className="flex items-center space-x-2">
          <input
            type="number"
            min="10"
            max="200"
            value={stackSize}
            onChange={(e) => onStackSizeChange(Number(e.target.value))}
            className="w-24 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
          <span className="text-sm text-gray-500">BB</span>
        </div>
      </div>
    </div>
  );
};

export default PositionSelector; 