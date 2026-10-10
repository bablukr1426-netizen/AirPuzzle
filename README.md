# 🎮 AirPuzzle – Hand Gesture Controlled Sliding Puzzle

**AirPuzzle** is an interactive sliding puzzle game that allows users to control game pieces using hand gestures instead of a mouse or keyboard. It uses Computer Vision to detect hand movements and recognize pinch gestures through a webcam.

## 🚀 Features

- ✋ **Hand Tracking:** Detects hand movements using MediaPipe.
- 👆 **Virtual Cursor:** Uses the index finger to control the cursor.
- 🤏 **Pinch Gesture:** Pinch your thumb and index finger to grab a block.
- 🧩 **Sliding Puzzle Gameplay:** Move the red block toward the exit.
- 🚧 **Collision Detection:** Prevents blocks from overlapping or moving through obstacles.
- 🎯 **Grid-Based Movement:** Keeps blocks aligned with the puzzle board.
- 🟢 **Exit Detection:** Detects when the player reaches the target.
- 🎮 **Multiple Levels:** Includes different puzzle layouts and increasing difficulty.
- 🔄 **Restart and Progression:** Restart the game or advance to the next level.
- 🖥️ **Interactive Interface:** Built with Pygame.

## 🛠️ Technologies Used

- Python 3.11
- OpenCV
- MediaPipe
- NumPy
- Pygame

## 📋 Requirements

- Python 3.11
- A working webcam
- A computer capable of running Python and OpenCV
- Required Python libraries

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AirPuzzle
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python3.11 -m venv venv
```

### 3. Activate the Virtual Environment

**macOS / Linux**

```bash
source venv/bin/activate
```

**Windows**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install numpy opencv-contrib-python==4.11.0.86 mediapipe==0.10.21 pygame
```

### 5. Run the Game

```bash
python main.py
```

Allow camera access if your operating system requests permission.

## 🎮 How to Play

1. Launch AirPuzzle using `main.py`.
2. Position your hand in front of the webcam.
3. Move your index finger to control the virtual cursor.
4. Bring your thumb and index finger together to grab the red block.
5. Move your hand to move the block.
6. Release the pinch gesture to drop the block.
7. Navigate around obstacles and move the red block to the green exit.
8. Complete the level and continue to the next one.

## ⌨️ Keyboard Controls

| Key     | Action                                          |
| ------- | ----------------------------------------------- |
| `R`     | Restart the current level                       |
| `Q`     | Quit the game                                   |
| `SPACE` | Move to the next level after completing a level |

## 🧠 How It Works

1. **Video Capture:** OpenCV captures frames from the webcam.
2. **Hand Detection:** MediaPipe detects hand landmarks.
3. **Gesture Recognition:** The distance between the thumb tip and index fingertip determines whether the user is pinching.
4. **Cursor Control:** The index finger position controls the virtual cursor.
5. **Block Movement:** Pygame handles puzzle interactions and movement.
6. **Collision Checking:** The game checks movement against obstacles and board boundaries.
7. **Win Detection:** The game checks whether the player reaches the exit.

## 📁 Project Structure

```text
AirPuzzle/
├── main.py
├── README.md
└── venv/
```

*Note: Add any other source files, assets, or configuration files that your project uses. Do not upload the `venv/` folder to GitHub.*

## 🔮 Future Enhancements

- More challenging puzzle levels
- Score tracking and a leaderboard
- Improved animations and visual effects
- AI-powered hints and puzzle solving
- Additional hand gestures and customization
- Performance improvements for hand tracking

## 🎯 Project Objective

The objective of AirPuzzle is to explore the practical application of Computer Vision and gesture recognition by creating a touch-free gaming experience.

## 👨‍💻 Author

**Bablu Kumar Singh**

GitHub: [Add your GitHub ](https://github.com/)[https://github.com/bablukr1426-netizen/AirPuzzle](https://github.com/bablukr1426-netizen/AirPuzzle)[profile URL](https://github.com/)

LinkedIn: [Add your LinkedIn profile URL](https://www.linkedin.com/)www\.linkedin.com/in/bablu-singh-6a9153334

---

⭐ If you find this project interesting, consider giving the repository a star!
