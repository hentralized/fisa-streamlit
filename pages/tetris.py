import streamlit as st
import pygame
import time

# Streamlit 초기 설정
st.title("Tetris Game with Streamlit")
st.markdown("Use arrow keys to play Tetris. Press the button below to start the game.")

# 게임 시작 버튼
if st.button("Start Tetris Game"):
    # Pygame 초기 설정
    pygame.init()

    # 화면 크기
    screen_width = 300
    screen_height = 600
    block_size = 30

    # 색상
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    # 스크린 생성
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tetris")

    # 게임 루프
    running = True
    clock = pygame.time.Clock()

    # 블록 초기 위치
    block_x = screen_width // 2
    block_y = 0

    while running:
        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 키 입력 처리
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    block_x -= block_size
                if event.key == pygame.K_RIGHT:
                    block_x += block_size
                if event.key == pygame.K_DOWN:
                    block_y += block_size

        # 블록 이동
        block_y += 5

        # 경계 확인
        if block_x < 0:
            block_x = 0
        if block_x > screen_width - block_size:
            block_x = screen_width - block_size
        if block_y > screen_height - block_size:
            block_y = 0  # 블록 초기화

        # 화면 업데이트
        screen.fill(black)
        pygame.draw.rect(screen, red, (block_x, block_y, block_size, block_size))
        pygame.display.flip()

        # 초당 프레임 설정
        clock.tick(10)

    pygame.quit()
    st.write("Game Over!")
