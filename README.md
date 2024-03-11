# Prosperity2-2024

Welcome to `Prosperity2-2024`, an immersive algorithmic trading challenge hosted by IMC. In this competition, participants design and implement trading algorithms to compete on a simulated exchange, trading virtual products to earn as many SeaShells (the currency of the archipelago) as possible. With new products introduced in various rounds and dynamic market conditions, `Prosperity2-2024` offers a unique platform to test and refine your trading strategies.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Knowledge in algorithmic trading principles
- Familiarity with object-oriented programming in Python

### Installation

Clone the repository to get started:

```bash
git clone https://github.com/yourusername/prosperity2-2024.git
cd prosperity2-2024
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Quick Start

After installation, run the sample trader to see it in action:

```bash
python run_trader.py
```

## Usage

To participate in the `Prosperity2-2024` challenge, you need to implement your trading logic within the `Trader` class provided in the `trader.py` file. The key method to modify is `run`, which is invoked at each trading iteration with the current market state.

```python
class Trader:
    def run(self, state: TradingState):
        # Implement your trading logic here
        pass
```

### Testing Your Algorithm

To test your trading algorithm locally, you can use the provided simulation environment:

```bash
python simulate.py --trader trader.Trader
```

This will run your `Trader` class against historical market data, outputting the performance and transactions made by your algorithm.

## Features

- **Realistic Trading Environment:** Simulates an exchange where algorithms trade against bot traders, reflecting realistic market dynamics.
- **Dynamic Products:** New products are introduced at various stages, requiring participants to adapt their strategies.
- **State Persistence:** Utilize the `traderData` attribute to maintain state information between trading iterations.
- **Performance Feedback:** Receive detailed logs and performance metrics to refine your strategies.

## Contributing

Contributions to the `Prosperity2-2024` challenge are welcome! If you have suggestions to improve the competition or encounter any issues, please file an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to IMC for hosting the `Prosperity2-2024` trading challenge.
- Appreciation to all participants for their innovative contributions and spirited competition.
