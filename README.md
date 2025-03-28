# Online Auction Solution

## Overview
This Python application is designed to manage a unique bid blind online auction. The system allows bidders to place bids, processes these bids, and determines the winner based on specific rules. The auction can handle thousands of bids efficiently and includes mechanisms for handling ties.

## Features
- **Bid Placement**: Bidders can place bids, which are validated and recorded.
- **Auction Closing**: The auction can be closed, determining the winner based on the highest unique bid.
- **Tie Handling**: The system can either restart the auction or determine the winner based on the first bid in case of a tie.
- **Auction Restart**: The auction can be restarted with a new minimum bid if necessary.

## Requirements
- Python 3.13
- Logging: For debugging and information purposes.
- Threading: Optional, for handling concurrent bid processing.

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/itscullenbrady/PROG2400_FinalProject.git
   ```
2. Navigate to the project directory:
   ```sh
   cd PROG2400_FinalProject
   ```
3. Ensure you have Python 3.13 installed and set up a virtual environment:
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```
4. Install required packages (if any):
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### Example Usage
```python
from Auction import Auction

if __name__ == "__main__":
    auction = Auction(min_bid=10)
    auction.place_bid("Bidder1", 15)
    auction.place_bid("Bidder2", 20)
    auction.place_bid("Bidder3", 20)

    # Standard closing: restart if there's a tie.
    winner = auction.close_auction(tie_breaker_first_bid=False)
    if winner:
        print(f"Winner: {winner}")
    else:
        print("Restart auction with min bid:", auction.current_max + 1)
        auction.restart_auction()

    # Example for tie-breaker scenario where first bid wins:
    auction.place_bid("Bidder4", 25)
    auction.place_bid("Bidder5", 25)
    winner = auction.close_auction(tie_breaker_first_bid=True)
    if winner:
        print(f"Tie-breaker Winner: {winner}")
```

## Class and Methods
### Auction
#### Attributes:
- **min_bid**: The minimum bid allowed.
- **frequency**: A dictionary mapping bid amounts to a list of bidder IDs.
- **current_max**: The highest bid amount recorded.
- **current_max_count**: The number of times the highest bid has been placed.

#### Methods:
- `__init__(self, min_bid: int)`: Initializes the auction with a minimum bid.
- `place_bid(self, bidder_id: str, bid_amount: int)`: Places a bid for a bidder if the bid amount is valid.
- `close_auction(self, tie_breaker_first_bid: bool = False) -> Optional[Any]`: Closes the auction and determines the winner.
- `restart_auction(self)`: Resets the auction state for a new round, setting the new minimum bid as `current_max + 1`.

## Technical Solution/Design Document
### Part A. Complexity Analysis
- **O(n³)**: Cubic time complexity, impractical for large inputs.
- **Ω(n³)**: Lower bound, not useful without an upper bound.
- **O(n²lg n)**: Upper bound with logarithmic factor, lacks a lower bound.
- **Θ(n²lg n)**: Tight bound, ideal for large inputs.
- **O(2ⁿ)**: Exponential complexity, highly inefficient.

### Part B. Data Structures & Auction System Design
- **Frequency Map**: Dictionary mapping bid values to lists of bidder IDs.
- **Current Max Tracker**: Variables to track the highest bid and its count.

### Detailed Algorithm
#### Bid Placement
1. Validate the bid.
2. Update the frequency map.
3. Update the current maximum bid.
4. Ensure thread safety if necessary.

#### Auction Close Process
1. Check if the highest bid is unique.
2. Handle ties by either restarting the auction or selecting the first bidder.

### Scalability and Performance
- **Hash Map Efficiency**: O(1) average-case time complexity for insertions and look-ups.
- **Memory Usage**: Efficient storage of bid information.
- **Concurrency**: Use thread-safe collections if necessary.

### Additional Considerations
- **Error Handling**: Validate inputs and log errors.
- **Future Enhancements**: Add features like bid retraction or dynamic minimum bid adjustments.
- **Testing and Validation**: Unit tests for edge cases and large-scale simulations.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

