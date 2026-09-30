import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌깨기 게임")
st.write("키보드의 ← → 방향키로 패들을 움직이세요!")

game = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
    body {
        margin: 0;
        background: #111827;
        color: white;
        font-family: Arial, sans-serif;
        text-align: center;
    }

    canvas {
        background: #0f172a;
        border: 3px solid #38bdf8;
        border-radius: 10px;
        display: block;
        margin: 10px auto;
        max-width: 100%;
    }

    #info {
        font-size: 18px;
        margin: 10px;
    }

    button {
        background: #38bdf8;
        border: none;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
    }

    button:hover {
        background: #0ea5e9;
    }
</style>
</head>

<body>

<div id="info">
    점수: <span id="score">0</span>
    &nbsp;&nbsp;
    목숨: <span id="lives">3</span>
</div>

<canvas id="gameCanvas" width="700" height="500"></canvas>

<button onclick="restartGame()">🔄 다시 시작</button>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let score = 0;
let lives = 3;

let ball = {
    x: canvas.width / 2,
    y: canvas.height - 50,
    dx: 4,
    dy: -4,
    radius: 9
};

let paddle = {
    width: 110,
    height: 14,
    x: (canvas.width - 110) / 2,
    speed: 8
};

let rightPressed = false;
let leftPressed = false;

const brickRows = 5;
const brickColumns = 8;

const brickWidth = 72;
const brickHeight = 22;
const brickPadding = 10;

const brickOffsetTop = 45;
const brickOffsetLeft = 30;

let bricks = [];

function createBricks() {

    bricks = [];

    for (let r = 0; r < brickRows; r++) {

        bricks[r] = [];

        for (let c = 0; c < brickColumns; c++) {

            bricks[r][c] = {
                x: c * (brickWidth + brickPadding) + brickOffsetLeft,
                y: r * (brickHeight + brickPadding) + brickOffsetTop,
                alive: true
            };

        }
    }
}

function drawBall() {

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#facc15";
    ctx.fill();

    ctx.closePath();
}

function drawPaddle() {

    ctx.fillStyle = "#38bdf8";

    ctx.fillRect(
        paddle.x,
        canvas.height - paddle.height - 15,
        paddle.width,
        paddle.height
    );
}

function drawBricks() {

    for (let r = 0; r < brickRows; r++) {

        for (let c = 0; c < brickColumns; c++) {

            const brick = bricks[r][c];

            if (brick.alive) {

                const colors = [
                    "#ef4444",
                    "#f97316",
                    "#eab308",
                    "#22c55e",
                    "#a855f7"
                ];

                ctx.fillStyle = colors[r];

                ctx.fillRect(
                    brick.x,
                    brick.y,
                    brickWidth,
                    brickHeight
                );
            }
        }
    }
}

function collisionDetection() {

    for (let r = 0; r < brickRows; r++) {

        for (let c = 0; c < brickColumns; c++) {

            const brick = bricks[r][c];

            if (brick.alive) {

                if (
                    ball.x > brick.x &&
                    ball.x < brick.x + brickWidth &&
                    ball.y > brick.y &&
                    ball.y < brick.y + brickHeight
                ) {

                    ball.dy = -ball.dy;

                    brick.alive = false;

                    score++;

                    document.getElementById("score").innerText = score;

                    if (score === brickRows * brickColumns) {

                        setTimeout(() => {
                            alert("🎉 축하합니다! 모든 벽돌을 깼습니다!");
                            restartGame();
                        }, 100);
                    }
                }
            }
        }
    }
}

function updatePaddle() {

    if (rightPressed && paddle.x < canvas.width - paddle.width) {
        paddle.x += paddle.speed;
    }

    if (leftPressed && paddle.x > 0) {
        paddle.x -= paddle.speed;
    }
}

function updateBall() {

    ball.x += ball.dx;
    ball.y += ball.dy;

    // 왼쪽 / 오른쪽 벽
    if (
        ball.x + ball.radius > canvas.width ||
        ball.x - ball.radius < 0
    ) {
        ball.dx = -ball.dx;
    }

    // 위쪽 벽
    if (ball.y - ball.radius < 0) {
        ball.dy = -ball.dy;
    }

    // 패들 충돌
    const paddleY =
        canvas.height - paddle.height - 15;

    if (
        ball.y + ball.radius >= paddleY &&
        ball.y + ball.radius <= paddleY + paddle.height &&
        ball.x >= paddle.x &&
        ball.x <= paddle.x + paddle.width
    ) {

        ball.dy = -Math.abs(ball.dy);

        // 패들 위치에 따라 공의 방향 변경
        const hitPosition =
            (ball.x - paddle.x) / paddle.width;

        ball.dx = (hitPosition - 0.5) * 10;
    }

    // 바닥
    if (ball.y + ball.radius > canvas.height) {

        lives--;

        document.getElementById("lives").innerText = lives;

        if (lives <= 0) {

            setTimeout(() => {
                alert("게임 오버! 😢");
                restartGame();
            }, 100);

        } else {

            ball.x = canvas.width / 2;
            ball.y = canvas.height - 50;

            ball.dx = 4;
            ball.dy = -4;
        }
    }
}

function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();
    drawBall();
    drawPaddle();

    collisionDetection();
    updateBall();
    updatePaddle();

    requestAnimationFrame(draw);
}

document.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "ArrowRight") {
            rightPressed = true;
        }

        if (event.key === "ArrowLeft") {
            leftPressed = true;
        }
    }
);

document.addEventListener(
    "keyup",
    function(event) {

        if (event.key === "ArrowRight") {
            rightPressed = false;
        }

        if (event.key === "ArrowLeft") {
            leftPressed = false;
        }
    }
);

function restartGame() {

    score = 0;
    lives = 3;

    document.getElementById("score").innerText = score;
    document.getElementById("lives").innerText = lives;

    paddle.x =
        (canvas.width - paddle.width) / 2;

    ball.x = canvas.width / 2;
    ball.y = canvas.height - 50;

    ball.dx = 4;
    ball.dy = -4;

    createBricks();
}

createBricks();
draw();

</script>

</body>
</html>
"""

components.html(game, height=620, scrolling=False)
