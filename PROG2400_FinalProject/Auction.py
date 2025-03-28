from collections import defaultdict
from typing import Optional, List, Dict, Any
import logging
import threading

# Configure logging for debugging purposes
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Auction:
    """
    A class to manage a unique bid blind online auction.

    Attributes:
        min_bid (int): The minimum bid allowed.
        frequency (Dict[int, List[str]]): A mapping from bid amounts to a list of bidder IDs.
        current_max (int): The highest bid amount recorded.
        current_max_count (int): The number of times the highest bid has been placed.
    """

    def __init__(self, min_bid: int) -> None:
        self.min_bid: int = min_bid
        self.frequency: Dict[int, List[str]] = defaultdict(list)
        self.current_max: int = -float('inf')
        self.current_max_count: int = 0
        # For concurrent bid processing, uncomment the next line:
        # self.lock = threading.Lock()

    def place_bid(self, bidder_id: str, bid_amount: int) -> None:
        """
        Places a bid for a bidder if the bid amount is valid.

        Args:
            bidder_id (str): The unique identifier for the bidder.
            bid_amount (int): The bid amount in Canadian dollars.
        """
        # Uncomment if thread safety is required:
        # with self.lock:
        if bid_amount < self.min_bid:
            logging.info(f"Bid of ${bid_amount} from {bidder_id} is below the minimum bid of ${self.min_bid}. Discarded.")
            return

        self.frequency[bid_amount].append(bidder_id)
        logging.info(f"Bid of ${bid_amount} placed by {bidder_id}.")

        if bid_amount > self.current_max:
            self.current_max = bid_amount
            self.current_max_count = 1
            logging.info(f"New current max bid is ${self.current_max}.")
        elif bid_amount == self.current_max:
            self.current_max_count += 1
            logging.info(f"Current max bid ${self.current_max} now has {self.current_max_count} bids.")

    def close_auction(self, tie_breaker_first_bid: bool = False) -> Optional[Any]:
        """
        Closes the auction and determines the winner.

        Args:
            tie_breaker_first_bid (bool): If True, the first bidder wins in the event of a tie.
                                          Otherwise, the auction is restarted.

        Returns:
            The winner's bidder ID if a unique highest bid is found or if tie_breaker_first_bid is True.
            Returns None if a tie is detected and the auction needs to be restarted.
        """
        # Uncomment if thread safety is required:
        # with self.lock:
        if self.current_max_count == 1 or tie_breaker_first_bid:
            winner = self.frequency[self.current_max][0]
            logging.info(f"The winner is {winner} with a bid of ${self.current_max}.")
            return winner
        else:
            logging.info(f"Tie detected for bid ${self.current_max}. Auction will be restarted with new minimum bid ${self.current_max + 1}.")
            return None

    def restart_auction(self) -> None:
        """
        Resets the auction state for a new round, setting the new minimum bid as current_max + 1.
        """
        # Uncomment if thread safety is required:
        # with self.lock:
        self.min_bid = self.current_max + 1
        self.frequency.clear()
        self.current_max = -float('inf')
        self.current_max_count = 0
        logging.info(f"Auction restarted. New minimum bid is ${self.min_bid}.")

# Example Usage:
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
