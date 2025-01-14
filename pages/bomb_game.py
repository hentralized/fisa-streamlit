import streamlit as st
import numpy as np

# Streamlit 앱 타이틀
st.title("Minesweeper Game")
st.markdown("Click on the grid to reveal cells. Avoid the mines!")

# 게임 설정
GRID_SIZE = 8  # 그리드 크기 (8x8)
NUM_MINES = 10  # 지뢰 개수

# 게임 초기화
@st.cache_data
def initialize_game():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    mines = np.random.choice(GRID_SIZE * GRID_SIZE, NUM_MINES, replace=False)
    for mine in mines:
        x, y = divmod(mine, GRID_SIZE)
        grid[x, y] = -1  # -1은 지뢰를 의미

    # 숫자 셀 계산
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x, y] == -1:
                continue
            grid[x, y] = count_adjacent_mines(grid, x, y)
    return grid

def count_adjacent_mines(grid, x, y):
    """주변 지뢰 개수를 세는 함수"""
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx, ny] == -1:
                count += 1
    return count

# 세션 상태 초기화
if "grid" not in st.session_state:
    st.session_state.grid = initialize_game()
    st.session_state.revealed = np.zeros((GRID_SIZE, GRID_SIZE), dtype=bool)
    st.session_state.game_over = False

# 그리드 출력
def display_grid():
    """Streamlit에서 그리드를 출력"""
    for x in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for y, col in enumerate(cols):
            if st.session_state.revealed[x, y]:
                if st.session_state.grid[x, y] == -1:
                    col.button("💣", disabled=True, key=f"mine-{x}-{y}")
                else:
                    col.button(f"{st.session_state.grid[x, y]}", disabled=True, key=f"num-{x}-{y}")
            else:
                if col.button(" ", key=f"cell-{x}-{y}"):
                    reveal_cell(x, y)


def reveal_cell(x, y):
    """셀을 열고 지뢰인지 확인"""
    if st.session_state.grid[x, y] == -1:
        st.session_state.game_over = True
    else:
        st.session_state.revealed[x, y] = True
        if st.session_state.grid[x, y] == 0:
            reveal_adjacent_cells(x, y)

def reveal_adjacent_cells(x, y):
    """빈 셀 주변을 자동으로 열기"""
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if not st.session_state.revealed[nx, ny]:
                    st.session_state.revealed[nx, ny] = True
                    if st.session_state.grid[nx, ny] == 0:
                        reveal_adjacent_cells(nx, ny)

# 게임 상태 확인
if st.session_state.game_over:
    st.error("Game Over! You hit a mine. 😢")
    st.button("Restart", on_click=lambda: st.session_state.clear())
else:
    display_grid()
